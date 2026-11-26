%% run_w7_gate1b_suite.m
% V2.7 W7 / GATE 1B 全系统总验收批处理脚本 (Windows MATLAB R2025a / WEC-Sim v7.1.0)
%
% 功能 (按 V2.7 §五 순서):
%   1) 单位运动 quadDrag 涌现代数自检 + 仿真力矢量 (forceMorisonAndViscous) 实测核对;
%   2) 全系统自由衰减 (纵荡 / 垂荡 / 纵摇 / 艏摇, 关风/静风口径, noWaveCIC),
%      对比 NREL/TP-5000-76773 表 11 固有频率 (0.007 / 0.049 / 0.036 / 0.011 Hz)
%      与图 13-16 阻尼比随幅值变化趋势, 并行对比 quadDragK1 (1.0 版)、
%      quadDragS1 (5/3 版) 与 quadDragZ (置零);
%   3) 典型风浪规则波基准 (0° 定常额定风 10.59 m/s + 规则波 H=2 m, T=10 s),
%      提取 6-DOF RAO、Constraint16 零反力、15 截面内力及 60°/300° 链对称性。
%
% 用法:
%   在工作根目录 (含 futi_16body.h5, SModel_16body.slx, mostData/,
%   w7-assembly-data-16body.m, wecSimInputFile_16body_case.m) 下运行:
%     >> run_w7_gate1b_suite
%   注: 脚本自动备份已有 wecSimInputFile.m 并在结束或报错时恢复。
%   输出: output/gate1b_<case>.mat, output/gate1b_summary.json,
%         output/gate1b_verification_summary.txt

%% ==================== 0. 运行开关与工况参数 (可按需调整) ====================
w7_run_unit_algebraic = true;
w7_run_free_decay     = true;
w7_run_reg_wave       = true;

w7_deduct_100t  = false;                 % false = 17,854.16 t 原口径; true = 扣减 Body1 100 t 接口占位
w7_damping_list = {'K1', 'S1', 'Z'};     % 并行对比三版: 1.0 版 K1 / 5/3 版 S1 / 置零 Z
w7_decay_dofs   = {'heave', 'pitch', 'surge', 'yaw'};

% 静水平衡预测吃水偏移 (m), 用于 surge/pitch/yaw 衰减预置平、抑制伴生垂荡瞬态
if w7_deduct_100t
    w7_z_eq_est = -0.27;
else
    w7_z_eq_est = -0.49;
end

% 自由衰减初始位移与仿真时长设置 (通过 Constraint16 Bushing Joint PositionTarget 整体刚体施加)
w7_decay_specs = struct();
w7_decay_specs.heave = struct('dofCol', 3, 'targetField', 'Pz', 'initVal', 2.5,  'unit', 'm',   'endTime', 180, 'refHz', 0.049, 'eqVal', w7_z_eq_est);
w7_decay_specs.pitch = struct('dofCol', 5, 'targetField', 'Ry', 'initVal', 5.0,  'unit', 'deg', 'endTime', 220, 'refHz', 0.036, 'eqVal', 0.0);
w7_decay_specs.surge = struct('dofCol', 1, 'targetField', 'Px', 'initVal', 8.0,  'unit', 'm',   'endTime', 450, 'refHz', 0.007, 'eqVal', 0.0);
w7_decay_specs.yaw   = struct('dofCol', 6, 'targetField', 'Rz', 'initVal', 8.0,  'unit', 'deg', 'endTime', 300, 'refHz', 0.011, 'eqVal', 0.0);

% 典型风浪规则波基准 (0° 对称定常额定风 + 规则波, 检验 60°/300° 对称性与 15 截面反力)
w7_reg_spec = struct('waveHeight', 2.0, 'wavePeriod', 10.0, 'waveDir', 0.0, ...
                     'windSpeed', 10.59, 'rampTime', 20.0, 'endTime', 160.0);

