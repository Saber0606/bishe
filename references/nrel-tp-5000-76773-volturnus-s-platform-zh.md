# UMaine VolturnUS-S 参考平台定义——为 IEA Wind 15 MW 海上参考风电机组开发

**IEA Wind TCP Task 37**

2020 年 7 月

技术报告

---

# UMaine VolturnUS-S 参考平台定义——为 IEA Wind 15 MW 海上参考风电机组开发

Christopher Allen,¹ Anthony Viselli,¹ Habib Dagher,¹ Andrew Goupee,¹ Evan Gaertner,² Nikhar Abbas,² Matthew Hall,² 和 Garrett Barter²

¹ University of Maine（缅因大学）
² National Renewable Energy Laboratory（国家可再生能源实验室，NREL）

**建议引用格式**

Allen, Christopher, Anthony Viselli, Habib Dagher, Andrew Goupee, Evan Gaertner, Nikhar Abbas, Matthew Hall, and Garrett Barter. Definition of the UMaine VolturnUS-S Reference Platform Developed for the IEA Wind 15-Megawatt Offshore Reference Wind Turbine. Golden, CO: National Renewable Energy Laboratory. NREL/TP-5000-76773. https://www.nrel.gov/docs/fy20osti/76773.pdf.

---

## 声明

本工作由 National Renewable Energy Laboratory（NREL）撰写完成（部分内容）。NREL 由 Alliance for Sustainable Energy, LLC 运营，与美国能源部（DOE）的合同号为 DE-AC36-08GO28308。经费由美国能源部能效与可再生能源办公室下属的风能技术办公室提供。本报告中的观点不一定代表美国能源部或美国政府的观点。

本报告可在 National Renewable Energy Laboratory (NREL) 免费获取，网址：www.nrel.gov/publications。

1991 年之后出版的美国能源部（DOE）报告，以及越来越多的 1991 年之前的文献，均可在 www.OSTI.gov 免费获取。

封面照片由 Dennis Schroeder 拍摄：（顺时针，自左向右）NREL 51934、NREL 45897、NREL 42160、NREL 45891、NREL 48097、NREL 46526。

NREL 采用含回收成分的纸张印刷。

---

## 缩略语表

| 缩略语 | 英文全称 | 中文 |
|---|---|---|
| DLC | design load case | 设计载荷工况 |
| DOF | degree of freedom | 自由度 |
| IEC | International Electrotechnical Commission | 国际电工委员会 |
| QTF | quadratic transfer function | 二阶传递函数 |
| RAO | response amplitude operator | 响应幅值算子 |
| RNA | rotor nacelle assembly | 风轮—机舱总成 |
| ROSCO | Reference OpenSource Controller | 参考开源控制器 |
| SWL | still water line | 静水面（静水线） |
| NREL | National Renewable Energy Laboratory | 国家可再生能源实验室 |
| UMaine | University of Maine | 缅因大学 |

---

## 执行摘要

参考风电机组是风电行业的重要组成部分。它们是公开可用的基准机型，研究人员和企业可以自由使用，用来探索新技术、新设计，也有助于推动产学研之间的协作。今年早些时候，国际能源署（IEA）发布了 15 兆瓦（MW）参考风电机组，它是目前公开可用的最大参考机型（Gaertner et al. 2020）。IEA 15-MW 参考机组的尺寸，反映了海上风电机组单机容量不断变大的行业趋势。根据美国能源部《2018 年海上风电技术市场报告》和美国风能协会的数据，过去几年海上风电发展势头明显，值得有针对性地加大科研投入（Musial et al. 2019）。马萨诸塞州、纽约州、马里兰州等几个州已经出台新政策，或加强了原有政策，支持开发 4000 MW 以上的海上风电。展望近期，美国海上风电在建及规划项目管线中的潜在装机容量已达 25,824 MW（Musial et al. 2019）。

美国海上风能资源总量虽然是全国当前用电量的两倍多，但其中近 60% 位于深水海域，必须依靠漂浮式基础技术（Schwartz et al. 2010）。在欧洲的大多数商业化风电场，以及近期的美国项目中，水深 30 米（m）以内的海上风电机组采用单桩基础，水深 25 m 到约 50 m 采用钢制导管架基础。而在 50 m 以上水深——美国大部分海上风电潜力正位于这一水深范围——导管架基础的成本高得难以承受，必须采用漂浮式海上风电机组技术。

本报告是《IEA Wind TCP Task 37：IEA Wind 15 MW 海上参考风电机组定义》（Gaertner et al. 2020）的配套补充文件。本报告定义了缅因大学（UMaine）VolturnUS-S 参考漂浮式半潜平台，该平台专为支撑 IEA 15-MW 参考风电机组而设计。报告中描述的设计与布置，旨在一般性地代表未来漂浮式海上风电技术的发展方向。除漂浮式平台外，本报告还详细给出了漂浮式风电机组其他专属部件，包括系泊系统、塔架和风电机组控制器。

---

## 目录

- 1 引言 …… 1
- 2 设计细节 …… 6
  - 2.1 UMaine VolturnUS-S 半潜式平台 …… 6
  - 2.2 系泊系统参数 …… 13
  - 2.3 漂浮式塔架 …… 15
  - 2.4 风电机组控制器 …… 19
- 3 系统辨识 …… 20
  - 3.1 静态纵荡—横荡偏移 …… 20
  - 3.2 刚体自由衰减 …… 21
  - 3.3 响应幅值算子（RAO） …… 23
- 4 系统性能评估 …… 26
- 参考文献 …… 33

---

## 图目录

