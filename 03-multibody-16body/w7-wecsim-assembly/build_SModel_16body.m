%% build_SModel_16body.m
% 自动生成/重建 W7 16 体刚接装配 Simulink 模型 SModel_16body.slx。
% 用法: 在工作目录 (包含或不含模板 SModel_16body.slx 均可) 运行:
%   >> build_SModel_16body
%
% 说明:
%   1) 若当前目录已存在官方模板复制来的 SModel_16body.slx, 脚本会先备份为
%      SModel_16body_template_backup.slx, 清空其中旧的风机/系泊/原单浮体模块,
%      保留其官方 Simscape Multibody 求解器配置 (Configuration6), 再自动搭出
%      16 体无闭环树形刚接拓扑。
%   2) 严格对应 wecSimInputFile_16body.m 与 w7-assembly-data-16body.m:
%      - Global Reference Frame (waves, simu)
%      - Constraint16: Floating (6DOF) 接地 (Global -> Body1)
%      - Body1..Body16: 16 个 Rigid Body (CEN + 180/60/300 三链各 4 段 + 3 外柱)
%      - Constraint1..Constraint15: 15 个 Fixed 约束 (B 朝内侧 -> F 朝外侧)
%   3) 柔性铰版占位提示: 若后续切换 §九 柔性铰, 只需把 Constraint1..15 的
%      Fixed 替换为 Spherical PTO 并改为 pto(1:15) 即可。

clearvars;
sys = 'SModel_16body';
slxFile = [sys '.slx'];
backupFile = [sys '_template_backup.slx'];

if bdIsLoaded(sys)
    close_system(sys, 0);
end

if exist(slxFile, 'file')
    if ~exist(backupFile, 'file')
        copyfile(slxFile, backupFile);
        fprintf('[info] 已备份原模板至 %s\n', backupFile);
    end
    load_system(sys);
    Simulink.BlockDiagram.deleteContents(sys);
    fprintf('[info] 已清空 %s 内原模块并保留其求解器配置\n', slxFile);
else
    new_system(sys);
    fprintf('[info] 新建空白模型 %s\n', slxFile);
end

%% 载入 WEC-Sim Simulink 库 (v7.1.0 库名已从模板 .slx 实测核实)
libs = {'WECSim_Lib_Frames', 'WECSim_Lib_Body_Elements', 'WECSim_Lib_Constraints'};
for k = 1:numel(libs)
    try
        load_system(libs{k});
    catch ME
        error('无法载入 WEC-Sim 库 %s，请先确认 WEC-Sim source 目录已在 MATLAB 路径中。\n原始报错: %s', ...
              libs{k}, ME.message);
    end
end

%% 1. Global Reference Frame + 根体接地 Constraint16 (Floating 6DOF) + Body1 (CEN)
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

% 接地连接: Global Reference Frame (RConn1) -> Constraint16 B (LConn1), F (RConn1) -> Body1 (RConn1)
add_line(sys, 'Global Reference Frame/RConn1', 'Constraint16/LConn1', 'autorouting', 'on');
add_line(sys, 'Constraint16/RConn1', 'Body1/RConn1', 'autorouting', 'on');

%% 2. 三条浮筒链: 180° (Constraint1..5), 60° (Constraint6..10), 300° (Constraint11..15)
% 严格匹配 w7-assembly-data-16body.m 的 constraintPair (B 朝向内侧/中央柱, F 朝向外柱)
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

        xCon = 630 + (s - 1) * 330;
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

        % 连线: Base Body (RConn1) -> Constraint B (LConn1), Constraint F (RConn1) -> Follower Body (RConn1)
        add_line(sys, sprintf('Body%d/RConn1', bBase), [conName '/LConn1'], 'autorouting', 'on');
        add_line(sys, [conName '/RConn1'], [bodName '/RConn1'], 'autorouting', 'on');
    end
end

%% 3. 保存并回显自检
save_system(sys, slxFile);
nBlks = numel(find_system(sys, 'SearchDepth', 1, 'Type', 'block'));
nLines = numel(find_system(sys, 'SearchDepth', 1, 'FindAll', 'on', 'Type', 'line'));
fprintf('[done] 已生成并保存 %s: 共 %d 个模块 (预期 33 = 1 Frame + 16 Body + 16 Constraint), %d 条连线对象\n', ...
    slxFile, nBlks, nLines);
fprintf('[next] 请运行 wecSim 进行静水 (noWave) 首跑测试。\n');