%% ==================== 1. 前置检查与备份保护 ====================
assert(isfile('futi_16body.h5'), '缺少 futi_16body.h5');
assert(isfile('SModel_16body.slx'), '缺少 SModel_16body.slx (请先运行 build_SModel_16body_full)');
assert(isfile('w7-assembly-data-16body.m'), '缺少 w7-assembly-data-16body.m');
assert(isfile('wecSimInputFile_16body_case.m'), '缺少 wecSimInputFile_16body_case.m');
assert(isfolder('mostData'), '缺少 mostData/ 文件夹');

if ~isfolder('output')
    mkdir('output');
end

w7_orig_input_bak = '';
if isfile('wecSimInputFile.m')
    w7_orig_input_bak = 'wecSimInputFile_backup_before_gate1b.m';
    copyfile('wecSimInputFile.m', w7_orig_input_bak);
end
w7_cleanup_obj = onCleanup(@() w7_restore_env(w7_orig_input_bak));

copyfile('wecSimInputFile_16body_case.m', 'wecSimInputFile.m');

w7_summary = struct();
w7_summary.meta = struct( ...
    'date', datestr(now, 'yyyy-mm-dd HH:MM:SS'), ...
    'matlabVersion', version, ...
    'deduct100t', w7_deduct_100t, ...
    'zEqEst', w7_z_eq_est, ...
    'table11RefHz', struct('surge', 0.007, 'heave', 0.049, 'pitch', 0.036, 'yaw', 0.011));

w7_log_lines = {};
w7_log_lines{end+1} = sprintf('=== W7 / GATE 1B Full-System Verification Suite (%s) ===', w7_summary.meta.date);
w7_log_lines{end+1} = sprintf('MATLAB: %s | deduct100t = %d | z_eq_est = %.2f m', ...
    w7_summary.meta.matlabVersion, w7_deduct_100t, w7_z_eq_est);

%% ==================== 2. Part A: 单位运动 quadDrag 涌现代数自检 ====================
if w7_run_unit_algebraic
    run('w7-assembly-data-16body.m');
    w7_unit_alg = struct();
    w7_log_lines{end+1} = '';
    w7_log_lines{end+1} = '--- [Part A1] Algebraic Emergent Check of quadDrag Tables (SWL Origin) ---';
    for w7_iv = 1:numel(w7_damping_list)
        w7_ver = w7_damping_list{w7_iv};
        switch w7_ver
            case 'K1', w7_qt = quadDragK1;
            case 'S1', w7_qt = quadDragS1;
            case 'Z',  w7_qt = quadDragZ;
        end
        w7_em = w7_calc_emergent(w7_qt, bodyCG);
        w7_unit_alg.(w7_ver) = w7_em;
        w7_log_lines{end+1} = sprintf('  [%s] Sum(X/Y/Z) = %.1f / %.1f / %.1f | Bq44=%.4e, Bq55=%.4e, Bq66=%.4e, cross=%.4e', ...
            w7_ver, w7_em.sumSurge, w7_em.sumSway, w7_em.sumHeave, w7_em.Bq44, w7_em.Bq55, w7_em.Bq66, w7_em.crossCG);
    end
    w7_summary.unitAlgebraic = w7_unit_alg;
end