- 图 1 为支撑 IEA-15-240 RWT 系统定义而设计的 UMaine VolturnUS-S 参考平台。图由 University of Maine 提供 …… 2
- 图 2 漂浮式风电机组（FOWT）参考坐标系。图由 University of Maine 提供 …… 4
- 图 3 总布置图。图由 University of Maine 提供 …… 5
- 图 4 WAMIT 计算的附加质量与辐射阻尼随频率的变化 …… 8
- 图 5 辐射脉冲响应函数 …… 9
- 图 6 WAMIT 计算的 0˚ 浪向下的一阶波浪激励系数 …… 10
- 图 7 WAMIT 计算的 0˚ 浪向下二阶波浪力的差频（左）与和频（右）结果 …… 11
- 图 8 OpenFOAM 中纵荡定常流（即流向自右向左）阻力仿真，图中为流体 x 向速度，单位 m/s …… 12
- 图 9 系泊系统在惯性坐标系中的布置，平面图（上）和立面图（下）。图由 University of Maine 提供 …… 15
- 图 10 塔架固有频率与激励频率的相对关系 …… 16
- 图 11 塔架结构参数随静水面以上塔架高度的变化 …… 18
- 图 12 导缆孔与锚链张力随纵荡—横荡偏移的变化 …… 20
- 图 13 静水面纵荡与横荡自由衰减时程（上），以及阻尼比随初始周期幅值的变化（下） …… 21
- 图 14 静水面垂荡自由衰减时程（上），以及阻尼比随初始周期幅值的变化（下） …… 22
- 图 15 静水面纵摇与横摇自由衰减时程（上），以及阻尼比随初始周期幅值的变化（下） …… 22
- 图 16 静水面艏摇自由衰减时程（上），以及阻尼比随初始周期幅值的变化（下） …… 23
- 图 17 静水面纵荡 RAO 幅值（上）与相位（下） …… 24
- 图 18 静水面垂荡 RAO 幅值（上）与相位（下） …… 24
- 图 19 静水面纵摇 RAO 幅值（上）与相位（下） …… 25
- 图 20 风轮—机舱总成（RNA）前后方向 RAO 幅值（上）与相位（下） …… 25
- 图 21 DLC 加速度统计（m/s2） …… 29
- 图 22 DLC 挠度与位移统计（m 或 ˚） …… 30
- 图 23 DLC 弯矩统计（kN-m） …… 31
- 图 24 DLC 力统计（N） …… 32

---

## 表目录

- 表 1 漂浮式海上风电机组系统总体参数 …… 3
- 表 2 半潜式平台参数 …… 6
- 表 3 WAMIT 计算的浮体静水刚度（N/m、N/rad 或 N-m/rad） …… 7
- 表 4 WAMIT 计算的浮体无穷频率附加质量（kg、kg-m 或 kg-m2） …… 9
- 表 5 粘性阻尼矩阵（N-s2/m2、N-s2、N-s2/m、N-m-s2） …… 12
- 表 6 系泊系统参数 …… 13
- 表 7 系泊缆阻力与附加质量系数 …… 13
- 表 8 漂浮式塔架参数 …… 17
- 表 9 漂浮式塔架用钢材料参数 …… 17
- 表 10 塔架尺寸随高度的变化 …… 17
- 表 11 刚体固有频率 …… 21
- 表 12 IEC 设计载荷工况矩阵 …… 27
- 表 13 OpenFAST 输出量定义 …… 28
# 1 引言

本报告给出缅因大学（UMaine）VolturnUS-S 参考半潜式浮式平台的设计定义，该平台用于支撑国际能源署（IEA）15-240-RWT 这台 15 兆瓦（MW）参考风电机组。这座半潜式平台是 UMaine 专利混凝土浮式基础技术的通用钢制版本，该技术是 UMaine 与美国能源部合作开发的（Viselli et al. 2015a, 2015b; Viselli et al. 2014）。本报告是《IEA Wind TCP Task 37：IEA Wind 15 兆瓦海上参考风电机组定义》（Gaertner et al. 2020）的配套补充文件，详细说明了为支撑这台 15 MW 参考风电机组而开发的浮式半潜式平台设计。

近年来，海上风电机组的单机容量快速攀升，8～12 MW 的机组如今已成为主流。机组越做越大，浮式海上风电系统的其他部件也必须跟着升级，才能满足大型机组新的设计要求。本报告给出的浮式支撑系统在设计时充分考虑了当前的技术发展趋势，目标是代表未来浮式海上风电技术的通用形态。UMaine 开发这一参考设计，是希望为行业提供一个公开的设计基准，方便各方探索新技术、验证新设计方法，也促进产业界与研究人员之间的合作。

如图 1 所示，本报告定义的参考浮式海上风电机组由四部分组成：浮式半潜平台、三根链式悬链线系泊系统、专为浮式应用设计的塔架，以及针对浮式机组重新整定的控制器，四者都是围绕 Gaertner et al.（2020）定义的 IEA-15-240-RWT 量身配套的。这套参考浮式风电机组系统将随 IEA-15-240-RWT 一起向风电行业发布：设计细节见本报告，同时还提供开源的 OpenFAST 和 HAWC2 模型，存放在 Github 仓库中，地址为：https://github.com/IEAWindTask37/IEA-15-240-RWT。

本报告给出 IEA-15-240-RWT 浮式海上风电机组建模所需的数据和系统特性。第 2 节是系统总览，介绍整机的布置形式和关键特性参数，并给出整机坐标系——该坐标系把浮式机组定义在 OpenFAST 模型的惯性坐标系中；随后各小节分别详细介绍浮式机组的各个子系统，即浮式平台、系泊系统、风机塔架和风机控制器。第 3 节给出系统辨识仿真的结果，包括静态偏移、刚体自由衰减，以及系统在波浪载荷作用下的响应幅值算子。第 4 节最后选取国际电工委员会（IEC）的若干载荷工况，评估这台浮式机组在正常和极端条件下的性能。

图 1 UMaine VolturnUS-S 参考平台，其设计目的是支撑 IEA-15-240 RWT 系统定义。图片由缅因大学提供

# 2 设计细节

本节详细介绍 UMaine VolturnUS-S 半潜式参考浮式海上风电机组及其各组成部分的特性和布置，平面图和立面图见图 3，系统总体特性见表 1。除非另有说明，本报告中所有数值均相对于图 2 定义的坐标系给出。这套系统专为支撑 IEA-15-240-RWT 而设计，主体是一座四立柱钢制半潜平台——三根立柱呈放射状布置，另一根位于中央——靠三根悬链线系泊缆组成的阵列固定在站位上，部署水深为 200 米（m）。塔架是针对浮式应用专门设计的，与最初随单桩基础发布的塔架不同（Gaertner et al. 2020）；塔架连接在平台的中央立柱上，使叶轮-机舱组件（RNA）的轮毂中心高出静水面（SWL）150 m。

平台安装就位后吃水 20 m，立柱上甲板的干舷为 15 m。整机组装完成后排水体积为 20,206 立方米（m3）（海水密度取 1,025 千克每立方米 [kg/m3]），其质量构成为：塔架 1,263 t（吨），RNA 991 t，带压载的平台 17,839 t，此外系泊系统提供 6,065 千牛（kN）的垂向预张力。系统假定部署水深为 200 m，由三根链式悬链线系泊缆固定站位。这套发散式悬链线系泊的缆绳沿径向延伸至锚点，锚点距塔架中心线 837.60 m。

