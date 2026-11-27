%% wecSimInputFile_16body_case.m
% V2.7 参数化全系统输入文件 (用于 W7 / GATE 1B 自由衰减、规则波与阻尼对比)
% 用法:
%   1) 由 run_w7_gate1b_suite.m 自动生成 w7_case_cfg.mat 并复制为 wecSimInputFile.m 运行;
%   2) 也可手动单独运行: 若当前目录无 w7_case_cfg.mat, 则按下方默认配置 (noWave + 8 m/s + K1) 运行。
%
% 严格保留 V2.7 红线:
%   - simu.b2b = 1 (96x96 全耦合矩阵)
%   - simu.gravity = 9.81, simu.rho = 1025 (与 AQWA/BEMIO 一致)
%   - simu.explorer = 'off'
%   - body(i).inertiaProducts = bodyInertiaProducts(i,:) (含 60/300 度链 Ixy)
%   - 阻尼版本: quadDragK1 (1.0 版主用) / quadDragS1 (5/3 版) / quadDragZ (置零)

w7_dir = fileparts(mfilename('fullpath'));
if isfile(fullfile(w7_dir, 'w7.m'))
    run(fullfile(w7_dir, 'w7.m'));
elseif isfile(fullfile(w7_dir, 'w7-assembly-data-16body.m'))
    % MATLAB run() 不允许脚本名含连字符 '-', 仓内原名通过 eval 兼容载入
    eval(fileread(fullfile(w7_dir, 'w7-assembly-data-16body.m')));
else
    error('未找到 w7.m (或 w7-assembly-data-16body.m)');
end
clear w7_dir;

%% 默认工况配置 (若存在 w7_case_cfg.mat 则覆盖)
cfg = struct();
cfg.slxFile      = 'SModel_16body.slx';
cfg.endTime      = 30;
cfg.rampTime     = 0;
cfg.dt           = 0.01;
cfg.dtOut        = 0.1;
cfg.cicDt        = 0.1;          % 与 .h5 IRF 原生 0.1 s 分辨率一致 (避免 0.01 s 100倍冗余卷积)
cfg.cicEndTime   = 60;
cfg.saveWorkspace = 0;           % 批处理由主脚本保存精简 .mat, 跳过巨型工作区转存
cfg.waveType     = 'noWave';     % 'noWave' | 'noWaveCIC' | 'regular'
cfg.waveHeight   = 2.0;          % [m] regular 时有效
cfg.wavePeriod   = 10.0;         % [s] regular / noWave 时有效
cfg.waveDir      = 0;            % [deg]
cfg.dampingVer   = 'K1';         % 'K1' | 'S1' | 'Z'
cfg.deduct100t   = false;        % 是否从 Body1 扣减 W2 100 t 塔架接口占位质量
cfg.windMode     = 'turbulent';  % 'still' | 'constant' | 'turbulent'
cfg.windSpeed    = 8.0;          % [m/s]
cfg.aeroLoadsType = 1;           % 0 = LUT (静风安全), 1 = BEM
cfg.aeroLoadsName = fullfile('mostData', 'windTurbine', 'aeroloads', 'Aeroloads_IEA15MW.mat');

if isfile('w7_case_cfg.mat')
    loadedCfg = load('w7_case_cfg.mat');
    if isfield(loadedCfg, 'cfg')
        fn = fieldnames(loadedCfg.cfg);
        for k = 1:numel(fn)
            cfg.(fn{k}) = loadedCfg.cfg.(fn{k});
        end
    end
end

%% Simulation class
simu = simulationClass();
simu.simMechanicsFile = cfg.slxFile;
simu.mode = 'normal';
simu.explorer = 'off';
simu.startTime = 0;
simu.rampTime = cfg.rampTime;
simu.endTime = cfg.endTime;
simu.rho = 1025;
simu.solver = 'ode4';
simu.dt = cfg.dt;
simu.stateSpace = 0;
simu.domainSize = 300;
simu.cicDt = cfg.cicDt;
simu.cicEndTime = cfg.cicEndTime;
simu.gravity = 9.81;
simu.b2b = 1;
simu.dtOut = cfg.dtOut;
simu.saveWorkspace = cfg.saveWorkspace;

%% Wave class
waves = waveClass(cfg.waveType);
switch cfg.waveType
    case 'noWave'
        waves.period = 2*pi;
        waves.direction = cfg.waveDir;
    case 'noWaveCIC'
        % 无波但开启辐射阻尼卷积积分 (自由衰减标准配置)
    case 'regular'
        waves.height = cfg.waveHeight;
        waves.period = cfg.wavePeriod;
        waves.direction = cfg.waveDir;
    otherwise
        error('Unsupported waveType: %s', cfg.waveType);
end