%% ==================== 3. Part B: 全系统自由衰减 (静风口径, 三版并行) ====================
if w7_run_free_decay
    w7_decay_slx = 'SModel_16body_decay.slx';
    w7_decay_results = struct();
    w7_log_lines{end+1} = '';
    w7_log_lines{end+1} = '--- [Part B] Full-System Free Decay (Still Air 0 m/s, noWaveCIC) ---';
    w7_log_lines{end+1} = sprintf('  %-6s %-4s | %8s %8s %7s | %10s %10s | %10s | %s', ...
        'DOF', 'Ver', 'f_simHz', 'f_refHz', 'Err%', 'zeta0%', 'slope/unit', 'liveDragErr', 'InitCheck');

    for w7_id = 1:numel(w7_decay_dofs)
        w7_dof = w7_decay_dofs{w7_id};
        w7_sp  = w7_decay_specs.(w7_dof);

        % 生成仅用于本自由度衰减的 SModel_16body_decay.slx (释放 Bushing Joint 初位移)
        w7_configure_decay_slx('SModel_16body.slx', w7_decay_slx, w7_dof, w7_sp, w7_z_eq_est);

        for w7_iv = 1:numel(w7_damping_list)
            w7_ver = w7_damping_list{w7_iv};
            cfg = struct();
            cfg.slxFile       = w7_decay_slx;
            cfg.endTime       = w7_sp.endTime;
            cfg.rampTime      = 0;
            cfg.dt            = 0.01;
            cfg.dtOut         = 0.1;
            cfg.cicEndTime    = 60;
            cfg.waveType      = 'noWaveCIC';
            cfg.waveHeight    = 0;
            cfg.wavePeriod    = 10.0;
            cfg.waveDir       = 0;
            cfg.dampingVer    = w7_ver;
            cfg.deduct100t    = w7_deduct_100t;
            cfg.windMode      = 'still';
            cfg.windSpeed     = 0;
            cfg.aeroLoadsType = 0; % 静风 0 m/s 用 LUT 避免 BEM 0/0
            save('w7_case_cfg.mat', 'cfg');

            fprintf('\n[GATE 1B Decay] Running DOF=%s, Damping=%s (endTime=%ds)...\n', w7_dof, w7_ver, w7_sp.endTime);
            w7_t0 = tic;
            wecSim;
            w7_elapsed = toc(w7_t0);

            % 提取平台 6-DOF 时程 (以 Body1 位移 + 扣减静态 CG [-3.731])
            w7_t   = output.bodies(1).time;
            w7_pos = output.bodies(1).position;
            w7_pos(:,3) = w7_pos(:,3) - (-3.731); % 换算为相对 SWL 的垂荡偏移

            % 核对 t=0 初始位移是否正确施加
            if strcmp(w7_sp.unit, 'deg')
                w7_init_obs = rad2deg(w7_pos(1, w7_sp.dofCol));
            else
                w7_init_obs = w7_pos(1, w7_sp.dofCol);
            end

            % 提取自由衰减周期、固有频率与对数衰减阻尼比
            w7_met = w7_extract_decay_metrics(w7_t, w7_pos(:, w7_sp.dofCol), w7_sp.unit, w7_sp.refHz);
            w7_met.elapsedSec = w7_elapsed;
            w7_met.initObs    = w7_init_obs;
            w7_met.initTarget = w7_sp.initVal;
            w7_met.constraint16Max = max(abs(output.constraints(16).forceConstraint(:)));

            % 实机复核 Simulink forceMorisonAndViscous 与方案 quadDrag 映射一致
            w7_live_err = w7_check_quadDrag_live(output, w7_ver, w7_sp.dofCol);
            w7_met.liveDragMaxRelErr = w7_live_err.maxRelErr;
            w7_met.emergentMeasured  = w7_live_err.emergentMeasured;

            w7_decay_results.(w7_dof).(w7_ver) = w7_met;

            % 保存精简时程文件
            w7_out_mat = fullfile('output', sprintf('gate1b_decay_%s_%s.mat', w7_dof, w7_ver));
            w7_save_case = struct('t', w7_t, 'pos', w7_pos, 'vel', output.bodies(1).velocity, ...
                'mooringForce', output.mooring(1).forceMooring, ...
                'towerBaseLoad', output.windTurbine(1).towerBaseLoad, ...
                'metrics', w7_met, 'liveDrag', w7_live_err, 'cfg', cfg); %#ok<NASGU>
            save(w7_out_mat, '-struct', 'w7_save_case');

            w7_line = sprintf('  %-6s %-4s | %8.4f %8.4f %+6.2f%% | %9.3f%% %10.4f | %10.2e | obs=%.2f %s (C16=%.1e)', ...
                w7_dof, w7_ver, w7_met.fnHz, w7_sp.refHz, w7_met.freqErrPct, ...
                w7_met.zeta0Pct, w7_met.zetaSlopePerUnit, w7_live_err.maxRelErr, ...
                w7_init_obs, w7_sp.unit, w7_met.constraint16Max);
            w7_log_lines{end+1} = w7_line;
            fprintf('%s\n', w7_line);
        end
    end
    w7_summary.freeDecay = w7_decay_results;