IEA-15-240-RWT 风机本身的特性和规格见先前发布的报告《IEA Wind TCP Task 37：IEA Wind 15 兆瓦海上参考风电机组定义》（Gaertner et al. 2020），本报告不再重复给出。

表 1 浮式海上风电机组系统总体特性

| 参数 | 单位 | 数值 |
|---|---|---|
| 风机额定功率 | MW | 15 |
| 轮毂高度 | m | 150 |
| 包络尺寸¹（长、宽、高） | m | 90.1, 102.1, 290.0 |
| 平台型式 |  | 半潜式 |
| 干舷 | m | 15 |
| 吃水 | m | 20 |
| 系统总质量 | t | 20,093 |
| 平台质量 | t | 17,839 |
| 塔架质量 | t | 1,263 |
| RNA 质量 | t | 991 |
| 水深 | m | 200 |
| 系泊系统 | - | 三根链式悬链线 |

¹ 系统的包络尺寸描述的是整套完整结构所占据的空间范围。在图 3 中，长和宽分别是系统最外侧点沿 x 轴和 y 轴方向的距离；高则是从龙骨底到叶轮直径顶点的 z 向总距离。

图 2 浮式海上风电机组参考坐标系。图片由缅因大学提供

图 3 总布置图。图片由缅因大学提供

## 2.1 UMaine VolturnUS-S 半潜式平台

本报告给出的参考平台是一座四立柱钢制半潜平台，其总体特性见表 2，包括系统质量、尺寸、重心和浮心位置以及惯量。如图 3 所示，船体布置为：三根直径 12.5 m 的浮力立柱呈放射状布置，柱中心距塔架垂向轴线 51.75 m；第四根浮力立柱位于平台中央的纵荡-横荡平面内，平台与塔架的接口就设在这根立柱顶部。中央立柱与三根外立柱之间，靠三根宽 12.5 m、高 7.0 m 的矩形底部浮筒相连，另有三根直径 0.9 m 的径向斜撑，分别连接在浮力立柱的底部和顶部。平台在站工作时总质量为 17,854 t，其中结构钢 3,914 t；固定压载为铁矿石混凝土，共 2,540 t，平均分成三份，分别放在三根径向立柱的底部；流体压载为海水，共 11,300 t，灌满三根水下浮筒的大部分空间；另外还有塔架接口连接构造 100 t。塔架接口没有做详细设计，处理上假定在干舷高度处有一个 100 t 的点质量，并假定下部结构与塔架之间为刚性连接。

表 2 半潜式平台特性

| 参数 | 单位 | 数值 |
|---|---|---|
| 船体排水量 | m3 | 20,206 |
| 船体钢质量 | t | 3,914 |
| 塔架接口质量 | t | 100 |
| 压载质量（固定/流体） | t | 2,540/11,300 |
| 吃水 | m | 20 |
| 干舷 | m | 15 |
| 重心垂向位置（距 SWL） | m | -14.94 |
| 浮心垂向位置（距 SWL） | m | -13.63 |
| 横摇惯量（绕重心） | kg-m2 | 1.251E+10 |
| 纵摇惯量（绕重心） | kg-m2 | 1.251E+10 |
| 艏摇惯量（绕重心） | kg-m2 | 2.367E+10 |

在 OpenFAST 的水动力模块 HydroDyn 中，系统的水动力特性用势流模型加二次型阻力模型来表示。注意，本节后续所有数值均相对于平台参考点给出，该参考点在 OpenFAST 中定义为静水面与塔架轴线的交点。势流模型中随频率变化的系数，是用边界元法水动力求解器 WAMIT v6 计算的：该软件求解一阶静水力、绕射和辐射问题，再利用得到的响应幅值算子（RAO）计算二阶波浪激励力的二次传递函数（QTF）（Lee 1995）。总的来说，WAMIT 给出的系数涵盖了平台的水动力附加质量、波浪辐射阻尼、静水恢复力，以及一阶和二阶波浪激励力等特性。另外，二次型阻力模型的系数则用于计入非线性粘性阻力效应，其依据是平台整体的运动速度。

WAMIT 根据平台的水下几何形状计算出的静水刚度系数见表 3。这些数值均相对于平台参考点计算。需要注意的是，表 3 中的横摇和纵摇项所表示的恢复力矩，只计入了水线面面积惯性矩和系统浮心这两方面的贡献。每个静水恢复力矩中的质量分量，是在 OpenFAST 框架内单独计算并施加的，因此没有包含在表 3 中。

表 3 WAMIT 计算的船体静水刚度（N/m、N/rad 或 N-m/rad）

|  | 纵荡 | 横荡 | 垂荡 | 横摇 | 纵摇 | 艏摇 |
|---|---|---|---|---|---|---|
| 纵荡 | 0 | 0 | 0 | 0 | 0 | 0 |
| 横荡 | 0 | 0 | 0 | 0 | 0 | 0 |
| 垂荡 | 0 | 0 | 4.470E+06 | 0 | 0 | 0 |
| 横摇 | 0 | 0 | 0 | 2.190E+09 | 0 | 0 |
| 纵摇 | 0 | 0 | 0 | 0 | 2.190E+09 | 0 |
| 艏摇 | 0 | 0 | 0 | 0 | 0 | 0 |

水动力附加质量和辐射阻尼系数随平台响应频率的变化见图 4。需要注意的是，根据以往对纵荡-横荡平面内具有类似对称性的系统所做的研究，图中只给出了上三角的非对角项，因为下三角的对应项与之完全相同（Robertson et al. 2014）。另外，由于纵荡-横荡方向的对称性，纵荡与横荡、纵摇与横摇的附加质量和阻尼数值相同，在图中曲线彼此重合。除随频率变化的附加质量外，无穷频率处的附加质量系数见表 4。

势流分析得到的辐射阻尼，在 OpenFAST 的时域环境中是通过辐射脉冲响应函数的时域卷积来施加的（HydroDyn 中 RdtnMod = 1）。卷积形式能够反映辐射波所引起的水动力载荷的记忆效应；之所以不用另一种状态空间形式，是因为以往研究表明，对于类似系统，卷积方法的精度更高（Duarte et al. 2013）。脉冲响应函数由 WAMIT 的 F2T 工具计算，见图 5。需要注意的是，前面提到的附加质量的对称性规律同样适用于阻尼特性。另外，所有自由度（DOF）的响应在 45 秒（s）之前都已衰减到零，因此 HydroDyn 中保留的总记忆时间 RdtnTMax 保守地取为 60 s。
图 4 WAMIT 计算的附加质量与辐射阻尼随频率的变化

