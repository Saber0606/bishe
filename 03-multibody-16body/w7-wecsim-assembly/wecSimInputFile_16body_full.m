%% wecSimInputFile_16body_full.m
% V2.7 全系统合并版: 16 体刚接平台 (quadDragK1 1.0 版) + MOST 风机 (IEA 15 MW) + MooringNLStatic
% 用法: 在工作目录运行 wecSim 时须另存或重命名为 wecSimInputFile.m (并确保同目录含 w7-assembly-data-16body.m 与 mostData)。
run(fullfile(fileparts(mfilename('fullpath')), 'w7-assembly-data-16body.m'));

%% Simulation class
simu = simulationClass();                           % Initialize Simulation Class
simu.simMechanicsFile = 'SModel_16body.slx';        % Specify Simulink Model File
simu.mode = 'normal';                               % ('normal','accelerator','rapid-accelerator')
simu.explorer = 'off';                              % 无逐体 STL/STEP 几何文件, 必须关
simu.startTime = 0;                                 % Simulation Start Time [s]
simu.rampTime = 0;                                  % 首跑 noWave 设为 0; 跑波浪时改 20
simu.endTime = 30;                                  % 首跑静水平衡自检 30 s; 正式工况再拉长
simu.rho = 1025;                                    % Water density [kg/m3]
simu.solver = 'ode4';                               % Fixed step
simu.dt = 0.01;                                     % Simulation Time-Step [s]
simu.stateSpace = 0;                                % 0 = convolution integral
simu.domainSize = 300;                              % Visualization only
simu.cicEndTime = 60;                               % Convolution Integral Time [s]
simu.gravity = 9.81;                                % 与 AQWA/BEMIO 一致 (不用 MOST 默认 9.80665)
simu.b2b = 1;                                       % 16 体全耦合矩阵, 必须为 1
simu.dtOut = 0.1;                                   % Output sampling [s]

%% Wave class (首跑静水无波, 验重浮平衡与吃水回归 z≈0)
waves = waveClass('noWave');                        % 后续跑规则波/不规则波时改此处
waves.period = 2*pi;                                % omega = 1.0 rad/s
waves.direction = 0;                                % Wave Direction [deg]

%% Body class (16 bodies, 沿用 16 体 .h5 + quadDragK1, 不叠加 MOST 单体阻尼)
for i = 1:16
    body(i) = bodyClass('futi_16body.h5');          %#ok<SAGROW>
    body(i).mass = bodyMass(i);                     % AH1 实跑质量 [kg]
    body(i).inertia = bodyInertiaDiag(i,:);         % 对角惯量 [kg-m2]
    body(i).inertiaProducts = bodyInertiaProducts(i,:); % [Ixy Ixz Iyz] [kg-m2]
    body(i).quadDrag.drag = diag(quadDragK1(i,:));  % 1.0 版 (K1); 对照可切 quadDragS1 / quadDragZ
end

%% Wind class (MOST)
wind = windClass();
wind.constantWindFlag = 0;                          % 0 = turbulent wind (mostData)
wind.windDataFile = fullfile('mostData', 'turbSim', strcat('WIND_', num2str(8), 'mps.mat'));

%% Windturbine class (MOST IEA 15 MW)
windSpeed0 = 8;
load(fullfile('mostData', 'windTurbine', 'control', 'SteadyStates_IEA15MW.mat'));

windTurbine(1) = windTurbineClass('IEA15MW');
windTurbine(1).aeroLoadsType = 1;                   % 0 = LUT, 1 = BEM
windTurbine(1).control = 0;                         % 0 = Baseline, 1 = ROSCO
windTurbine(1).omega0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.ROTSPD, windSpeed0);
windTurbine(1).bladepitch0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.BLADEPITCH, windSpeed0);
windTurbine(1).GenTorque0 = interp1(SteadyStates.ROSCO.SS.WINDSPEED, SteadyStates.ROSCO.SS.TORQUE, windSpeed0);
windTurbine(1).aeroLoadsName = fullfile('mostData', 'windTurbine', 'aeroloads', 'Aeroloads_IEA15MW.mat');
windTurbine(1).turbineName = fullfile('mostData', 'windTurbine', 'turbine_properties', 'Properties_IEA15MW.mat');
windTurbine(1).bladeDataName = fullfile('mostData', 'windTurbine', 'turbine_properties', 'Bladedata_IEA15MW.mat');
windTurbine(1).controlName = fullfile('mostData', 'windTurbine', 'control', 'Control_IEA15MW.mat');
windTurbine(1).offset_plane = [0 0];                % 平台平面中心 [0 0]
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
