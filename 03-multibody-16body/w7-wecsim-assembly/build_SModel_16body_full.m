%% build_SModel_16body_full.m
% 按 V2.7 生成 16 体刚接 + MOST 风机 + MooringNLStatic 全系统模型 SModel_16body.slx。
% 用法: 在工作根目录 (含 SModel_16body.slx / SModel_16body_template_backup.slx) 运行:
%   >> build_SModel_16body_full

clearvars;
sys = 'SModel_16body';
slxFile = [sys '.slx'];
pureBackup = [sys '_pure_backup.slx'];

if bdIsLoaded(sys)
    close_system(sys, 0);
end

if exist(slxFile, 'file')
    if ~exist(pureBackup, 'file')
        copyfile(slxFile, pureBackup);
        fprintf('[info] 已备份纯浮体模型至 %s\n', pureBackup);
    end
    load_system(sys);
    Simulink.BlockDiagram.deleteContents(sys);
    fprintf('[info] 已清空 %s 内原模块并保留其求解器配置\n', slxFile);
else
    new_system(sys);
    fprintf('[info] 新建空白模型 %s\n', slxFile);
end

%% 载入 WEC-Sim 与 MOST 库
libs = {'WECSim_Lib_Frames', 'WECSim_Lib_Body_Elements', ...
        'WECSim_Lib_Constraints', 'WECSim_Lib_Moorings', 'MOST_Lib'};
for k = 1:numel(libs)
    try
        load_system(libs{k});
    catch ME
        error('无法载入库 %s，请确认 WEC-Sim 与 MOST 已在 MATLAB 路径中。\n原始报错: %s', ...
              libs{k}, ME.message);
    end
end

%% 1. Global Reference Frame + 接地 Constraint16 + Body1 (CEN) + Wind turbine + MooringNLStatic
add_block('WECSim_Lib_Frames/Global Reference Frame', [sys '/Global Reference Frame'], ...
    'Position', [40, 290, 190, 330], ...
    'waves', 'waves', 'simu', 'simu');

add_block('WECSim_Lib_Constraints/Floating (6DOF)', [sys '/Constraint16'], ...
    'Position', [250, 280, 360, 340], ...
    'constraint', 'constraint(16)', ...
    'AttributesFormatString', '%<constraint>');

add_block('WECSim_Lib_Body_Elements/Rigid Body', [sys '/Body1'], ...
    'Position', [430, 280, 540, 340], ...
    'body', 'body(1)', ...
    'AttributesFormatString', '%<body>');

add_block('MOST_Lib/Wind turbine', [sys '/Wind turbine'], ...
    'Position', [420, 120, 555, 190], ...
    'windTurbine', 'windTurbine', ...
    'BEMstruct', 'windTurbine.BEMstruct');
try
    set_param([sys '/Wind turbine'], 'VariantControl', 'sv_1_IEA15MW');
catch
end

add_block('WECSim_Lib_Moorings/MooringNLStatic', [sys '/MooringNLStatic'], ...
    'Position', [460, 410, 510, 445], ...
    'mooring', 'mooring(1)', ...
    'nonlinearStaticData', 'mooring.nonlinearStaticData', ...
    'AttributesFormatString', '%<mooring>');

% 接地与全系统连接: Global -> Constraint16 -> Body1; Wind turbine / MooringNLStatic -> Body1
add_line(sys, 'Global Reference Frame/RConn1', 'Constraint16/LConn1', 'autorouting', 'on');
add_line(sys, 'Constraint16/RConn1', 'Body1/RConn1', 'autorouting', 'on');
add_line(sys, 'Wind turbine/RConn1', 'Body1/RConn1', 'autorouting', 'on');
add_line(sys, 'MooringNLStatic/LConn1', 'Body1/RConn1', 'autorouting', 'on');

%% 2. 三条浮筒链: 180° (Constraint1..5), 60° (Constraint6..10), 300° (Constraint11..15)
pairs = [
     1  2;   2  3;   3  4;   4  5;   5  6;   % 180° 链 (Body2..6)
     1  7;   7  8;   8  9;   9 10;  10 11;   %  60° 链 (Body7..11)
     1 12;  12 13;  13 14;  14 15;  15 16;   % 300° 链 (Body12..16)
];

rowY = [80, 280, 480];
for c = 1:3
    y = rowY(c);
    for s = 1:5
        ic = (c - 1) * 5 + s;      % Constraint1..15
        bBase = pairs(ic, 1);
        bFol  = pairs(ic, 2);

        xCon = 650 + (s - 1) * 330;
        xBod = xCon + 160;

        conName = sprintf('Constraint%d', ic);
        bodName = sprintf('Body%d', bFol);

        add_block('WECSim_Lib_Constraints/Fixed', [sys '/' conName], ...
            'Position', [xCon, y, xCon + 100, y + 60], ...
            'constraint', sprintf('constraint(%d)', ic), ...
            'AttributesFormatString', '%<constraint>');

        add_block('WECSim_Lib_Body_Elements/Rigid Body', [sys '/' bodName], ...
            'Position', [xBod, y, xBod + 110, y + 60], ...
            'body', sprintf('body(%d)', bFol), ...
            'AttributesFormatString', '%<body>');

        add_line(sys, sprintf('Body%d/RConn1', bBase), [conName '/LConn1'], 'autorouting', 'on');
        add_line(sys, [conName '/RConn1'], [bodName '/RConn1'], 'autorouting', 'on');
    end
end

%% 3. 保存并自检
save_system(sys, slxFile);
nBlks = numel(find_system(sys, 'SearchDepth', 1, 'Type', 'block'));
nLines = numel(find_system(sys, 'SearchDepth', 1, 'FindAll', 'on', 'Type', 'line'));
fprintf('[done] 已保存 %s: 共 %d 个模块 (预期 35 = 1 Frame + 16 Body + 16 Constraint + 1 Wind turbine + 1 MooringNLStatic), %d 条连线对象\n', ...
    slxFile, nBlks, nLines);