表 4 WAMIT 计算的船体无穷频率附加质量（kg、kg-m 或 kg-m2）

|  | 纵荡 | 横荡 | 垂荡 | 横摇 | 纵摇 | 艏摇 |
|---|---|---|---|---|---|---|
| 纵荡 | 9.640E+06 | 0 | 0 | 0 | -1.010E+08 | 0 |
| 横荡 | 0 | 9.640E+06 | 0 | 1.010E+08 | 0 | 0 |
| 垂荡 | 0 | 0 | 2.480E+07 | 0 | 0 | 0 |
| 横摇 | 0 | 0 | 0 | 1.160E+10 | 0 | 0 |
| 纵摇 | -1.010E+08 | 0 | 0 | 0 | 1.160E+10 | 0 |
| 艏摇 | 0 | 0 | 0 | 0 | 0 | 2.010E+10 |

图 5 辐射脉冲响应函数

图 6 给出了浪向角 0˚ 时一阶波浪激励系数随波浪频率的变化。左上图和右上图分别是平动自由度和转动自由度载荷的幅值，左下图和右下图则分别是平动自由度和转动自由度载荷响应的相位。需要注意，图中没有给出横荡、横摇和艏摇的结果：由于平台对称，浪向角 0˚ 时这几个自由度上的总绕射载荷积分恰好为零。

图 6 WAMIT 计算的浪向角 0˚ 时一阶波浪激励系数

图 7 给出了浪向角 0˚ 时和频与差频二阶波浪激励的二次传递函数（QTF），浪向定义见图 2。WAMIT 生成这些 QTF 所用的响应幅值算子，以一阶水动力系数、整个浮式系统的质量矩阵，以及平台在未偏移位置处算得的线性化系泊刚度矩阵为基础，其中忽略了风机弹性、气动载荷和水动力粘性阻力。需要说明的是，计算二阶力项会显著拉长分析时间，因此这里给出的频率范围为 0.04-0.48 hertz (Hz)，频率间隔 0.008 Hz。这一组频率能够覆盖半潜式平台上重要的差频（慢漂）载荷，尤其是纵荡方向的慢漂载荷（Chakrabarti 2005），其和频范围也包含了风机的主要结构频率。使用二阶差频波浪载荷时，相关分析规程建议把考虑的波浪频率取到波浪场谱峰频率为止（Jonkman et al. forthcoming）。因此，这里给出的二阶频率范围可以分析谱峰周期最长达 25 s 的波浪场。

图 7 WAMIT 计算的浪向角 0˚ 时差频（左）与和频（右）二阶波浪力

已有研究表明，对漂浮式海上风机半潜平台而言，由流动分离引起的阻力是总水动力阻尼的重要组成部分（Coulling et al. 2013）。这部分阻尼在势流模型中没有考虑，本报告用二次阻力模型来表示，系数见表 5。在 OpenFAST 中，这个二次阻力模型与 HydroDyn 的线性辐射阻尼模型配合使用，共同表示平台的总水动力阻尼。

表 5 粘性阻尼矩阵（N-s2/m2, N-s2, N-s2/m, N-m-s2）

|  | 纵荡 | 横荡 | 垂荡 | 横摇 | 纵摇 | 艏摇 |
|---|---|---|---|---|---|---|
| 纵荡 | 9.225E+05 | 0 | 0 | 0 | -8.918E+06 | 0 |
| 横荡 | 0 | 9.225E+05 | 0 | 8.918E+06 | 0 | 0 |
| 垂荡 | 0 | 0 | 2.296E+06 | 0 | 0 | 0 |
| 横摇 | 0 | 8.918E+06 | 0 | 1.676E+10 | 0 | 0 |
| 纵摇 | -8.918E+06 | 0 | 0 | 0 | 1.676E+10 | 0 |
| 艏摇 | 0 | 0 | 0 | 0 | 0 | 4.798E+10 |

粘性阻尼模型用开源计算流体力学软件 OpenFOAM 计算，具体采用其定常、不可压缩求解器 SimpleFoam（Greenshields 2011）。如图 8 所示，建模时只取浸没于水中的部分，并利用平台关于 y-z 平面的对称性（平面定义见图 2）。一共做了四个独立的计算工况：分别考察流体以 1 meter per second (m/s) 或 1˚/s 的单位速度相对平台运动时，平台纵荡、垂荡、横摇和艏摇自由度所受的净阻力（绕平台参考点）。计算一直进行到计算域内达到定常状态，然后把浸没体表面的压力对塔架竖直轴线与 SWL 的交点积分。基于平台对称的假设，表 5 矩阵中横荡和纵摇的各项分别取与纵荡和横摇相同的数值。需要说明的是，分析中海水的运动粘度取 1.5E-06 m2/s（40°F 海水），流体密度取 1,250 kg/m3。

图 8 OpenFOAM 中纵荡定常流（即流向自右向左）阻力计算，图中为流体的 x 向速度，单位 m/s

## 2.2 系泊系统参数

本节介绍 UMaine VolturnUS-S 锚链系泊系统的设计。系泊系统的参数和布置分别见表 6 和图 9。系泊系统由三根 850-m 长的锚链悬链线组成。每根系泊线在导缆孔处与平台三根外立柱之一相连，连接点位于 SWL 以下 14 m。各系泊线沿径向向外延伸至锚固点，锚固点在纵荡-横荡平面内按 120 度等间隔布置，深度为 200 m，距塔架中心线的径向距离为 837.60 m。所有系泊线均采用无档 R3 锚链，公称（链杆）直径为 185 millimeters (mm)。系泊线的阻力系数和附加质量系数见表 7，选取时参考了 DNVGL-RP-C205（Det Norske Veritas 2010）和 DNVGL-OS-301（DNV GL 2015）。需要注意的是，表中系数给出了两种口径：一是上述标准按锚链公称直径给出的规定值，二是 MoorDyn 中按体积等效直径（即与锚链单位长度体积相同的圆柱直径）换算后的调整值（Hall and Goupee 2015）。

表 6 系泊系统参数