%% 阻尼矩阵选择
switch upper(cfg.dampingVer)
    case 'K1'
        dragTable = quadDragK1;
    case 'S1'
        dragTable = quadDragS1;
    case 'Z'
        dragTable = quadDragZ;
    otherwise
        error('Unsupported dampingVer: %s (expected K1, S1, or Z)', cfg.dampingVer);
end

%% Body class (16 bodies)
for i = 1:16
    body(i) = bodyClass('futi_16body.h5'); %#ok<SAGROW>
    if i == 1 && cfg.deduct100t
        % 扣除 W2 100 t 接口占位质量 (注: .h5 内置 CG 仍为 -3.731 m, 仅作吃水灵敏度对照)
        body(i).mass = bodyMass(i) - 100000.0;
        body(i).inertia = [1.1688e+08, 1.1688e+08, bodyInertiaDiag(i,3)];
    else
        body(i).mass = bodyMass(i);
        body(i).inertia = bodyInertiaDiag(i,:);
    end
    body(i).inertiaProducts = bodyInertiaProducts(i,:);
    body(i).quadDrag.drag = diag(dragTable(i,:));
end

%% Wind class (MOST)
wind = windClass();
switch lower(cfg.windMode)
    case 'still'
        wind.constantWindFlag = 1;
        wind.modules = [0 0];
        wind.directions = [1 0 0; 1 0 0];
    case 'constant'
        wind.constantWindFlag = 1;
        wind.modules = [cfg.windSpeed cfg.windSpeed];
        wind.directions = [1 0 0; 1 0 0];
    case 'turbulent'
        wind.constantWindFlag = 0;
        wind.windDataFile = fullfile('mostData', 'turbSim', sprintf('WIND_%gmps.mat', cfg.windSpeed));
    otherwise
        error('Unsupported windMode: %s', cfg.windMode);
end

%% Windturbine class (MOST IEA 15 MW)
load(fullfile('mostData', 'windTurbine', 'control', 'SteadyStates_IEA15MW.mat'));

windTurbine(1) = windTurbineClass('IEA15MW');
windTurbine(1).aeroLoadsType = cfg.aeroLoadsType;
windTurbine(1).control = 0;
if strcmpi(cfg.windMode, 'still') || cfg.windSpeed <= 0
    % SteadyStates.WINDSPEED 下限为 3 m/s, 静风停机直接置零防 interp1 返回 NaN
    windTurbine(1).omega0 = 0;
    windTurbine(1).bladepitch0 = 0;
    windTurbine(1).GenTorque0 = 0;
else
    windTurbine(1).omega0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.ROTSPD, cfg.windSpeed);
    windTurbine(1).bladepitch0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.BLADEPITCH, cfg.windSpeed);
    windTurbine(1).GenTorque0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.TORQUE, cfg.windSpeed);
end
windTurbine(1).aeroLoadsName = cfg.aeroLoadsName;
windTurbine(1).turbineName   = fullfile('mostData', 'windTurbine', 'turbine_properties', 'Properties_IEA15MW.mat');
windTurbine(1).bladeDataName = fullfile('mostData', 'windTurbine', 'turbine_properties', 'Bladedata_IEA15MW.mat');
windTurbine(1).controlName   = fullfile('mostData', 'windTurbine', 'control', 'Control_IEA15MW.mat');
windTurbine(1).offset_plane  = [0 0];
windTurbine(1).YawControlFlag = 0;

%% Constraint class (15 道局部界面 + 根体接地 Constraint16)
chainAzimuthDeg = [repmat(180, 1, 5), repmat(60, 1, 5), repmat(300, 1, 5)];
for i = 1:15
    phi = chainAzimuthDeg(i);
    constraint(i) = constraintClass(['Constraint' num2str(i)]); %#ok<SAGROW>
    constraint(i).location = constraintPair(i, 3:5);
    constraint(i).orientation.z = [0 0 1];
    constraint(i).orientation.y = [-sind(phi) cosd(phi) 0];
end
constraint(16) = constraintClass('Constraint16');
constraint(16).location = [0 0 0];

%% Mooring class (MOST MooringNLStatic, 3 根 850 m 悬链线)
mooring(1) = mooringClass('mooring1');
mooring(1).location = [0 0 0];
mooring(1).nonlinearStaticData = struct(...
    'flag',          1, ...
    'd',             0.333, ...
    'L',             850, ...
    'linearMassAir', 685, ...
    'nLines',        3, ...
    'nodes',         [-58 0 -14 ; -837 0 -inf]', ...
    'EA',            3.27e9, ...
    'CB',            1, ...
    'MaxIter',       150, ...
    'TolFun',        1e-5, ...
    'TolX',          1e-5, ...
    'HV0_try',       [1e6 2e6; 1e6 2e6; 1e6 2e6]);