end

%% ==================== 4. Part C: 典型风浪规则波基准 (0° 对称性 + 15 截面反力) ====================
if w7_run_reg_wave
    w7_reg_results = struct();
    w7_log_lines{end+1} = '';
    w7_log_lines{end+1} = sprintf('--- [Part C] Regular Wave + Steady Rated Wind (H=%.1fm, T=%.1fs, Vw=%.2fm/s, Dir=0 deg) ---', ...
        w7_reg_spec.waveHeight, w7_reg_spec.wavePeriod, w7_reg_spec.windSpeed);

    for w7_iv = 1:numel(w7_damping_list)
        w7_ver = w7_damping_list{w7_iv};
        cfg = struct();
        cfg.slxFile       = 'SModel_16body.slx';
        cfg.endTime       = w7_reg_spec.endTime;
        cfg.rampTime      = w7_reg_spec.rampTime;
        cfg.dt            = 0.01;
        cfg.dtOut         = 0.1;
        cfg.cicEndTime    = 60;
        cfg.waveType      = 'regular';
        cfg.waveHeight    = w7_reg_spec.waveHeight;
        cfg.wavePeriod    = w7_reg_spec.wavePeriod;
        cfg.waveDir       = w7_reg_spec.waveDir;
        cfg.dampingVer    = w7_ver;
        cfg.deduct100t    = w7_deduct_100t;
        cfg.windMode      = 'constant';
        cfg.windSpeed     = w7_reg_spec.windSpeed;
        cfg.aeroLoadsType = 1;
        save('w7_case_cfg.mat', 'cfg');

        fprintf('\n[GATE 1B RegWave] Running Damping=%s (H=%.1fm, T=%.1fs, Vw=%.2fm/s)...\n', ...
            w7_ver, cfg.waveHeight, cfg.wavePeriod, cfg.windSpeed);
        w7_t0 = tic;
        wecSim;
        w7_elapsed = toc(w7_t0);

        w7_rm = w7_extract_reg_wave_metrics(output, w7_reg_spec);
        w7_rm.elapsedSec = w7_elapsed;
        w7_reg_results.(w7_ver) = w7_rm;

        % 保存全部 15 道界面反力与平台响应
        w7_con_forces = zeros(numel(output.constraints(1).time), 6, 16);
        for w7_ic = 1:16
            w7_con_forces(:,:,w7_ic) = output.constraints(w7_ic).forceConstraint;
        end
        w7_out_mat = fullfile('output', sprintf('gate1b_regwave_%s.mat', w7_ver));
        w7_save_reg = struct('t', output.bodies(1).time, 'pos1', output.bodies(1).position, ...
            'constraintForces', w7_con_forces, 'mooringForce', output.mooring(1).forceMooring, ...
            'towerBaseLoad', output.windTurbine(1).towerBaseLoad, ...
            'turbinePower', output.windTurbine(1).turbinePower, ...
            'metrics', w7_rm, 'cfg', cfg); %#ok<NASGU>
        save(w7_out_mat, '-struct', 'w7_save_reg');

        w7_line = sprintf('  [%s] SurgeRAO=%.3f m/m | HeaveRAO=%.3f m/m | PitchRAO=%.3f deg/m | MeanHeave=%.4f m | C16max=%.1e | SymMaxRel=%.3f%%', ...
            w7_ver, w7_rm.surgeRAO, w7_rm.heaveRAO, w7_rm.pitchRAO_degPerM, ...
            w7_rm.meanHeaveOffset, w7_rm.constraint16Max, w7_rm.sym60vs300MaxRelPct);
        w7_log_lines{end+1} = w7_line;
        fprintf('%s\n', w7_line);
    end
    w7_summary.regularWave = w7_reg_results;