| 参数 | 单位 | 值 |
|---|---|---|
| 系泊系统型式 | - | 锚链悬链线 |
| 系泊线型式 | - | R3 无档系泊链 |
| 系泊线破断强度 | kN | 22,286 |
| 系泊线数量 | - | 3 |
| 锚固深度 | m | 200 |
| 导缆孔深度 | m | 14 |
| 锚固点径向间距 | m | 837.6 |
| 导缆孔径向间距 | m | 58 |
| 锚链公称直径 | mm | 185 |
| 系泊线干重线密度 | kg/m | 685 |
| 轴向拉伸刚度 | MN | 3270 |
| 系泊线无张力长度 | m | 850 |
| 导缆孔预张力 | kN | 2,437 |
| 导缆孔与 SWL 夹角 | ˚ | 56.4 |

表 7 系泊线阻力与附加质量系数

| 系泊线系数 | 相对锚链公称直径 | 相对体积等效直径 |
|---|---|---|
| 法向附加质量 | 1 | 0.82 |
| 切向附加质量 | 1 | 0.27 |
| 法向阻力 | 2 | 1.11 |
| 切向阻力 | 1.15 | 0.20 |

锚链尺寸的选取，是为了在正常运行工况下把系统的纵荡-横荡最大偏移控制在 25 m 以内，以免对动态电缆脐带缆的设计造成过多约束。按第 4 节给出的导缆孔峰值张力载荷校核，这套锚链尺寸满足强度要求，但尚未对系泊线做疲劳分析。需要指出的是，本设计所定的锚链尺寸，已经代表了本报告发布时市面上能买到的最大系泊链。受锚链可供尺寸和布放船能力的限制，一台 15-MW 漂浮式海上风机的完整系泊系统设计，实际做出来可能大不一样。要把这个尺度的系泊系统做到最优，很可能还得靠系泊技术的进一步发展，比如采用合成材料。
图 9 系泊系统在惯性坐标系中的布置：俯视图（上）与立视图（下）。图由缅因大学提供

## 2.3 浮式塔架

浮式海上风电机组的塔架要承受平台运动带来的额外惯性载荷和重力载荷，因此刚度要求比固定式机组更高。本半潜式机型的塔架与前面介绍的单桩式机型（Gaertner et al. 2020）分开、单独设计。塔架为各向同性钢管结构，采用风电场一体化系统设计与工程模型（WISDEM®）（National Renewable Energy Laboratory [NREL] 2020a）和 BModes v1.03（Bir 2005）进行设计，边界条件取自由—自由。

塔架设计中最关键的约束是频率。从浮式平台的运行设计载荷工况（DLC）看，平台运动使转子转速的波动明显加大，再加上转子惯量大、最大变桨速率又只有 2°/s，转速更容易超出 5～7.56 rpm 的设计运行范围，欠速和超速的情况随之增多。为避开塔架共振问题，设计时采取保守做法：计入转速波动加大的影响，把塔架一阶前后向和一阶侧向固有频率放在修正后的每转激振频率（1P）和叶片通过频率（3P）范围之外。设计约束运行转速（Ω_const）范围定为 3.97～8.86 rpm。该范围由式（1）和式（2）确定，这两式以风速（U）和全部运行 DLC 中观测到的转速波动的两倍标准差为依据，给出转子转速的下限和上限。1P 与 3P 之间的软—刚区间本来就很窄（见图 10），再计入安全系数后更是所剩无几，因此塔架必须按刚—刚型设计，即一阶固有频率高于 3P。

$$\Omega_{const,min} = \min[\Omega(U) - 2\Omega_{std}(U)] \tag{1}$$

$$\Omega_{const,max} = \max[\Omega(U) + 2\Omega_{std}(U)] \tag{2}$$

图 10 塔架固有频率与激振频率的相对关系

塔架底部高度（15 m）和轮毂高度（150 m）与单桩式机型取相同值，塔架柔性段总长为 129.495 m。设计约束为：最大外径 10 m，塔顶直径 6.5 m，以便与已有的机舱底座设计对接。半潜式机型的塔架刚度更大，质量为 1,263 t，比单桩式机型的塔架重 47%。塔架特性汇总于表 8，钢材材料参数见表 9。

**表 8 浮式塔架特性**

| 参数 | 数值 | 单位 |
|---|---|---|
| 质量 | 1,263 | ton |
| 长度 | 129.495 | m |
| 塔底外径 | 10 | m |
| 塔顶外径 | 6.5 | m |
| 一阶前后向弯曲模态 | 0.496 | Hz |
| 一阶侧向弯曲模态 | 0.483 | Hz |

**表 9 浮式塔架钢材材料参数**

| 参数 | 符号 | 数值 | 单位 |
|---|---|---|---|
| 杨氏模量 | E | 200e11 | Pascals (Pa) |
| 剪切模量 | G | 793e10 | Pa |
| 密度 | ρ | 785e3 | kg/m3 |

塔架尺寸随高度的变化见图 11，并列于表 10。由这些参数可以方便地算出 OpenFAST 等气动弹性建模工具所需的弹性截面特性（见 Gaertner et al. [2020] 附录 B），计算结果同样绘于图 11。

**表 10 塔架尺寸随高度的变化**

| 高度 [m] | 外径 [m] | 壁厚 [mm] |
|---|---|---|
| 15.000 | 10.000 | 82.954 |
| 28.000 | 9.964 | 82.954 |
| 28.001 | 9.964 | 83.073 |
| 41.000 | 9.967 | 83.073 |
| 41.001 | 9.967 | 82.799 |
| 54.000 | 9.927 | 82.799 |
| 54.001 | 9.927 | 29.900 |
| 67.000 | 9.528 | 29.900 |
| 67.001 | 9.528 | 27.842 |
| 80.000 | 9.149 | 27.842 |
| 80.001 | 9.149 | 25.567 |
| 93.000 | 8.945 | 25.567 |
| 93.001 | 8.945 | 22.854 |
| 106.000 | 8.735 | 22.854 |
| 106.001 | 8.735 | 20.250 |
| 119.000 | 8.405 | 20.250 |
| 119.001 | 8.405 | 18.339 |
| 132.000 | 7.321 | 18.339 |
| 132.001 | 7.321 | 21.211 |
| 144.582 | 6.500 | 21.211 |

图 11 塔架结构特性随静水面以上塔架高度的变化

## 2.4 风机控制器

