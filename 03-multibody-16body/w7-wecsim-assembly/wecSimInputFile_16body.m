%% wecSimInputFile_16body.m
% W7 16 体纯浮体 (状态 A) WEC-Sim 输入文件, 2026-11-22 初版。
% 模板来源: WEC-Sim_Applications / MOST 的 wecSimInputFile.m (commit d53d4d4),
%   只沿用 simu / waves / body / constraint 四段的写法与参数名;
%   wind / windTurbine / mooring 三段整段删除 — W7/GATE-C 口径为纯浮体
%   (无系泊、无风机), 基准 (衰减周期 0.316/0.474 rad/s、整体单体 AQWA RAO)
%   同为纯浮体口径, 状态 A/B 不混用 (仓库 AGENTS.md 第 5 节红线 3)。
% 数据来源: 同目录 w7-assembly-data-16body.m (质量/惯量/惯量积 = AH1 实跑值,
%   阻尼 = S1 定案, 约束 = W1 段界), 运行前先由本文件自动载入。
% 与 MOST 模板的关键差异 (逐项有据, 不是笔误):
%   1) simu.b2b = 1: 16 体在 AQWA 中同属一个相互作用组, .h5 的附加质量/
%      辐射阻尼矩阵是 96x96 全耦合矩阵; b2b=0 时 WEC-Sim 只取每体自身
%      6x6 对角块, 体间辐射耦合会被丢掉 (v7.1.0 bodyClass.setDOF /
%      constAddedMassAndDamping 按 b2b 决定矩阵尺寸 6x6 或 6x96)。
%   2) simu.gravity = 9.81, simu.rho = 1025: 与 AQWA/BEMIO 侧口径一致
%      (GATE-A 核查 K33 = rho*g*Awp = 4.460e6 N/m 反推 rho*g = 10056);
%      .h5 内静水刚度按 BEM 侧 rho*g 归一化存储, WEC-Sim 以 simu 的
%      rho*g 还原, 两侧口径必须相同。MOST 模板的 9.80665 不沿用。
%   3) simu.explorer = 'off': 本模型无逐体几何文件 (无 STL/STEP),
%      explorer='on' 时 bodyClass.checkInputs 会因找不到 geometryFile
%      报错 (v7.1.0 bodyClass.m 第 243-247 行); 可视化不影响 GATE-C 数值。
%   4) body(i).quadDrag.drag 用 diag() 展开为 6x6: v7.1.0 checkInputs
%      断言 drag 必须为 6x6 (bodyClass.m 第 173 行); 本方案逐体只有
%      平动对角系数 (转动项由装配涌现), diag() 与方案等价。
%   5) body(i).inertiaProducts 必须赋值: 60 度链段 Ixy = +2.289e6,
%      300 度链段 Ixy = -2.289e6 (AH1 实跑值), 只赋对角会丢这一项。
% 工况段 (waves / endTime / 各体初始位移) 目前是初始化与静水检查口径;
%   GATE-C 的衰减与 RAO 工况按清单第 5 节逐工况改, 不在本文件预设。

%% 装配数据载入 (质量/质心/惯量/惯量积/阻尼/约束体对)
run(fullfile(fileparts(mfilename('fullpath')), 'w7-assembly-data-16body.m'));

%% Simulation class
simu = simulationClass();                           % Initialize Simulation Class
simu.simMechanicsFile = 'SModel_16body.slx';        % Specify Simulink Model File
simu.mode = 'normal';                               % ('normal','accelerator','rapid-accelerator')
simu.explorer = 'off';                              % 见头部差异 3
simu.startTime = 0;                                 % Simulation Start Time [s]
simu.rampTime = 0;                                  % Wave Ramp Time [s] (noWave 时不起作用, 工况时再定)
simu.endTime = 10;                                  % 初始化/静水检查用短时程; 正式工况按清单第 5 节改
simu.rho = 1025;                                    % Water density [kg/m3], 见头部差异 2
simu.solver = 'ode4';                               % Fixed step
simu.dt = 0.01;                                     % Simulation Time-Step [s]
simu.stateSpace = 0;                                % 0 = convolution integral
simu.domainSize = 300;                              % Visualization only
simu.cicEndTime = 60;                               % Convolution Integral Time [s]
simu.gravity = 9.81;                                % [m/s2], 见头部差异 2
simu.b2b = 1;                                       % Body-to-body interactions ON, 见头部差异 1
simu.dtOut = 0.1;                                   % Output sampling [s]

%% Wave class
% 静水 (无波): 常系数水动力, 系数取 BEM 频点中与 waves.period 最接近者。
% period = 2*pi/1.0, 对应 omega = 1.0 rad/s, 在 BEM 频段 0.02-2.10 rad/s 内。
waves = waveClass('noWave');                        % Initialize Wave Class, No Waves
waves.period = 2*pi;                                % BEM period for constant coefficients [s]
waves.direction = 0;                                % Wave Direction [deg]

%% Body class (16 bodies, 编号/顺序同 .h5 与 AH1, 不另起编号)
for i = 1:16
    body(i) = bodyClass('futi_16body.h5');          %#ok<SAGROW> % 同一多体 .h5, 按创建顺序对应体内编号
    body(i).mass = bodyMass(i);                     % User-defined mass [kg] (AH1 实跑值)
    body(i).inertia = bodyInertiaDiag(i,:);         % Moments of inertia, diagonal [kg-m2]
    body(i).inertiaProducts = bodyInertiaProducts(i,:); % [Ixy Ixz Iyz] [kg-m2], 见头部差异 5
    body(i).quadDrag.drag = diag(quadDragS1(i,:));  % 主版 S1 逐体二次阻尼 [6x6 对角], 见头部差异 4
    % 注: 质心/浮心/排水量由 .h5 内置值给出 (hydro body 不在输入文件赋 CG);
    %     装配核对时以 bodyCG 表逐项对 .h5 内置值, 不一致以 AH1 值为准排查。
    % Z 对照版: 同一文件仅把上一行换成 diag(quadDragZ(i,:)), 其余全不动。
end

%% Constraint class (15 道体-体刚接, 体对与位置见 constraintPair)
for i = 1:15
    constraint(i) = constraintClass(['Constraint' num2str(i)]); %#ok<SAGROW> % Initialize constraintClass
    constraint(i).location = constraintPair(i, 3:5); % Constraint Location [m] (全局系, 界面点)
end