end

%% ==================== 5. 写出汇总报告与 JSON ====================
w7_txt_path  = fullfile('output', 'gate1b_verification_summary.txt');
w7_json_path = fullfile('output', 'gate1b_summary.json');

w7_fid = fopen(w7_txt_path, 'w');
for w7_il = 1:numel(w7_log_lines)
    fprintf(w7_fid, '%s\n', w7_log_lines{w7_il});
end
fclose(w7_fid);

w7_fid_j = fopen(w7_json_path, 'w');
fprintf(w7_fid_j, '%s\n', jsonencode(w7_summary, 'PrettyPrint', true));
fclose(w7_fid_j);

fprintf('\n[DONE] GATE 1B 批处理完成! 汇总见:\n  %s\n  %s\n', w7_txt_path, w7_json_path);

%% ==================== 本地辅助函数 ====================
function w7_restore_env(bakFile)
    if bdIsLoaded('SModel_16body_decay')
        close_system('SModel_16body_decay', 0);
    end
    if ~isempty(bakFile) && isfile(bakFile)
        copyfile(bakFile, 'wecSimInputFile.m');
        delete(bakFile);
    end
    if isfile('w7_case_cfg.mat')
        delete('w7_case_cfg.mat');
    end
end

function w7_configure_decay_slx(srcSlx, dstSlx, dofName, spec, zEqEst)
    [~, dstSys] = fileparts(dstSlx);
    if bdIsLoaded(dstSys)
        close_system(dstSys, 0);
    end
    copyfile(srcSlx, dstSlx);
    load_system(dstSys);

    c16 = [dstSys '/Constraint16'];
    set_param(c16, 'LinkStatus', 'inactive');
    bjList = find_system(c16, 'LookUnderMasks', 'all', 'FollowLinks', 'on', 'RegExp', 'on', 'Name', 'Bushing Joint');
    assert(~isempty(bjList), '未在 Constraint16 内找到 Bushing Joint');
    bj = bjList{1};

    % 先全部关闭位置目标
    axesNames = {'Px', 'Py', 'Pz', 'Rx', 'Ry', 'Rz'};
    for k = 1:numel(axesNames)
        set_param(bj, [axesNames{k} 'PositionTargetSpecify'], 'off');
        set_param(bj, [axesNames{k} 'PositionTargetValue'], '0');
    end

    % 对 surge / pitch / yaw 预置静态吃水平衡 z_eq_est, 抑制伴生垂荡跳跃
    if ~strcmp(dofName, 'heave')
        set_param(bj, 'PzPositionTargetSpecify', 'on');
        set_param(bj, 'PzPositionTargetPriority', 'High');
        set_param(bj, 'PzPositionTargetValue', num2str(zEqEst, '%.6g'));
        set_param(bj, 'PzPositionTargetValueUnits', 'm');
    end

    % 施加目标自由度初始位移/转角
    tf = spec.targetField;
    set_param(bj, [tf 'PositionTargetSpecify'], 'on');
    set_param(bj, [tf 'PositionTargetPriority'], 'High');
    set_param(bj, [tf 'PositionTargetValue'], num2str(spec.initVal, '%.6g'));
    set_param(bj, [tf 'PositionTargetValueUnits'], spec.unit);

    save_system(dstSys, dstSlx);
    close_system(dstSys, 0);
end