本机型的控制策略与 IEA Wind 15 MW 参考风机单桩式机型相同，只针对浮式平台的动力学特点做了少量调整。控制器仍采用 NREL 开源参考控制器（ROSCO）（NREL 2020b），最小转子转速为 5 rpm，额定转子转速为 7.55 rpm。在区域 2 按设计叶尖速比（TSR = 9.0）运行时，桨距角取 0°。

整定标准桨距控制器和发电机转矩控制器时，我们把桨距控制器的目标阻尼比和固有频率分别改为 1.0 和 0.2 rad/s，转矩控制器的目标阻尼比和固有频率则分别改为 0.85 和 0.12 rad/s。此外，还把塔顶前后向运动乘以一个比例反馈项，叠加到桨距控制器的指令信号上；按 ROSCO 的通用整定逻辑，该项取值为 -9.32196 s。塔顶前后向运动信号先经过一个二阶低通滤波器和一个陷波滤波器：二阶低通滤波器的截止频率取平台纵摇固有频率 0.213 rad/s，阻尼比为 1.0；陷波滤波器的中心频率取塔架前后向固有频率 3.12 rad/s，品质因数为 2.0。

# 3 系统辨识

## 3.1 纵荡—横荡静态偏移

本节给出系统在纵荡—横荡平面内作静态偏移时，导缆孔和锚点处的张力值。图 12 中的导缆孔张力和锚点张力反映了悬链式系泊系统的非线性恢复力特性。OpenFAST 仿真的具体做法是：把平台位移设定在纵荡—横荡平面内的不同位置，并保持平台各自由度不变，再运行 150 s，让系泊缆越过分析开始时的瞬态运动、到达平衡位置。文中给出的导缆孔张力取自每个仿真的最后一个时间步。注意，锚点和导缆孔的编号与图 9 对应。

图 12 导缆孔与锚点张力随纵荡—横荡偏移的变化

## 3.2 刚体自由衰减

我们在 OpenFAST 中对每个刚体自由度都做了自由衰减仿真。衰减试验结果见图 13 至图 16，图中给出了衰减时历曲线以及衰减信号的对数衰减量。可以看出，每个自由度上都体现了第 2.1 节所讨论的二次阻尼模型的影响，这一点从对数衰减量趋势线的斜率就能看出来。仿真取静风环境；仿真中虽然计入了气动阻力，但通过调整叶片方位、使其随衰减运动产生的阻力尽量小，已把气动阻力的影响降到最低。衰减仿真计入了平台、塔架和叶片的全部自由度。系统刚体模态的固有频率汇总于表 11，其值由下图各衰减曲线的平均振荡周期计算得到。

**表 11 刚体固有频率**

| 刚体模态 | 数值 | 单位 |
|---|---|---|
| 纵荡 | 0.007 | Hz |
| 横荡 | 0.007 | Hz |
| 垂荡 | 0.049 | Hz |
| 横摇 | 0.036 | Hz |
| 纵摇 | 0.036 | Hz |
| 艏摇 | 0.011 | Hz |

图 13 静水面处纵荡与横荡自由衰减时历（上）及阻尼比随初始周期幅值的变化（下）
图 14 静水面处垂荡自由衰减时历（上）与阻尼比—初始周期幅值关系（下）

图 15 静水面处横摇与纵摇自由衰减时历（上）与阻尼比—初始周期幅值关系（下）

图 16 静水面处艏摇自由衰减时历（上）与阻尼比—初始周期幅值关系（下）

### 3.3 响应幅值算子（RAO）

本节给出浮式海上风电机组刚体波浪诱导运动的响应幅值算子（Response Amplitude Operator，RAO）分析结果。RAO 通过规则波仿真求得：每组仿真时长 5,000 s，波浪周期从 2.5 s 到 30 s、步长 0.25 s，浪向取 0°（定义见图 2）。本次分析关闭了 OpenFAST 的 AeroDyn 模块，因此不考虑气动载荷的影响；同时锁定与塔架、机舱、轮毂和叶片相关的自由度。计算中取了 2 m 和 8 m 两种波幅，以便考察非线性阻尼效应的影响。从 RAO 幅值响应可以看出，这种效应只在波浪频率与系统某个刚体固有频率接近时才出现。

浪向为 0° 时，只考虑纵荡、垂荡和纵摇三个方向的 RAO，分别见图 17、图 18 和图 19。浮式机组的布置关于 x 轴对称（见图 2），因此浪向为 0° 或 180° 时，横荡、横摇和艏摇方向上的受力关于纵荡-垂荡平面对称，合力或合力矩为零。也就是说，在这一浪向下，横荡、横摇和艏摇三个自由度的 RAO 在所有波浪频率下都等于零。

图 17 静水面处纵荡 RAO 幅值（上）与相位（下）

图 18 静水面处垂荡 RAO 幅值（上）与相位（下）

图 19 静水面处纵摇 RAO 幅值（上）与相位（下）

图 20 风轮-机舱组件（RNA）纵向 RAO 幅值（上）与相位（下）

## 4 系统性能评估

本节从 IEC 设计载荷工况（DLC）中选取了一部分工况，用来考察这台参考浮式海上风电机组在具有代表性的正常和极端设计条件下的性能（IEC 61400-1 [2020]）。OpenFAST 中纳入分析的仿真清单见表 12。选取这些工况时，依据的是同类系统的设计经验，它们代表了浮式机组各个关键部件的控制工况。需要注意，所有工况的风、浪方向都取对齐的 0°（定义见图 2）。各设计工况对应的环境条件代表美国东海岸的海况，按 Stewart et al. (2015) 和 Viselli et al. (2015c) 的定义选取。

这些设计工况下浮式机组的性能，用若干输出量的统计结果来汇总：按加速度分组的结果见图 21，按挠度和位移分组见图 22，按弯矩分组见图 23，按力分组见图 24。下文各图中的标注采用 OpenFAST 输出量的命名，其定义见表 13。从这些结果中可以得到以下几点关键结论：

- 浮式机组的总体性能，通常用平台纵摇角的最大值和风轮-机舱组件（RNA）处观测到的加速度来衡量。由图 21 的加速度结果可见，DLC 6.3 工况中出现的峰值加速度小于 1.5 m/s2；由图 22 可见，平台纵摇角的峰值控制在 6° 以内。
- 由图 22 可见，叶尖最大挠度没有超过 IEA-15-240-RWT 单桩基础设计中所报告的数值（Gaertner et al. 2020）。也就是说，没有出现因平台纵摇角过大而引起的叶片挠度过大的问题。
- 就系泊系统而言，图 22 表明平台的纵荡-横荡偏移量没有超过 25 m，满足前述设计要求；另外，导缆孔张力的峰值小于锚链的破断强度。

表 12 IEC 设计载荷工况矩阵

| DLC | 风况 | 轮毂高度风速 (m/s) | 风向 (°) | 有义波高 (m) | 谱峰周期 (s) | Gamma 形状因子 (-) | 浪向 (°) | 附加设置 | 种子数 | 仿真总数 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.1 | NTM | 4.00 | 0.00 | 1.10 | 8.52 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 6.00 | 0.00 | 1.18 | 8.31 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 8.00 | 0.00 | 1.32 | 8.01 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 10.00 | 0.00 | 1.54 | 7.65 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 12.00 | 0.00 | 1.84 | 7.44 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 14.00 | 0.00 | 2.19 | 7.46 | 1.00 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 16.00 | 0.00 | 2.60 | 7.64 | 1.35 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 18.00 | 0.00 | 3.06 | 8.05 | 1.59 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 20.00 | 0.00 | 3.62 | 8.52 | 1.82 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 22.00 | 0.00 | 4.03 | 8.99 | 1.82 | 0.00 | - | 6 | 6 |
| 1.1 | NTM | 24.00 | 0.00 | 4.52 | 9.45 | 1.89 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 4.00 | 0.00 | 1.10 | 8.52 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 6.00 | 0.00 | 1.18 | 8.31 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 8.00 | 0.00 | 1.32 | 8.01 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 10.00 | 0.00 | 1.54 | 7.65 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 12.00 | 0.00 | 1.84 | 7.44 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 14.00 | 0.00 | 2.19 | 7.46 | 1.00 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 16.00 | 0.00 | 2.60 | 7.64 | 1.35 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 18.00 | 0.00 | 3.06 | 8.05 | 1.59 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 20.00 | 0.00 | 3.62 | 8.52 | 1.82 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 22.00 | 0.00 | 4.03 | 8.99 | 1.82 | 0.00 | - | 6 | 6 |
| 1.3 | ETM | 24.00 | 0.00 | 4.52 | 9.45 | 1.89 | 0.00 | - | 6 | 6 |
| 1.4 | ECD+/-R-2.0 | 8.00 | 0.00 | 1.32 | 8.01 | 1.00 | 0.00 | 风向变化 +/- | 1 | 2 |
| 1.4 | ECD+/-R | 10.00 | 0.00 | 1.54 | 7.65 | 1.00 | 0.00 | 风向变化 +/- | 1 | 2 |
| 1.4 | ECD+/-R+2.0 | 12.00 | 0.00 | 1.84 | 7.44 | 1.00 | 0.00 | 风向变化 +/- | 1 | 2 |
| 1.6 | NTM | 4.00 | 0.00 | 6.30 | 11.50 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 6.00 | 0.00 | 8.00 | 12.70 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 8.00 | 0.00 | 8.00 | 12.70 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 10.00 | 0.00 | 8.10 | 12.80 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 12.00 | 0.00 | 8.50 | 13.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 14.00 | 0.00 | 8.50 | 13.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 16.00 | 0.00 | 9.80 | 14.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 18.00 | 0.00 | 9.80 | 14.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 20.00 | 0.00 | 9.80 | 14.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 22.00 | 0.00 | 9.80 | 14.10 | 2.75 | 0.00 | - | 6 | 6 |
| 1.6 | NTM | 24.00 | 0.00 | 9.80 | 14.10 | 2.75 | 0.00 | - | 6 | 6 |
| 6.1 | EWM 50 年一遇 | 47.50 | 0.00 | 10.70 | 14.20 | 2.75 | 0.00 | 偏航 +/- 8° | 6 | 12 |
| 6.3 | EWM 1 年一遇 | 38.00 | 0.00 | 6.98 | 11.70 | 2.75 | 0.00 | 偏航 +/- 20° | 6 | 12 |

NTM：正常湍流模型；ETM：极端湍流模型；ECD：带风向变化的极端相干阵风；EWM：极端风速模型。

表 13 OpenFAST 输出量定义

| OpenFAST 输出量名称 | 说明 |
|---|---|
| RootMxb1 | 叶片 1 叶根摆振弯矩（即由摆振方向的力引起的弯矩） |
| RootMyb1 | 叶片 1 叶根挥舞弯矩（即由挥舞方向的力引起的弯矩） |
| TipDxb1 | 叶片 1 挥舞方向叶尖挠度（相对于变桨轴） |
| TipDyb1 | 叶片 1 摆振方向叶尖挠度（相对于变桨轴） |
| NcIMUTAxs | 机舱惯性测量单元 x 方向平动加速度（绝对值） |
| NcIMUTAys | 机舱惯性测量单元 y 方向平动加速度（绝对值） |
| NcIMUTAzs | 机舱惯性测量单元 z 方向平动加速度（绝对值） |
| YawBrTDxt | 塔顶/偏航轴承纵向（平动）挠度（相对于未变形位置） |
| YawBrTDyt | 塔顶/偏航轴承横向（平动）挠度（相对于未变形位置） |
| TwrBsMxt | 塔底横摇（即横向）弯矩（即由横向力引起的弯矩） |
| TwrBsMyt | 塔底纵摇（即纵向）弯矩（即由纵向力引起的弯矩） |
| PtfmSurge | 平台纵荡（平动）位移 |
| PtfmHeave | 平台垂荡（平动）位移 |
| PtfmPitch | 平台纵摇（转动）倾角位移 |
| FAIRTEN1 | 第 1 根系泊缆的导缆孔张力 |
| FAIRTEN2 | 第 2 根系泊缆的导缆孔张力 |
| FAIRTEN3 | 第 3 根系泊缆的导缆孔张力 |
| ANCHTEN1 | 第 1 根系泊缆的锚点张力 |
| ANCHTEN2 | 第 2 根系泊缆的锚点张力 |
| ANCHTEN3 | 第 3 根系泊缆的锚点张力 |
图 21 各设计载荷工况（DLC）下的加速度统计（m/s2）

图 22 各设计载荷工况下的挠度与位移统计（m 或 ˚）

图 23 各设计载荷工况下的弯矩统计（kN-m）

图 24 各设计载荷工况下的力统计（N）

## 参考文献