function em = w7_calc_emergent(qt, cg)
    em = struct('sumSurge', sum(qt(:,1)), 'sumSway', sum(qt(:,2)), 'sumHeave', sum(qt(:,3)), ...
                'Bq44', 0, 'Bq55', 0, 'Bq66', 0, 'crossCG', 0);
    for i = 1:size(qt, 1)
        x = cg(i,1); y = cg(i,2); z = cg(i,3);
        em.Bq55 = em.Bq55 + qt(i,1)*abs(z)^3 + qt(i,3)*abs(x)^3;
        em.Bq44 = em.Bq44 + qt(i,2)*abs(z)^3 + qt(i,3)*abs(y)^3;
        em.Bq66 = em.Bq66 + qt(i,1)*abs(y)^3 + qt(i,2)*abs(x)^3;
        em.crossCG = em.crossCG + qt(i,1)*abs(z);
    end
end

function met = w7_extract_decay_metrics(t, sig, unitStr, refHz)
    if strcmp(unitStr, 'deg')
        y = rad2deg(sig);
    else
        y = sig;
    end
    % 用正负峰包络中点估计静平衡点 (兼顾 -0.49 m 垂荡 / -1.25 deg 悬臂静倾与 Z 版低阻尼非整周期尾部)
    [~, locPos0] = findpeaks(y);
    [~, locNeg0] = findpeaks(-y);
    if y(1) > mean(y) && (isempty(locPos0) || locPos0(1) > 2)
        locPos0 = [1; locPos0(:)];
    end
    nPair = min(numel(locPos0), numel(locNeg0));
    if nPair >= 2
        yEq = 0.5 * (mean(y(locPos0(end-1:end))) + mean(y(locNeg0(end-1:end))));
    elseif nPair == 1
        yEq = 0.5 * (y(locPos0(1)) + y(locNeg0(1)));
    else
        nTail = max(10, round(0.4 * numel(y)));
        yEq = mean(y(end-nTail+1:end));
    end
    dy = y - yEq;

    % 寻正峰 (含 t=0 若为释放峰值)
    [pksPos, locsPos] = findpeaks(dy);
    if dy(1) > 0 && (isempty(locsPos) || locsPos(1) > 2)
        pksPos  = [dy(1); pksPos(:)];
        locsPos = [1; locsPos(:)];
    end
    % 仅保留单调有效振幅 (> 初始振幅的 3%)
    valid = pksPos > 0.03 * abs(dy(1));
    pksPos  = pksPos(valid);
    tPeaks  = t(locsPos(valid));

    if numel(tPeaks) >= 2
        periods = diff(tPeaks);
        Tn = mean(periods);
        fn = 1.0 / Tn;
        nCyc = numel(pksPos) - 1;
        zetaCyc = zeros(nCyc, 1);
        ampCyc  = zeros(nCyc, 1);
        for k = 1:nCyc
            delta = log(pksPos(k) / pksPos(k+1));
            zetaCyc(k) = delta / sqrt((2*pi)^2 + delta^2);
            ampCyc(k)  = pksPos(k);
        end
        if numel(ampCyc) >= 2
            pFit = polyfit(ampCyc, zetaCyc * 100, 1); % % per unit
            zetaSlope = pFit(1);
            zeta0     = pFit(2);
        else
            zetaSlope = NaN;
            zeta0     = zetaCyc(1) * 100;
        end
    else
        Tn = NaN; fn = NaN; zetaCyc = []; ampCyc = [];
        zetaSlope = NaN; zeta0 = NaN;
    end

    met = struct();
    met.eqVal          = yEq;
    met.nPeaks         = numel(pksPos);
    met.tPeaks         = tPeaks(:)';
    met.ampPeaks       = pksPos(:)';
    met.zetaPctPerCycle = (zetaCyc(:)') * 100;
    met.ampCycleInit   = ampCyc(:)';
    met.TnSec          = Tn;
    met.fnHz           = fn;
    met.refHz          = refHz;
    met.freqErrPct     = (fn - refHz) / refHz * 100;
    met.zeta0Pct       = zeta0;
    met.zetaSlopePerUnit = zetaSlope;
end

function res = w7_check_quadDrag_live(output, dampingVer, dofCol)
    % 读取 Simulink 实际输出的 forceMorisonAndViscous, 验证与 diag(quadDrag) 映射一致,
    % 并按各体质心输运至 SWL [0 0 0] 复测等效涌现系数。
    run('w7-assembly-data-16body.m');
    switch dampingVer
        case 'K1', qt = quadDragK1;
        case 'S1', qt = quadDragS1;
        case 'Z',  qt = quadDragZ;
    end

    v1 = output.bodies(1).velocity;
    [~, idxPeak] = max(abs(v1(:, dofCol)));
    maxRel = 0.0;
    F_swl = zeros(1, 6);

    for i = 1:16
        vi = output.bodies(i).velocity(idxPeak, :);
        Fi_sim = output.bodies(i).forceMorisonAndViscous(idxPeak, :);
        Fi_exp = -qt(i,:) .* vi .* abs(vi);
        denom = max(1.0, norm(Fi_exp));
        rel = norm(Fi_sim - Fi_exp) / denom;
        if rel > maxRel
            maxRel = rel;
        end
        ri = output.bodies(i).position(idxPeak, 1:3); % 瞬时位置近似输运至原点
        Mi_swl = Fi_sim(4:6) + cross(ri, Fi_sim(1:3));
        F_swl(1:3) = F_swl(1:3) + Fi_sim(1:3);
        F_swl(4:6) = F_swl(4:6) + Mi_swl;
    end

    vRef = v1(idxPeak, dofCol);
    if abs(vRef) > 1e-6
        emMeas = -F_swl(dofCol) / (vRef * abs(vRef));
    else
        emMeas = 0.0;
    end
    res = struct('idxPeak', idxPeak, 'vRefAtPeak', vRef, ...
                 'maxRelErr', maxRel, 'F_swl', F_swl, 'emergentMeasured', emMeas);
end

function rm = w7_extract_reg_wave_metrics(output, spec)
    t   = output.bodies(1).time;
    pos = output.bodies(1).position;
    pos(:,3) = pos(:,3) - (-3.731);

    % 取最后 5 个完整波周期作稳态统计
    tWin = t >= (spec.endTime - 5 * spec.wavePeriod);
    A_wave = spec.waveHeight / 2.0;

    sAmp = 0.5 * (max(pos(tWin, 1)) - min(pos(tWin, 1)));
    hAmp = 0.5 * (max(pos(tWin, 3)) - min(pos(tWin, 3)));
    pAmp = 0.5 * (max(pos(tWin, 5)) - min(pos(tWin, 5)));

    % 校核 60° (Constraint6..10) 与 300° (Constraint11..15) 对称性
    symMaxRel = 0.0;
    for s = 1:5
        F60  = output.constraints(5 + s).forceConstraint(tWin, :);
        F300 = output.constraints(10 + s).forceConstraint(tWin, :);
        % 局部系下 N(1), Vz(3), My(5) 应相等; Vy(2), T(4), Mz(6) 应反号
        F300_mapped = F300;
        F300_mapped(:, [2 4 6]) = -F300_mapped(:, [2 4 6]);
        for c = [1 3 5] % 主对称分量 N, Vz, My
            scale = max(abs(F60(:, c)));
            if scale > 1e3
                rel = max(abs(F60(:, c) - F300_mapped(:, c))) / scale * 100;
                symMaxRel = max(symMaxRel, rel);
            end
        end
    end

    rm = struct();
    rm.surgeRAO = sAmp / A_wave;
    rm.heaveRAO = hAmp / A_wave;
    rm.pitchRAO_degPerM = rad2deg(pAmp) / A_wave;
    rm.meanSurge = mean(pos(tWin, 1));
    rm.meanHeaveOffset = mean(pos(tWin, 3));
    rm.meanPitchDeg = rad2deg(mean(pos(tWin, 5)));
    rm.constraint16Max = max(abs(output.constraints(16).forceConstraint(:)));
    rm.sym60vs300MaxRelPct = symMaxRel;
end