Bir, G. 2005. User's Guide to BModes (Technical Report). Golden, CO: National Renewable Energy Laboratory. NREL/TP-500-39133. https://www.nrel.gov/docs/fy06osti/39133.pdf.

Chakrabarti, S. 2005. Handbook of Offshore Engineering. Oxford, UK: Elsevier Ltd.

Coulling, A. J., A. J. Goupee, A. N. Roberston, J. M. Jonkman, H. J. Dagher. 2013. "Validation of a FAST semi-submersible floating wind turbine numerical model with DeepCWind test data." Journal of Renewable and Sustainable Energy. https://aip.scitation.org/doi/10.1063/1.4796197.

Det Norske Veritas. 2010. Recommended Practice DNV-RP-C205. Environmental Conditions and Environmental Loads. https://rules.dnvgl.com/docs/pdf/dnv/codes/docs/2010-10/rp-c205.pdf.

DNV-GL. 2018 Offshore Standards; DNVGL-OS-E301: Position Mooring. http://rules.dnvgl.com/docs/pdf/dnvgl/os/2018-07/dnvgl-os-e301.pdf.

Duarte, T., A. Sarmento, M. Alves, J. Jonkman. 2013. "State-Space Realization of the Wave-Radiation Force within FAST." Presented at the ASME 2013 32nd International Conference on Ocean, Offshore and Artic Engineering, Nantes, France, June 9–14, 2013. Golden, CO: National Renewable Energy Laboratory. NREL/CP-5000-58099. https://www.nrel.gov/docs/fy13osti/58099.pdf.

Gaertner, E., J. Rinker, L. Sethuraman, F. Zahle, B. Anderson, G. Barter, N. Abbas, F. Meng, P. Bortolotti, W. Skrzypinski, G. Scott, R. Feil, H. Bredmose, K. Dykes, M. Shields, C. Allen, A. Viselli. 2020. IEA Wind TCP Task 37: Definition of the IEA Wind 15-Megawatt Offshore Reference Wind Turbine (Technical Report). Golden, CO: National Renewable Energy Laboratory. NREL/TP-5000-75698. https://www.nrel.gov/docs/fy20osti/75698.pdf.

Greenshields, C. J. 2011. "OpenFoam: Open Source CFD: Documentation." OpenFOAM Foundation Ltd. https://www.openfoam.com/documentation/. Accessed June 11, 2020.

Hall, M., and A. Goupee. 2015. "Validation of a lumped-mass mooring line model with DeepCwind semisubmersible test data." Ocean Engineering, Vol. 104, pp. 590-603. https://doi.org/10.1016/j.oceaneng.2015.05.035. https://www.sciencedirect.com/science/article/pii/S0029801815002279?via%3Dihub.

International Electrotechnical Commission (IEC). 2005. IEC 61400-1: Wind Tubines - Part 1: Design Requirements, 3rd Edition.

Jonkman, J. M., A. N. Robertson, and G. J. Hayman. Forthcoming. "HydroDyn User's Guide and Theory Manual." Golden, CO: National Renewable Energy Laboratory.

Lee, C. H. 1995. WAMIT Theory Manual. Massachusetts Institute of Technology, Department of Ocean Engineering, Cambridge, Massachusetts.

Musial, W., P. Beiter, P. Spitsen, J. Nunemaker, V. Gevorgian. 2018 Offshore Wind Technologies Market Report. U.S. Department of Energy, Office of Scientific and Technical Information, Oak Ridge, TN. https://www.energy.gov/sites/prod/files/2019/09/f66/2018%20Offshore%20Wind%20Technologies%20Market%20Report.pdf.

National Renewable Energy Laboratory (NREL). 2020a. Wind Plant Integrated System Design and Engineering Model (WISDEM), https://github.com/WISDEM/WISDEM. Accessed June 11, 2020.

NREL. 2020b. Reference OpenSource Controller (ROSCO) for wind turbine applications, https://github.com/NREL/rosco. Accessed 6/11/2020.

Robertson, A., J. Jonkman, M. Masciola, A. Goupee, A. Coulling, C. Luan. 2014. Definition of the Semisubmersible Floating System for Phase II of OC4 (Technical Report). Golden, CO: National Renewable Energy Laboratory. NREL/TP-5000-60601. https://www.nrel.gov/docs/fy14osti/60601.pdf.

Schwartz, Marc, Donna Heimiller, Steve Haymes, Walt Musial. 2010. Assessment of Offshore Wind Energy Resources for the United States (Technical Report). Golden, CO: National Renewable Energy Laboratory. NREL/TP-500-45889. https://www.nrel.gov/docs/fy10osti/45889.pdf.

Stewart, G. M., A. Roberston, J. Jonkman, M. A. Lackner. 2015. "The creation of a comprehensive metocean data set for offshore wind turbine simulations." Wind Energy, pp. 1151-1159. https://doi.org/10.1002/we.1881. https://onlinelibrary.wiley.com/doi/full/10.1002/we.1881.

Viselli, Anthony, H. J. Dagher, and Andrew Goupee. 2014. "Volturnus 1:8 – Design and testing of the first grid-connected offshore wind turbine in the U.S.A." in 19th Offshore Symposium Sponsored by the Texas Section of SNAME, Houston, TX, 2014. https://www.onepetro.org/conference-paper/SNAME-TOS-2014-015?sort=&start=0&q=Design+and+testing+of+the+first+grid-connected+offshore+wind+turbine+in+the&from_year=&peer_reviewed=&published_between=&fromSearchResults=true&to_year=&rows=25#

Viselli, Anthony M., Andrew J. Goupee, and Habib J. Dagher. 2015a. "Model Test of a 1:8-Scale Floating Wind Turbine in the Gulf of Maine." Offshore Mech. Arct. Eng. 137(4): 041901. https://doi.org/10.1115/1.4030381.

Viselli, Anthony M., Andrew J. Goupee, Habib J. Dagher, and Christopher K. Allen. 2015b. "Design and model confirmation of the intermediate scale VolturnUS floating wind turbine subjected to its extreme design conditions offshore Maine." Wind Energy. Vol. 19, pp. 1161-1177. https://doi.org/10.1002/we.1886.

Viselli, A. G. Z. Forristall, B. R. Pearce and H. J. Dagher. 2015c. "Estimation of extreme wave and wind design parameters for offshore wind turbines in the Gulf of Maine using a POT method." Ocean Engineering, vol. 104, pp. 649-658. https://doi.org/10.1016/j.oceaneng.2015.04.086.
