# IEA Wind 15 MW 海上参考风机的定义

2020 年 3 月

IEA Wind TCP Task 37

技术报告

Evan Gaertner¹, Jennifer Rinker², Latha Sethuraman¹, Frederik Zahle², Benjamin Anderson¹, Garrett Barter¹, Nikhar Abbas¹, Fanzhong Meng², Pietro Bortolotti¹, Witold Skrzypiński², George Scott¹, Roland Feil¹, Henrik Bredmose², Katherine Dykes², Matt Shields¹, Christopher Allen³, and Anthony Viselli³

1 National Renewable Energy Laboratory
2 Technical University of Denmark
3 University of Maine

建议引用格式

Gaertner, Evan, Jennifer Rinker, Latha Sethuraman, Frederik Zahle, Benjamin Anderson, Garrett Barter, Nikhar Abbas, Fanzhong Meng, Pietro Bortolotti, Witold Skrzypiński, George Scott, Roland Feil, Henrik Bredmose, Katherine Dykes, Matt Shields, Christopher Allen, and Anthony Viselli. 2020. Definition of the IEA 15-Megawatt Offshore Reference Wind. Golden, CO: National Renewable Energy Laboratory. NREL/TP-5000-75698. https://www.nrel.gov/docs/fy20osti/75698.pdf

NREL 是美国能源部能源效率与可再生能源办公室下属的国家实验室，由 Alliance for Sustainable Energy, LLC 运营。

技术报告
NREL/TP-5000-75698
2020 年 3 月

National Renewable Energy Laboratory
15013 Denver West Parkway
Golden, CO 80401
合同号 DE-AC36-08GO28308
303-275-3000 • www.nrel.gov

## 说明

本工作部分由美国国家可再生能源实验室（National Renewable Energy Laboratory, NREL）完成。该实验室由 Alliance for Sustainable Energy, LLC 为美国能源部（DOE）运营，合同号 DE-AC36-08GO28308。经费由美国能源部能源效率与可再生能源办公室下属的风能与水电技术办公室提供。本文所表达的观点不一定代表 DOE 或美国政府的观点。

本报告可在美国国家可再生能源实验室（NREL）网站 www.nrel.gov/publications 免费获取。

1991 年之后出版的美国能源部（DOE）报告，以及越来越多的 1991 年之前文献，可通过 www.OSTI.gov 免费获取。

NREL 采用含回收成分的纸张印刷。

## 致谢

美国国家可再生能源实验室（NREL）和丹麦技术大学（DTU）的工作人员通过国际能源署（IEA）Wind Task 37（风能系统工程）密切合作，共同设计了本报告所述的参考风机。缅因大学（UMaine）的作者发挥其专业优势和资源条件，贡献了浮式半潜平台的设计。为更清楚地呈现每位作者的贡献，也为今后的咨询提供依据，下表列出了所有作者的分工。

| 姓名 | 机构 | 贡献 |
|---|---|---|
| Evan Gaertner | NREL | 首席设计工程师，主导叶片、塔架和单桩设计 |
| Jennifer Rinker | DTU | HAWC2 负责人，设计载荷基础，控制器整定 |
| Latha Sethuraman | NREL | 负责永磁直驱发电机、传动链、机架、机舱及其他子系统的设计 |
| Frederik Zahle | DTU | 弯扭耦合方面的贡献，风轮与叶片设计评审 |
| Benjamin Anderson | NREL | 绘制机舱 CAD 模型，完成传动链和机架分析 |
| Garrett Barter | NREL | 项目首席研究员 |
| Nikhar Abbas | NREL | Reference OpenSource Controller 负责人与整定 |
| Fanzhong Meng | DTU | 控制器负责人与整定 |
| Pietro Bortolotti | NREL | 叶片设计支持 |
| Witold Skrzypiński | DTU | 叶片设计工具开发 |
| George Scott | NREL | 传动链设计支持 |
| Roland Feil | NREL | 叶片结构详细分析 |
| Henrik Bredmose | DTU | COREWIND 项目首席研究员 |
| Katherine Dykes | DTU | 综合支持 |
| Matt Shields | NREL | 单桩与过渡段设计支持，报告编辑 |
| Christopher Allen | UMaine | 半潜式平台首席设计工程师 |
| Anthony Viselli | UMaine | 半潜式平台首席研究员 |

除 IEA Wind 促成 NREL、DTU 和 UMaine 三方合作之外，我们还借助了各位工作人员更广泛的人脉网络以及 IEA Wind Task 37 这一平台，确保本设计对行业技术水平给出偏保守的估计。这些行业联系人提供了宝贵信息，帮助我们校准设计假设和输入取值。没有他们的投入，这台 15 MW 参考风机不会有如此专业的设计，也不会对业界同行有这么大的参考价值。以下排名不分先后，向下列公司和个人表示感谢：

- General Electric: Anna Diedrichkeit, Albert Fiass, Vanita Mani, Priyan Subramanian, David Torrey, Yogen Utturkar
- EDF Renewables: Julien Simon
- Senvion: Fabian Vorpahl
- Sintef: Karl Merz
- Atkins: Ikpoto Udoh
- NREL: Walt Musial, Jason Jonkman, Nicole Mendoza
- Sandia National Laboratories: Ernesto Camarena

NREL 的工作由美国能源部能源效率与可再生能源办公室风能技术办公室资助，项目经理为 Patrick Gilman。DTU 的研究由欧盟 H2020 计划资助，授权协议号 815083 - COREWIND。

## 术语表

### 缩略语

| 缩略语 | 全称 |
|---|---|
| 3D | 三维（three-dimensional） |
| BECAS | BEam Cross section Analysis Software（梁截面分析软件） |
| DLC | 设计载荷工况（design load case） |
| DTU | 丹麦技术大学（Technical University of Denmark） |
| HAWTOpt2 | Horizontal Axis Wind Turbine Optimization 2nd generation（第二代水平轴风机优化工具） |
| HAWC2 | Horizontal Axis Wind turbine simulation Code 2nd generation（第二代水平轴风机仿真程序） |
| IEC | 国际电工委员会（International Electrotechnical Commission） |
| IEA | 国际能源署（International Energy Agency） |
| metocean | 海洋气象（meteorological ocean） |
| NREL | 美国国家可再生能源实验室（National Renewable Energy Laboratory） |
| NdFeB | 钕（neodymium） |
| PSD | 功率谱密度（power spectral density） |
| PI | 比例积分（proportional integral） |
| ROSCO | Reference OpenSource Controller（参考开源控制器） |
| RMS | 均方根（root mean squared） |
| SRB | 球面滚子轴承（spherical roller bearing） |
| SST | 剪切应力输运（shear stress transport） |
| TDO | 锥形双外圈（tapered double outer） |
| TSR | 叶尖速比（tip-speed ratio） |
| UMaine | 缅因大学（University of Maine） |
| WindPACT | Wind Partnership for Advanced Component Technology |
| WISDEM® | Wind-Plant Integrated System Design Engineering Model |
| WP | 工作包（work package） |

### 单位

| 符号 | 名称 |
|---|---|
| A | 安培 |
| h | 小时 |
| Hz | 赫兹 |
| kg | 千克 |
| m | 米 |
| min | 分钟 |
| N (kgm/s2) | 牛顿 |
| rad | 弧度 |
| rpm | 转每分钟 |
| P | 周期 |
| Pa (N/m2) | 帕斯卡 |
| s | 秒 |
| t | 公吨 |
| T | 特斯拉 |
| V | 伏特 |
| W | 瓦特 |

### 词头

| 词头 | 含义 |
|---|---|
| m | 毫 |
| k | 千 |
| M | 兆 |
| G | 吉 |

## 执行摘要

### 概述与动机

参考风机在风电行业中扮演着多重角色，近年来重要性日益凸显。第一，参考风机是公开的对标基准，设计参数全部公开，可作为基线，供探索新技术或新设计方法的研究使用。第二，作为开放设计，参考风机为工业界与外部研究人员之间的协作搭建了平台。第三，参考风机也是风电新人的入门和教学平台，帮助他们理解基本的设计要素和系统层面的权衡取舍。

就固定式基础海上风电而言，2018 年欧洲投运机组的平均单机容量为 6.8 MW [1]；GE 的 12 MW Haliade-X 海上风机将于 2021 年推向市场，其风轮直径为 218 m，采用直驱构型。新的参考风机要想在当前乃至今后几年都保持参考价值，就必须领先于当前一代工业机组，但步子又不能迈得太大，以免需要激进的技术创新。因此，需要一台容量在 10 MW 以上 [2]、20 MW 以下 [3] 的参考风机：沿 GE Haliade-X 相同的增长趋势，采用类似的传动链构型和比功率。

本报告介绍一台 15 MW 海上风机，采用固定式单桩支撑结构。该参考风机为 IEC IB 类直驱机型，风轮直径 240 m，轮毂高度 150 m。图 ES-1 和表 ES-1 给出了该设计的概览。这一设计是美国国家可再生能源实验室（NREL，由美国能源部资助）与丹麦技术大学（DTU，由欧盟 H2020 计划资助）的联合成果，依托 IEA Wind Task 37（风能系统工程：综合研发与示范）的第二个工作包开展。缅因大学（UMaine）研制的半潜式浮式支撑结构将在后续报告中详细介绍。

### 叶片与风轮特性

风轮构型的顶层决策来自与行业伙伴的讨论，目标是确定下一代风机在技术上可行的方案。叶片设计主要由两个参数决定：选定的风轮直径 240 m，以及最大叶尖速度 95 m/s。叶片采用较为传统的结构构型：两根碳纤维增强的主梁承担主要载荷，由两道腹板连接，前缘和后缘局部加强，内部填充泡沫。翼型选用 DTU FFA-W3 系列，因为该系列的极曲线和几何数据均为公开数据。叶片的弦长、扭角、翼型布置、叶尖速比和主梁厚度均通过一次设计优化研究确定。表 ES-2 汇总了叶片的关键特征，包括设计功率系数 CP 为 0.489、叶片质量 65 t。

### 塔架与单桩特性

塔架和单桩按各向同性钢管设计。频率约束在很大程度上主导了这部分设计：塔架—单桩的一阶模态频率为 0.17 Hz，在所有风速下都位于叶片通过频率 1P 和 3P 之间。这也足以避开东海岸通用场址波浪能量最集中的频率范围（0.10 Hz 至 0.13 Hz）。塔架高度按轮毂高度达到 150 m 来选取，这样当叶片长达 120 m 时，叶尖距地面（水面）仍有 30 m 的净空。单桩基础外径为 10 m，已接近当前制造和安装技术的极限；壁厚沿高度变化，从桩身的 55 mm 到过渡段处的 44 mm。

### 机舱与传动链特性

15 MW 参考风机采用直驱构型，配一台永磁同步径向磁通外转子发电机，机舱布置简单紧凑。图 ES-2a 给出了一种简单的直驱机舱布置，采用外转子永磁发电机。该总成由一根轮毂轴构成，轮毂轴支撑着整台风机

表 ES-1 IEA Wind 15 MW 风机关键参数

| 参数 | 单位 | 值 |
|---|---|---|
| 额定功率 | MW | 15 |
| 机型等级 | - | IEC Class 1B |
| 比功率 | W/m2 | 332 |
| 风轮朝向 | - | Upwind |
| 叶片数 | - | 3 |
| 控制方式 | - | Variable speed, Collective pitch |
| 切入风速 | m/s | 3 |
| 额定风速 | m/s | 10.59 |
| 切出风速 | m/s | 25 |
| 设计叶尖速比 | - | 90 |
| 最低风轮转速 | rpm | 5.0 |
| 最高风轮转速 | rpm | 7.56 |
| 最大叶尖速度 | m/s | 95 |
| 风轮直径 | m | 240 |
| 翼型系列 | - | FFA-W3 |
| 轮毂高度 | m | 150 |
| 轮毂直径 | m | 7.94 |
| 轮毂悬垂距 | m | 11.35 |
| 风轮锥角 | deg | -4.0 |
| 叶片预弯 | m | 4 |
| 叶片质量 | t | 65 |
| 传动链 | - | Direct drive |
| 主轴倾角 | deg | 6 |
| 风轮—机舱总成质量 | t | 1,017 |
| 过渡段高度 | m | 15 |
| 单桩入泥深度 | m | 45 |
| 单桩底部直径 | m | 10 |
| 塔架质量 | t | 860 |
| 单桩质量 | t | 1,318 |

注：deg 为度，m 为米，m/s 为米每秒，rpm 为转每分钟，t 为公吨，W/m2 为瓦每平方米。
图 ES-1 IEA Wind 15 MW 参考风机

发电机转子装在两个主轴承上，主轴承由一个固定回转支座支承，回转支座自底板悬臂伸出。轮毂是一个简单的球形壳体，上面开有叶片安装口和法兰口。主轴截面为空心圆柱，壁厚恒定，倾角为 6°。主轴连同风轮一起由两个主轴承支承。两个主轴承都是外圈旋转、内圈固定。外圈和轴承座装在由底板支承的回转支座上。风轮、发电机转子以及轮毂的全部重量载荷，都经主轴、通过轴承传递到回转支座上。底板是一根空心的椭圆曲面悬臂梁，截面为圆形。偏航系统轴承采用双列角接触球轴承。

发电机采用外转子径向磁通结构，永磁体表贴在转子表面（见图 ES-2b）。外转子方案结构简单坚固、制造方便、端部绕组短，而且绕组与齿部之间的散热条件比内转子方案更好。定子采用分数槽、双层集中绕组布局，可以把基波绕组因数做到最大。

**表 ES-2 叶片参数**

| 说明 | 值 | 单位 |
|---|---|---|
| 叶片长度 | 117 | m |
| 叶根直径 | 5.20 | m |
| 叶根圆柱段长度 | 2.34 | m |
| 最大弦长 | 5.77 | m |
| 最大弦长的展向位置 | 27.2 | m |
| 叶尖预弯 | 4.00 | m |
| 预锥角 | 4.00 | deg |
| 叶片质量 | 65,250 | kg |
| 叶片质心位置 | 26.8 | m |
| 设计叶尖速比 | 9.00 | - |
| 一阶挥舞固有频率 | 0.555 | Hz |
| 一阶摆振固有频率 | 0.642 | Hz |
| 设计 CP | 0.489 | - |
| 设计 CT | 0.799 | - |
| 年发电量 | 77.4 | GWh |

单位缩写：deg 度；kg 千克；GWh 吉瓦时；m 米；Hz 赫兹。

图 ES-2 15 MW 直驱风电机组机舱布置示意图与 CAD 模型，未按比例绘制，部分结构细节已省略。叶片（图中未画出）、轮毂、主轴和发电机转子一起旋转。

**载荷分析**

本报告设定了一个美国东海岸的通用场址，风速服从 Weibull 分布，平均风速约 8.65 m/s，形状参数 2.12。在这个平均风速下，对应的有效波高约 1.4 m，谱峰周期 7.9 秒（s）。本报告给出的固定式单桩支撑结构按 30 m 水深设计。

本报告按国际电工委员会（IEC）的设计载荷工况 [4] 做了一轮分析，目的是找出对关键设计约束部件最不利的极限载荷。结果表明：极端风速下的偏航误差停机工况，以及带风向变化的极端相干阵风工况，是本设计的最不利载荷工况。最不利情况下叶尖面外挠度为 22.8 m，塔架净空绰绰有余——叶片不变形时叶尖到塔架的间隙为 30.0 m。这个裕度说明叶片设计偏保守，后续还可以做气动弹性优化，在保持推荐安全裕度的前提下进一步提升气动性能或降低度电成本。需要指出的是，本次没有对叶片做完整的疲劳分析；对这种超大叶片来说，摆振方向的叶根弯矩在疲劳上可能会成为问题。

**模型获取**

为促进后续合作，这台参考风机的设计成果以多种分析工具的输入文件形式向整个风电行业开放，包括 OpenFAST、HAWC2、风电场一体化系统设计与工程模型（WISDEM）和 HawtOpt2。文件托管在 GitHub 上，地址为 github.com/IEAWindTask37/IEA-15-240-RWT。希望行业同行把各自的设计变体也提交回这个仓库，共同充实这项工作。

# 目录

执行摘要 …… iii

1 引言 …… 4
- 1.1 参考风机的作用 …… 4
- 1.2 整机总体参数 …… 4
- 1.3 设计工具与方法 …… 4
- 1.4 模型获取 …… 7
- 1.5 气象海洋环境 …… 7

2 叶片参数 …… 8
- 2.1 叶片气动参数 …… 8
- 2.2 叶片结构参数 …… 9

3 风轮性能 …… 17
- 3.1 控制器参数 …… 17
- 3.2 稳态性能 …… 18

4 塔架与单桩参数 …… 21

5 机舱、传动链与轮毂 …… 25
- 5.1 机舱概述 …… 25
- 5.2 轮毂 …… 25
- 5.3 主轴、轴承与回转支座 …… 26
- 5.4 底板 …… 27
- 5.5 偏航系统 …… 27
- 5.6 直驱发电机 …… 29
- 5.7 机舱阻尼 …… 29

6 载荷评估 …… 32
- 6.1 结论 …… 34

参考文献 …… 35

附录 …… 37

A 叶片截面 …… 37

B 塔架与土壤建模 …… 41
- B.1 塔架数据 …… 41
- B.2 土壤模型 …… 44

# 插图目录

图 ES-1 IEA Wind 15 MW 参考风机 …… v

图 ES-2 15 MW 直驱风电机组机舱布置示意图与 CAD 模型。未按比例绘制，部分结构细节已省略。叶片（图中未画出）、轮毂、主轴和发电机转子一起旋转 …… vi

图 1-1 IEA Wind 15 MW 参考风机 …… 6

图 2-1 海上风机叶片的吸力面视图（上）和后缘视图（下） …… 8

图 2-2 IEA Wind 15 MW 叶片设计采用的 DTU FFA-W3 翼型族 …… 9

图 2-3 叶片所用翼型的气动极曲线 …… 10

图 2-4 叶片平面形状的展向分布量 …… 11

图 2-5 叶片放样外形 …… 12

图 2-6 70% 展长处的叶片截面 …… 12

图 2-7 IEA 风机本体复合材料定义示意图（从叶根到叶尖） …… 13

图 2-8 不同展向位置处，铺层厚度沿翼型归一化 s 坐标的分布 …… 14

图 2-9 不同展向位置处的剪切铺层厚度 …… 15

图 2-10 用 PreComp 计算的叶片梁结构参数沿展向叶片曲线位置的变化 …… 16

图 2-11 叶片平面形状与结构参数 …… 16

图 3-1 OpenFAST 叶素动量法算出的 15 MW 风轮性能，以及 ROSCO 控制器下的运行情况 …… 19

图 3-2 CCBlade 稳态叶素动量法气动功率与推力系数曲面（随桨距角和叶尖速比变化） …… 20

图 3-3 叶片展向力随风速的变化 …… 20

图 4-1 塔架固有频率与激励频率归一化功率谱密度（PSD）的关系 …… 21

图 4-2 塔架外径与壁厚 …… 22

图 4-3 塔架与单桩的截面参数 …… 22

图 5-1 15 MW 直驱风电机组机舱布置示意图与 CAD 模型。未按比例绘制，部分结构细节已省略。叶片（图中未画出）、轮毂、主轴和发电机转子一起旋转 …… 25

图 5-2 CAD 示意图：(a) 主轴，(b) 回转支座（也称机头）；尺寸见表 5-2 …… 26

图 5-3 底板 CAD 示意图 …… 28

图 5-4 外转子直驱发电机的 CAD 示意图，含电磁与结构设计参数 …… 30

图 6-1 各设计载荷工况下叶根与塔底最大弯矩的排序 …… 33

图 6-2 各设计载荷工况下叶尖与塔顶最大挠度的排序 …… 33

图 A-1 0% 展长处的叶片截面 …… 37

图 A-2 10% 展长处的叶片截面 …… 37

图 A-3 20% 展长处的叶片截面 …… 38

图 A-4 30% 展长处的叶片截面 …… 38

图 A-5 40% 展长处的叶片截面 …… 38

图 A-6 50% 展长处的叶片截面 …… 39

图 A-7 60% 展长处的叶片截面 …… 39

图 A-8 80% 展长处的叶片截面 …… 39

图 A-9 90% 展长处的叶片截面 …… 40

图 A-10 100% 展长处的叶片截面 …… 40

# 表格目录

表 ES-1 IEA Wind 15 MW 风机关键参数 …… iv

表 ES-2 叶片参数 …… vi

表 1-1 IEA Wind 15 MW 风机关键参数（与 DTU 10 MW 风机对比） …… 5

表 1-2 IEA Wind 15 MW 参考风机设计与分析所用模型 …… 7

表 2-1 叶片参数 …… 8

表 4-1 塔架材料参数 …… 21

表 4-2 塔架与基础的若干关键参数和尺寸 …… 23

表 5-1 机舱总成的集中质量与转动惯量 …… 26

表 5-2 主轴尺寸、轴承及定型所用载荷 …… 27

表 5-3 底板参数 …… 28

表 5-4 15 MW 直驱发电机的电磁与结构设计 …… 31

表 6-1 IEC 设计载荷工况设置汇总 …… 32

表 6-2 设计载荷工况分析所用的气象海洋条件 …… 32

# 1 引言

## 1.1 参考风机的作用

参考风机在风电行业里有多种用途，近年来重要性越来越高。第一，它是一个公开的基准机型，设计参数全部对外公布，可以作为基线，用来研究新技术或新设计方法。一直以来，参考风机的定位都是"真实但没有完全优化"的设计，方便风电界的同行在此基础上更新和改进。第二，作为一个开放设计，参考风机让企业和外部研究人员之间能开展合作：企业用参考风机做先进技术开发，既能和外部人员协作，又不用暴露自己的知识产权。第三，参考风机是风电新人入门的学习平台，可以借此理解风机设计的基本要素和系统层面的权衡取舍。

参考风机的历史可以追溯到 21 世纪初美国国家可再生能源实验室（NREL）的先进部件技术风电合作计划（WindPACT）系列机型，包括 0.75 MW、1.5 MW 和 3 MW 三种机型 [5]。不过这批机型的使用范围只限于美国的国家实验室。第一台被国际同行广泛采用的参考风机是 NREL 5 MW 风机 [6]，至今仍有大量研究人员在使用。后来，丹麦技术大学（DTU）又开发了一台面向海上风电的 10 MW 风机 [7]。除这两台之外，还有其他一些参考风机，比如欧盟 FP7 项目 LEANWIND 的 8 MW 风机 [8]、桑迪亚国家实验室的 100 m 叶片研究 [9]，以及 INNWIND 项目中一台 20 MW 风机的概念研究 [3]。最近，负责本项工作的 IEA Wind Task 37 还发布了现代化的 3.35 MW 陆上和 10 MW 海上参考风机 [2]。这批设计接连快速发布，背后是整个行业在快速放大机组的功率等级和尺寸。以海上固定式风电为例，2018 年欧洲投运机组的平均容量为 6.8 MW [1]；GE 的 12 MW Haliade-X 海上风机将于 2021 年推向市场，风轮直径 218 m，采用直驱构型。

一台新的参考风机要想在当下和未来几年里保持相关性，就必须领先当前一代工业机型，但又不能领先太多、以至于要用上激进的新技术。现有的参考风机阵容已经不能完全满足研究界和工业界的需求——叶片尺度放大、浮式基础设计、风电场控制、物流研究等很多课题都需要新的基准机型。因此，现在需要一台 10 MW 以上、20 MW 以下的参考风机：沿着 GE Haliade-X 的同一条增长路线走，采用类似的传动链构型和比功率。

这正是本报告介绍的 IEA Wind 15 MW 参考风机的设计出发点。这台参考风机（见图 1-1）是一台 IB 类直驱机组，风轮直径 240 m，轮毂高度 150 m。设计工作由 NREL（受美国能源部资助）和 DTU（受欧盟 H2020 计划资助）联合完成，属于 IEA Wind Task 37 第二工作包"风能系统工程：一体化研发"的成果。本报告介绍的是海上固定式单桩支撑结构；与缅因大学（UMaine）合作开发的半潜式浮式支撑结构，将在后续报告中单独介绍。

## 1.2 整机总体参数

整机的总体参数见表 1-1。表中同时列出了 DTU 10 MW 参考风机 [7] 的数据，供对比参考。

## 1.3 设计工具与方法

IEA Wind 15 MW 参考风机由 NREL、DTU 和 UMaine 联合设计。本次工作所用的分析与设计工具列在表 1-2 中。后面各节讨论设计细节时，会频繁出现这些模型的名称。
**表 1-1 IEA Wind 15-MW 风机与 DTU 10-MW 风机关键参数对比**

| 参数 | 单位 | DTU 10-MW 风机 | IEA Wind 15-MW 风机 |
|---|---|---|---|
| 额定功率 | MW | 10 | 15 |
| 风机等级 | - | IEC Class 1B | IEC Class 1B |
| 比功率 | W/m2 | 401 | 332 |
| 风轮布置 | - | 上风向 | 上风向 |
| 叶片数量 | - | 3 | 3 |
| 控制方式 | - | 变速、集体变桨 | 变速、集体变桨 |
| 切入风速 | m/s | 4 | 3 |
| 额定风速 | m/s | 11.4 | 10.59 |
| 切出风速 | m/s | 25 | 25 |
| 风轮直径 | m | 178.3 | 240 |
| 翼型系列 | - | FFA-W3 | FFA-W3 |
| 轮毂高度 | m | 119 | 150 |
| 轮毂直径 | m | 5.6 | 7.94 |
| 轮毂悬垂距离 | m | 7.1 | 11.35 |
| 传动链 | - | 中速、多级齿轮箱 | 低速、直驱 |
| 设计叶尖速比 | - | 7.5 | 9.0 |
| 最小风轮转速 | rpm | 6.0 | 5.0 |
| 最大风轮转速 | rpm | 9.6 | 7.56 |
| 最大叶尖速度 | m/s | 90 | 95 |
| 齿轮箱速比 | - | 50 | — |
| 主轴倾角 | deg | 5 | 6 |
| 风轮预锥角 | deg | -2.5 | -4.0 |
| 叶片预弯 | m | 3.332 | 4 |
| 叶片质量 | t | 41 | 65 |
| 风轮-机舱总成质量 | t | 674 | 1,017 |
| 塔架质量 | t | 987 | 860 |
| 塔架底部直径 | m | 8 | 10 |
| 过渡段高度 | m | 10 | 15 |
| 单桩埋深 | m | 42.6 | 45 |
| 单桩底部直径 | m | 9 | 10 |
| 单桩质量 | t | 2,044 | 1,318 |

deg 度；rpm 转/分；m 米；t 吨；m/s 米/秒；W/m2 瓦/平方米；MW 兆瓦

图 1-1 IEA Wind 15-MW 参考风机

**表 1-2 IEA Wind 15-MW 参考风机设计与分析所用模型**

| 用途 | NREL 工具链 | DTU 工具链 |
|---|---|---|
| 系统设计 | WISDEM [10], [11]；CCBlade [14]；RotorSE [15]；DrivetrainSE；TowerSE | HAWTOpt2 [12], [13] |
| 预处理器 | PreComp [16]；BModes [18] | BECAS [17] |
| 气动弹性分析 | OpenFAST [19], [20] | HAWC2 [21]；HAWCStab2 [22] |

整机设计的大部分工作是在风电场一体化系统设计与工程模型（Wind-Plant Integrated System Design & Engineering Model，WISDEM®）中完成的。WISDEM 是一组以简化、准静态为主的模型，可以在少量设计点上快速开展设计优化。WISDEM 构建在美国国家航空航天局（NASA）的 OpenMDAO 库之上，由 OpenMDAO 驱动优化，并充当各模型之间的"胶水"代码 [23]。概念设计随后用 OpenFAST、HAWC2 和 HAWCStab2 的非线性瞬态模型做了更完整的载荷与性能分析，加以验证和完善。这些高保真仿真得到的结果又反馈回 WISDEM，用于更新设计变量的边界和约束取值，整个过程反复迭代。

## 1.4 模型获取

这款参考风机的设计成果可供整个风电行业使用，提供适用于多种分析工具的输入文件，包括 OpenFAST、HAWC2、WISDEM 和 HawtOpt2。此外，本报告图表中的数据也以 Microsoft Excel 格式提供电子版，不再逐一列入附录。上述文件托管在 GitHub 上：

- github.com/IEAWindTask37/IEA-15-240-RWT
- github.com/IEAWindTask37/IEA-15-240-RWT/blob/master/Documentation

IEA Wind 15-MW 参考风机开源发布，旨在鼓励行业同行把各自的设计变体提交回仓库，纳入其中，供他人进一步使用。

## 1.5 气象与海洋环境

作为一款通用参考风机，该设计意在适用于多个不同的海上场址。不过，极限载荷分析和支撑结构设计都取决于具体的风、浪和土壤条件。Stewart 等人 [24] 的工作给出了一套通用、但又足够具体的气象海洋（metocean）环境，可用于开展分析和设计。该工作假定场址位于美国东海岸，详细的风、浪概率分布可在上一小节所述的仓库文档中找到。简要来说：风速服从 Weibull 分布，参数为 [9.767, 2.12]，平均风速约为 8.65 米/秒（m/s）。在该平均风速下，相应的有效波高约为 1.4 m，谱峰周期为 7.9 秒（s）。本报告给出的固定式单桩支撑结构按 30 m 水深设计。

# 2 叶片特性

这款 IEA Wind 15-MW 参考风机的叶片长 117 m，叶根直径 5.2 m，最大弦长 5.77 m，出现在约 20% 展长处。叶片总质量约 65 吨（t），设计要达到的功率系数 CP 为 0.489。叶片的俯视图和侧视图见图 2-1，更完整的参数汇总见表 2-1。

图 2-1 海上风机叶片视图：吸力面（上）与后缘（下）

**表 2-1 叶片参数**

| 说明 | 值 | 单位 |
|---|---|---|
| 叶片长度 | 117 | m |
| 叶根直径 | 5.20 | m |
| 叶根圆柱段长度 | 2.34 | m |
| 最大弦长 | 5.77 | m |
| 最大弦长展向位置 | 27.2 | m |
| 叶尖预弯 | 4.00 | m |
| 预锥角 | 4.00 | deg |
| 叶片质量 | 65,250 | kg |
| 叶片质心位置 | 26.8 | m |
| 设计叶尖速比 | 9.00 | - |
| 一阶挥舞固有频率 | 0.555 | Hz |
| 一阶摆振固有频率 | 0.642 | Hz |
| 设计 CP | 0.489 | - |
| 设计 CT | 0.799 | - |
| 年发电量 | 77.4 | GWh |

deg 度；kg 千克；GWh 吉瓦时；m 米；Hz 赫兹

## 2.1 叶片气动特性

叶片设计采用 DTU 的 FFA-W3 系列翼型。这套翼型资料公开、文档齐全，此前也用于 IEA Wind/DTU 10-MW 海上参考风机，如图 2-2 所示。

各 FFA-W3 翼型的气动数据在雷诺数 Re = 10⁷ 下生成。气动系数在 −32° 至 32° 范围内的计算采用二维不可压缩 Navier-Stokes 求解器 EllipSys2D [25–27]。网格用 HypGrid2D [28] 生成，为 512×256 的径向网格。计算基于 k − ω 剪切应力输运（SST）湍流模型 [29] 和 Drela-Giles 转捩模型 [30]，分别按全湍流和自由转捩两种边界层假设进行，来流湍流强度取 0.1%。我们用 AirfoilPreppy 做了 360° 外推，但由于相对厚度的展向分布是自由设计变量，极曲线没有做三维修正。最终设计的 OpenFAST 模型对极曲线数据施加了 Du-Selig [31] 失速延迟三维修正。叶片所用翼型的气动特性见图 2-3。翼型形状和性能极曲线的表格数据见配套的电子表格文档。

图 2-2 IEA Wind 15-MW 叶片设计采用的 DTU FFA-W3 翼型族

叶片平面形状的设计变量如图 2-4 所示。翼型的气动中心用作叶片的变桨轴线。有几处气动设计特点值得注意。截面从圆柱过渡到相对厚度 50% 的最厚翼型，发生在 2.34 m 至 17.55 m 之间，即展长的 2%–15%；最大弦长 5.77 m 位于 27.2 m 展长处（23.3%）。这些都体现在图 2-4a–b 的弦长和相对厚度分布中。叶片半径这么大，设计在很大程度上由叶尖挠度载荷和塔架净空约束主导。图 2-4c 的扭角分布显示叶尖段有一定卸载，牺牲少量发电量，来缓解叶片最柔部位的强推力载荷。这一特点在第 3 节的风轮性能曲线中还会再次出现。叶片设计了明显的背向塔架的预弯，叶尖弦线与叶根相差 4 m（图 2-4d），为叶尖提供额外的净空。将各翼型沿轴向叠放、生成放样叶片外形时，没有考虑预弯曲率带来的倾斜角。预弯再大一些可以留出更多裕度、降低刚度要求，但据行业反馈，受叶片成型模具等制造方面的限制，预弯量取为 4 m。未来先进制造技术或许能实现更大的叶片预弯，但就目前而言，这是一个合理的约束。

## 2.2 叶片结构特性

放样后的叶片外形见图 2-5，70% 展长处的内部结构布置见图 2-6，更多展向位置见附录 A。叶片的结构布置相当传统：两根主要承载主梁沿叶根至叶尖的直线布置，前缘和后缘辅以加强。一根主梁帽位于翼型的压力面一侧，另一根位于吸力面一侧。主梁帽采用碳纤维，用尽可能小的重量提供尽可能大的刚度。叶片有两块腹板，连接压力面和吸力面，并与主梁相连，从 10% 展长延伸到 95% 展长，如图 2-6 中的竖直构件所示。前缘和后缘加强采用单向玻璃纤维，以提供额外的摆振刚度。在前缘、后缘加强与主梁帽之间还填充了泡沫芯材板，压力面和吸力面两侧都有。

图 2-3 叶片所用翼型的气动极曲线

图 2-4 叶片平面形状参数沿展向的分布
图 2-5 叶片三维放样外形

图 2-6 展向 70% 处叶片截面

叶片的内部结构与复合材料铺层按 IEA 风机本体规范（Wind Turbine Ontology）[32] 定义。复合材料层作为展向单元，叠加在叶片壳体或腹板上，并沿叶片弯曲的参考轴线布置。该本体规范允许用多种方式定义单元：可以按实际尺寸定义，给出层宽（弧长）、偏置和相对参考位置的转角；也可以按无量纲方式定义，用归一化弧长位置表示，如图 2-7 所示。归一化弧长坐标（s）定义为：吸力面后缘处为 0，压力面后缘处为 1。对于平背翼型，后缘取平背面的中点。

图 2-7 IEA 风机本体规范复合材料定义示意图（自叶根至叶尖）

叶片的材料铺层见图 2-8 和图 2-9：图 2-8 给出沿翼型壳体、随弧长 s 坐标变化的铺层，图 2-9 给出腹板的铺层。各结构部件的完整铺层定义见配套的叶片本体文件和 Microsoft Excel 文件。铺层定义完成后，叶片梁的结构参数分别用 PreComp [16] 和 VABS [33, 34]（NREL 工具链）或 BECAS [17, 35]（DTU 工具链）计算。这些工具算出沿叶片各截面的刚度矩阵，再输入 OpenFAST 或 HAWC2 使用。NREL 与 DTU 两套建模工具算出的整机性能对比见 Rinker 等人 [36] 的工作。图 2-10 和图 2-11 给出了最终的叶片梁结构参数。第一阶挥舞、摆振和扭转模态的结构阻尼分别取 3%、3% 和 6%。

图 2-8 不同展向位置处，铺层厚度随翼型归一化 s 坐标的变化

图 2-9 不同展向位置处腹板的铺层厚度

图 2-10 用 PreComp 算出的叶片梁结构参数随展向叶片曲线位置的变化

图 2-11 叶片平面形状与结构参数

# 3 风轮性能

风轮性能与控制器行为、变桨调度紧密耦合，三者共同决定主轴转速（rpm）、扭矩和推力能否达到目标值。本章先介绍控制器，再给出风轮性能数据。

## 3.1 控制器特性

IEA Wind 15 MW 参考风机配了两套控制器：NREL 的开源参考控制器 ROSCO [37] 和 DTU 基础控制器（Basic Controller）[38]，分别在 OpenFAST 和 HAWC2 中实现。风轮最低转速为 5 rpm，目的是避开塔架/单桩固有频率的 3P（3 倍频）干扰；风速 10.59 m/s 时达到额定转速 7.55 rpm，对应的名义最大叶尖速度为 95 m/s。在设计叶尖速比（TSR）下，风轮桨距角为 0°；但在低风速段，为了在保持最低转速的同时跟踪最大功率，风轮采用正桨距角运行。风速达到额定值 10.59 m/s 后，风轮开始变桨。

### 3.1.1 控制器方法

两套控制器都对发电机扭矩和叶片桨距角各设了一个 PI（比例-积分）控制器在起作用，并对转子转速和桨距角设置了饱和限值，保证风机在设计约束内运行。控制器的运行可分为三个区域：

**3 m/s ≤ U ≤ 6.98 m/s：最低转速区。** 用发电机扭矩 PI 控制器把风机转速稳在最低转速 5 rpm。在 ROSCO 中，最小桨距角根据风速估计值设定，使 CP 最大。这个让 CP 最大的最小桨距角事先用稳态叶素动量分析算好，所用工具是 CCBlade [14]。在 DTU 基础控制器中，扭矩控制器也用 PI 控制来调节额定风速，桨距角则查表确定，查表依据是滤波后的轮毂高度风速。

**6.98 m/s ≤ U ≤ 10.59 m/s：最优叶尖速比区。** 在额定风速以下，用发电机扭矩 PI 控制器调节转速，使风轮始终运行在最优叶尖速比上。

**10.59 m/s ≤ U ≤ 25 m/s：额定功率区。** 在额定风速以上，用桨距角 PI 控制器调节转速。变桨控制器的目标是把转子转速稳在额定值 7.55 rpm。对于浮式风机，传统上会把恒功率设定改为恒发电机扭矩。

ROSCO 中用了一个基于扩展卡尔曼滤波的风速估计器：一方面在额定以下运行时估计最优转子转速，另一方面在最低转速运行时确定最小桨距角。在 2.5 区（Region 2.5），ROSCO 没有沿用 NREL 5 MW 参考风机的线性恒转速方法，而是采用设定点平滑（setpoint-smoothing）方法 [39]，保证控制区域之间平滑过渡。由于设计优化的结果，IEA Wind 15 MW 风机的 2.5 区小到可以忽略——因为达到额定扭矩时正好也达到额定转速。发电机扭矩和变桨控制器的 PI 增益按 ROSCO 通用整定方法 [39] 计算，已写入配套的 OpenFAST 输入文件。

DTU 基础控制器的参数用 HAWCStab2 的控制器整定功能确定。部分载荷极点（扭矩控制器）和满载极点（变桨控制器）假定的固有频率和阻尼分别为 0.05 Hz、70% 临界阻尼和 0.03 Hz、70% 临界阻尼。增益调度采用二次形式，并假定功率恒定。整定出的控制器参数见 HAWC2 输入文件；所有参数以及 1 区、2 区、3 区的定义都与 DTU 基础控制器报告 [38] 中的定义一致。

## 3.2 稳态性能

图 3-1 给出了用 OpenFAST 配合 ROSCO 控制器算出的风轮稳态性能随风速的变化。在 1.5 区（Region 1.5），最低转速约束使叶尖速比明显偏高、偏离最优。变桨控制器根据风速估计施加最小桨距角约束，使 CP 最大，于是低风速下出现最大可达 4° 的正桨距角。与此同时，发电机扭矩控制器在 1.5 区努力把转子转速稳在最低值。在 2 区，扭矩控制器跟踪设定叶尖速比，设定点取在 CP 最大值附近或正好取在最大值处。这支叶片的设计点是 TSR = 9.0、桨距角 Θpitch = 0°，略低于图 3-2 的 CP 和 CT 曲线所示的最优点 TSR = 8.5、Θpitch = −1.0°。设计点略偏离最优是叶片设计过程折中的结果，要在发电量和设计约束载荷之间权衡。ROSCO 的设定点平滑程序避免了 2.5 区过渡时发电机扭矩控制器和变桨控制器相互冲突。这支设计的 2.5 区实际上可以忽略，所以 ROSCO 中设定点平滑和削峰（peak shaving）程序的影响很小。最后在 3 区，扭矩控制器在额定扭矩处饱和，变桨 PI 控制器向顺桨方向变桨，保持额定转速。

图 3-3 对叶片性能作了进一步分析：在一系列额定以下风速下，计算了叶片上的分布气动力。第 2 节介绍过，叶片的气动设计、尤其是扭角分布，受叶尖挠度和塔架净空约束的限制很紧。叶片上的气动力在约 90 m 处达到峰值，然后向叶尖逐渐减小。叶尖这样卸载有助于避免扫塔；但代价是发电量损失，尤其是叶尖的气动效率和边际扫掠面积都是全叶片最高的。叶片外侧 5% 段那段陡直的线性下降，是气弹仿真中采用的 Prandtl 叶尖损失模型造成的。
图 3-1 采用 ROSCO 控制器时，OpenFAST 叶素动量法给出的 15 MW 风轮气动性能与运行特性

图 3-2 CCBlade 定常叶素动量法得到的气动功率系数和推力系数曲面（随桨距角和叶尖速比变化）

图 3-3 叶片上的展向力随风速的变化

# 4 塔架与单桩基础特性

塔架和单桩基础在 WISDEM 和 OpenFAST 中按各向同性钢管来设计。单桩的设计参考了 Arany 发表的一份实用指南[40]。这部分设计在很大程度上是被频率要求卡住的：塔架—单桩的一阶频率为 0.170 Hz，在所有风速下都落在叶片通过频率 1P 和 3P 的频带之间，如图 4-1 所示。这样也能避开东海岸通用场址预期的海浪频率范围，即 0.10 Hz 到 0.13 Hz。需要注意，换成漂浮式基础后，频率要求和边界条件都会变，需要刚度更大的塔架。因此，这里给出的塔架几何后续会被换成更适合半潜式平台的方案。

图 4-1 塔架固有频率与激励频率归一化功率谱密度（PSD）的相对位置

塔架高度按轮毂高度达到 150 m 来定，这样叶片长 120 m 时，叶尖距地面（水面）还有 30 m 净空。¹ 单桩基础的外径为 10 m，已经顶到当前制造和安装工艺的上限。外径和壁厚沿高度的分布见图 4-2，并列于表 4-2，一路往下到埋入段的吸力桩。材料参数见表 4-1。本次设计没有做详细的土质岩土分析，而是用一组弹簧常数来等效土体刚度，接入一维有限元模型。土体剪切模量和泊松比的取值，代表的是密实砂土或砾石土[41]。土体刚度弹簧常数的计算公式见附录 B.2。

¹ 30 m 净空值并无官方标准规定，海上风电机组的净空一般在 20 m 到 30 m 之间。

表 4-1 塔架材料特性

| 参数 | 符号 | 数值 | 单位 |
|---|---|---|---|
| 杨氏模量，钢 | E | 2.00E11 | Pa |
| 剪切模量，钢 | G | 7.93E10 | Pa |
| 密度，钢 | ρ | 7.85E3 | kg/m3 |
| 剪切模量，土 | Gs | 140E6 | Pa |
| 泊松比，土 | νs | 0.4 |  |

Pa：帕斯卡；kg/m3：千克每立方米

HAWC2 和 OpenFAST 都需要一系列结构截面特性参数，这些参数由直径和壁厚分布就能直接算出来，如图 4-3 所示，具体公式见附录 B。注意，表 1-1 中报告的最终质量，是在圆柱壳体质量之外再加 7% 的舾装质量，并另加过渡段的 100 t。

图 4-2 塔架外径与壁厚

图 4-3 塔架与单桩的截面特性

表 4-2 塔架与基础的部分关键特性与尺寸

| 位置 | 高度 [m] | 外径 [m] | 壁厚 [mm] |
|---|---|---|---|
| 单桩起点 | -75.000 | 10.000 | 55.341 |
| 泥线 | -30.000 | 10.000 | 55.341 |
|  | -29.999 | 10.000 | 55.341 |
|  | -25.000 | 10.000 | 55.341 |
|  | -24.999 | 10.000 | 53.449 |
|  | -20.000 | 10.000 | 53.449 |
|  | -19.999 | 10.000 | 51.509 |
|  | -15.000 | 10.000 | 51.509 |
|  | -14.999 | 10.000 | 49.527 |
|  | -10.000 | 10.000 | 49.527 |
|  | -9.999 | 10.000 | 47.517 |
|  | -5.000 | 10.000 | 47.517 |
|  | -4.999 | 10.000 | 45.517 |
| 水线 | 0.000 | 10.000 | 45.517 |
|  | 0.001 | 10.000 | 43.527 |
|  | 5.000 | 10.000 | 43.527 |
|  | 5.001 | 10.000 | 42.242 |
|  | 10.000 | 10.000 | 42.242 |
|  | 10.001 | 10.000 | 41.058 |
| 塔架起点 | 15.000 | 10.000 | 41.058 |
|  | 15.001 | 10.000 | 39.496 |
|  | 28.000 | 10.000 | 39.496 |
|  | 28.001 | 10.000 | 36.456 |
|  | 41.000 | 9.926 | 36.456 |
|  | 41.001 | 9.926 | 33.779 |
|  | 54.000 | 9.443 | 33.779 |
|  | 54.001 | 9.443 | 32.192 |
|  | 67.000 | 8.833 | 32.192 |
|  | 67.001 | 8.833 | 30.708 |
|  | 80.000 | 8.151 | 30.708 |
|  | 80.001 | 8.151 | 29.101 |
|  | 93.000 | 7.390 | 29.101 |
|  | 93.001 | 7.390 | 27.213 |
|  | 106.000 | 6.909 | 27.213 |
|  | 106.001 | 6.909 | 24.009 |
|  | 119.000 | 6.748 | 24.009 |
|  | 119.001 | 6.748 | 20.826 |
|  | 132.000 | 6.572 | 20.826 |
|  | 132.001 | 6.572 | 23.998 |
| 塔架顶部 | 144.582 | 6.500 | 23.998 |

塔架阻尼只考虑刚度比例阻尼。对 OpenFAST 和 HAWC2，刚度比例系数的定法是：让塔架一阶前后向、一阶侧向和一阶扭转模态（分别为第 1、2、7 阶模态）的对数衰减率都达到 2%。各模型最终用的具体数值见各自的输入文件。

# 5 机舱、传动链与轮毂

IEA Wind 15 MW 参考风机采用直驱型式，配一台永磁同步径向磁通发电机，机舱布置简单紧凑。直驱相比齿轮传动链有不少好处：零部件更少、结构更简单、可靠性更高，特殊拓扑的设计自由度也更大。但发电机在极低转速下直接耦合运行，物理尺寸和质量都很大，给运输、吊装和维护带来麻烦。要化解这些矛盾，需要在发电机位置、轴承数量、定子/转子内外置型式、定转子非有效部分的结构几何、辅助部件接口等多个方面综合权衡，取一个最优平衡[42]。

图 5-1 15 MW 直驱风机机舱布置的示意图与 CAD 模型。未按比例绘制，省略了部分结构细节。叶片（未画出）、轮毂、轴和发电机转子为旋转部件

## 5.1 机舱总体布置

图 5-1a 是一台简单的直驱机舱布置，采用外转子永磁发电机。整个总成由一根轮毂轴构成，轴上装着风轮和发电机转子，由两个主轴承支承；轴承座装在一个静止的支承座上，该支承座从底座上悬臂伸出。底座负责把轮毂载荷，以及风轮、发电机、轮毂、轴和支承座的重量，传给塔架。三维 CAD 图见图 5-1b。确定各部件的最优尺寸时，把极端湍流工况下极端气动载荷对应的等效 von Mises 应力上限取为 200 MPa。按国际电工委员会（IEC）61400-1 的建议，假定这些极限载荷代表该工况下的多轴载荷。机舱及其各部件的完整质量分解见表 5-1。

## 5.2 轮毂

轮毂采用简单的球形壳体模型，上面为叶片和法兰留了开孔。轮毂直径按叶片根部直径的函数来计算。轮毂壳体的厚度设计为能够承受
表 5-1 机舱总成的集中质量与转动惯量

（坐标系原点在塔顶，x 轴顺风向[与地面/水面平行，不是主轴方向]，z 轴竖直向上）

| 名称 | X_TT [m] | Z_TT [m] | 质量 [t] | Ixx [kg m²] | Iyy [kg m²] | Izz [kg m²] |
|---|---|---|---|---|---|---|
| 偏航系统 | 0.000 | -0.190 | 100.0 | 490,266 | 490,266 | 978,125 |
| 转塔鼻锥 | 5.786 | 4.956 | 11.394 | 12,571 | 10,890 | 10,909 |
| 发电机内定子 | 5.545 | 4.913 | 226.629 | 3,777,313 | 2,012,788 | 2,042,312 |
| 发电机外转子 | 6.544 | 5.033 | 144.963 | 3,173,003 | 1,673,269 | 1,691,864 |
| 主轴 | 6.208 | 5.000 | 15.734 | 33,009 | 22,906 | 23,018 |
| 轮毂 | 10.604 | 5.462 | 190.0 | 1,382,171 | 2,169,261 | 2,160,637 |
| 底座 | 0.812 | 2.697 | 70.329 | 398,973 | 515,880 | 535,055 |
| 法兰 | 4.593 | 4.831 | 3.946 | 4,081 | 2,065 | 2087 |
| 其他设备 | 0.000 | 0.500 | 50.0 | 16,667 | 16,667 | 25,000 |
| TDO 主轴轴承 | 6.582 | 5.040 | 2.230 | 3,515 | 1,784 | 1,803 |
| SRB 主轴轴承 | 5.388 | 4.914 | 5.664 | 8,930 | 4,593 | 4,641 |
| 机舱合计 | 5.486 | 3.978 | 820.888 | 12,607,277 | 21,433,958 | 18,682,468 |
| 机舱合计（不含轮毂） | 3.945 | 3.352 | 630.888 | 10,680,747 | 122,447,810 | 10,046,187 |

kg m²：千克平方米；m：米；t：吨；TDO：双列圆锥滚子（tapered double outer）；SRB：调心滚子轴承（spherical roller bearing）

……能够承受紧急停机时产生的力。轮毂法兰直径取轮毂直径的一半，法兰厚度取轮毂壳体厚度的四倍。法兰边缘做了专门设计，尽量减小应力集中。变桨系统没有做精细建模，其质量用回归拟合公式估算。

## 5.3 主轴、轴承与转塔

主轴、轴承和转塔如图 5-2 所示，主要参数和尺寸见表 5-2。主轴为空心圆柱截面，壁厚不变，倾角为 6°。主轴连同风轮由两套主轴承支撑。两套主轴承都是外圈旋转、内圈固定。外圈和轴承座装在转塔里，转塔由底座托住。风轮、发电机转子和轮毂的全部重量，都经主轴通过轴承传到转塔上。

图 5-2 （a）主轴和（b）转塔（又称鼻锥）的 CAD 示意图；尺寸见表 5-2

主轴内径设计时给机舱转塔和主轴承留了足够间隙。轴的壁厚这样定：既要保证风轮载荷有安全的传力路径，又要限制发电机处的最大挠度。假定全部推力载荷都由主轴传给迎风侧主轴承。

转塔同样是空心圆柱截面，壁厚不变，从底座上悬臂伸出。内径定为 2 m，给检修人员留出通行空间。转塔筒壁的厚度这样定：先算出主轴承的支反力，再把转塔与发电机转子、定子接口处的最大径向挠度控制在限值以内。假定转塔承受迎风侧主轴承传来的全部推力、横向力产生的弯矩以及扭矩。

两套轴承一前一后配对：迎风侧轴承定位，下风侧轴承游动。定位轴承选双列圆锥滚子型式（TDO），非定位轴承选调心滚子轴承（SRB）。轴承方案按文献 [43] 的推荐选定，并按 DNV 规范的方法针对极限载荷做了基本的寿命估算。主轴承支反力用气弹仿真得到的载荷来算。假定轴向载荷和弯矩全部由迎风侧轴承承担，径向力由前后两套轴承共同分担。这些力直接传给转塔，再经底座传到塔架。下风侧轴承受力较小，所以选了额定载荷低一些的轴承。

表 5-2 主轴尺寸、轴承及定型所用载荷

| 符号 | 说明 | 数值 | 单位 |
|---|---|---|---|
| Lfl | 轮毂法兰长度 | 0.358 | m |
| Lmb1 | 迎风侧轴承位置 | 1.0 | m |
| Lgr | 发电机转子位置 | 0.1 | m |
| L12 | 迎风侧与下风侧轴承间距 | 1.2 | m |
| Las | 主轴质心位置 | 1.25 | m |
| γ | 主轴倾角 | 6.0 | deg |
| Lms | 主轴长度 | 2.2 | m |
| Rosh | 主轴外半径 | 3.0 | m |
| Rish | 主轴内半径 | 2.8 | m |
| Lgs | 发电机定子距底座法兰位置 | 0.25 | m |
| Lan | 转塔质心位置 | 1.2 | m |
| L2n | 下风侧轴承距底座法兰距离 | 0.9 | m |
| Lan | 转塔长度 | 2.2 | m |
| Ron | 转塔外半径 | 2.2 | m |
| Rin | 转塔内半径 | 2.0 | m |
| Mb1 | 双列圆锥滚子轴承：质量 | 2,230 | kg |
| Mb2 | 调心滚子轴承：质量 | 5,664 | kg |

deg：度；m：米；kg：千克

## 5.4 底座

底座是一根空心、椭圆弯曲的悬臂梁，截面为圆形。它一端截面较小，与底座法兰连接；另一端截面较大，与塔顶的偏航轴承连接。圆环单元的壁厚经过优化，把弯曲、扭转、剪力和轴向载荷叠加起来的总应力控制在 200 MPa 以内。底座端部总挠度是转塔设计的输入量，用来准确估算气隙挠度。主导载荷工况取自极端气动载荷与湍流风场。图 5-3 是底座的 CAD 示意图，其关键尺寸见表 5-3。

## 5.5 偏航系统

偏航系统轴承选自 SKF 产品目录，具体为双排角接触球轴承。偏航系统在直径 6.5 m 处把底座底部与塔顶连接起来。

图 5-3 底座的 CAD 示意图

表 5-3 底座参数

| 符号 | 说明 | 数值 | 单位 |
|---|---|---|---|
| Ltop | 塔顶距转塔法兰距离 | 5 | m |
| Hnose | 鼻锥高度 | 4.875 | m |
| Dtop | 塔顶直径 | 6.5 | m |
| t | 底座壁厚 | 50 | mm |
| Mbed plate | 底座质量 | 70,329 | kg |

kg：千克；m：米；mm：毫米

## 5.6 直驱发电机

我们用 WISDEM [44] 里的 DrivetrainSE 模块，设计并优化了一台 15 MW 直驱同步发电机。这台发电机采用外转子径向磁通结构，永磁体表贴安装（见图 5-4），设计与性能参数见表 5-4。外转子方案的好处是结构简单结实、制造容易、端部绕组短，而且绕组与齿之间的散热比内转子方案更好。定子采用分数槽双层集中绕组，基波绕组因数能做到最大。设计优化参照了文献 [45–47] 的方法。设计中的主要假定如下：

- 转子磁钢用 N40 牌号烧结钕铁硼（NdFeB）永磁体，剩磁密度 1.28 特斯拉（T），相对磁导率 1.06。
- 只考虑气隙磁通的径向分量，忽略漏磁和边缘效应。
- 槽极配合取 2–5，用 Cro 方法和绕组矢量法 [45] 导出集中绕组排布。
- 磁钢宽度假定为极距的 80%。
- 设计对称，磁路不饱和。
- 磁负荷和电负荷按切向应力典型值 60 kPa 确定。比电流负荷假定小于 100 千安/米（kA/m），前提是配一套高效的热管理系统，这样不增大电机尺寸就能提高输出功率。
- 用单侧圆盘式支撑结构来托住电磁有效材料，大幅简化装配。
- 气隙长度假定为气隙直径的 1/1,000。气隙允许最多 20% 的变形，支撑结构、主轴和转塔都对这个变形有贡献。

优化后的设计有 100 对极，分布在直径 10.53 m 的气隙圆周上，铁心长度 2.17 m，效率 96.5%。发电机重 372 t，其中定子 227 t、转子 145 t。至少 50% 的质量来自结构支撑件。

## 5.7 机舱阻尼

我们给主轴选了刚度比例阻尼，让发电机/刚性风轮系统的自由-自由模态达到 5% 的临界模态阻尼。这个取值参照了 NREL 5 MW 参考模型。具体来说，刚度比例系数 β 应这样选取：

β = 2ζ·√(Igen·Irot) / [KDT·(Igen + Irot)] （5.1）

式中，ζ 是目标模态阻尼，Ii 是发电机或风轮的转动惯量，KDT 是传动链的等效刚度。对这台风机，刚性风轮转动惯量约为 3.524 605 × 108 千克平方米（kgm2），由 HAWC2 叶片结构文件算得，忽略了锥角和预弯。由此得到扭转运动的 β = 4.457 544 × 10−4。

图 5-4 外转子直驱发电机的 CAD 示意图，含电磁与结构设计参数

表 5-4 15 MW 直驱发电机的电磁与结构设计

| 符号 | 说明 | 数值 | 单位 |
|---|---|---|---|
| Pr | 发电机端额定功率 | 15 | MW |
| ωr | 额定转速 | 0.792 | rad/s |
| fe | 电频率 | 12.6 | Hz |
| Tr | 额定转矩 | 21.03 | MN m |
| **电磁设计** | | | |
| rg | 气隙半径 | 5.08 | m |
| l | 铁心长度 | 2.17 | m |
| g | 气隙长度 | 10.16 | mm |
| p | 极数 | 200 | - |
| S | 定子槽数 | 240 | - |
| hys | 定子轭厚 | 46.52 | mm |
| hyr | 转子轭厚 | 63.62 | mm |
| τp | 极距 | 159.55 | mm |
| τs | 槽距 | 132.7 | mm |
| hs | 槽高 | 400.03 | mm |
| bs | 槽宽 | 57.3 | mm |
| bt | 齿宽 | 74.85 | mm |
| hm | 磁钢高度 | 58.39 | mm |
| bm | 磁钢宽度 | 127.64 | mm |
| V | 线电压有效值 | 4770.34 | V |
| I | 绕组额定电流（有效值） | 1084.55 | A |
| Rs | 定子绕组每相电阻 | 0.16 | Ω |
| Ns | 定子绕组每相匝数 | 320 | - |
| B̂g | 气隙磁密峰值 | 1.06 | T |
| Js | 绕组电流密度 | 3.39 | A/mm2 |
| A1 | 比电流负荷 | 92.46 | kA/m |
| η | 满载效率 | 96.55 | % |
| MIron | 铁质量 | 180.95 | t |
| MCu | 铜质量 | 9.01 | t |
| MMagnet | 磁钢质量 | 24.20 | t |
| MActive | 有效材料总质量 | 214.16 | t |
| **结构设计** | | | |
| hss | 定子轮缘厚度 | 46.59 | mm |
| ts | 定子圆盘厚度 | 79.97 | mm |
| hsr | 转子轮缘厚度 | 63.69 | mm |
| tr | 转子圆盘厚度 | 81.75 | mm |
| δl | 转子与定子间隙 | 825 | mm |
| MSStru | 转子结构钢总质量 | 86.2 | t |
| MRStru | 定子结构钢总质量 | 71.1 | t |
| MGen | 发电机总质量（估算） | 371.57 | t |

MW：兆瓦；V：伏特；rad/s：弧度每秒；A：安培；Hz：赫兹（每秒周数）；Ω：欧姆；MN m：兆牛米；T：特斯拉；m：米；A/mm2：安培每平方毫米；mm：毫米；kA/m：千安每米；t：吨

## 6 载荷评估

我们做了一项 IEC 设计载荷工况（DLC）[4] 分析研究，目的是找出对关键设计约束部件最不利的极限载荷。表 6-1 给出了在 OpenFAST 中仿真的各 DLC 工况的设置，表 6-2 给出了相应的风浪（气象海洋）输入条件。全部工况下的最大弯矩和最大挠度做了排序对比，见图 6-1 和图 6-2。对这个设计来说，最不利的载荷出现在两个工况下：极端风速下带偏航误差的停机工况，以及带风向变化的极端相干阵风工况。最不利的面外叶尖挠度为 22.8 m，塔筒净空绰绰有余——叶片不变形时叶尖到塔筒的距离为 30.0 m。这个裕度说明叶片设计偏保守，后续再做气弹优化，有望在满足推荐安全裕度的前提下进一步提升气动性能或降低度电成本。不过我们没有对这支叶片做完整的疲劳分析，对这么大尺寸的叶片来说，摆振方向的叶片弯矩可能会是个问题。

表 6-1 IEC 设计载荷工况（DLC）设置汇总

| DLC | 风况 | 风速 | 附加设置 | 种子数 | 仿真数 |
|---|---|---|---|---|---|
| 1.1 | NTM | 3:2:25 m/s | - | 6 | 72 |
| 1.3 | ETM | 3:2:25 m/s | - | 6 | 72 |
| 1.4 | ECD | Vr，Vr ±2 m/s | ±风向变化 | - | 6 |
| 1.5 | EWS | 3:2:25 m/s | ±垂直/水平 | - | 48 |
| 6.1 | EWM | V50 | 偏航 ±8° | 6 | 12 |
| 6.3 | EWM | V1 | 偏航 ±20° | 6 | 12 |

NTM：正常湍流模型；ETM：极端湍流模型；ECD：带风向变化的极端相干阵风；EWS：极端风切变；EWM：极端风速模型；Vr = 10.8 m/s：额定风速；V50 = 50.0 m/s：50 年一遇的 10 分钟平均极端风速；V1 = 40.0 m/s：1 年一遇的 10 分钟平均极端风速

表 6-2 DLC 分析所用的风浪条件

| 运行状态 | 风速 [m/s] | 有效波高 [m] | 谱峰周期 [s] |
|---|---|---|---|
| 正常 | 4 | 1.102 | 8.515 |
| | 6 | 1.179 | 8.310 |
| | 8 | 1.316 | 8.006 |
| | 10 | 1.537 | 7.651 |
| | 12 | 1.836 | 7.441 |
| | 14 | 2.188 | 7.461 |
| | 16 | 2.598 | 7.643 |
| | 18 | 3.061 | 8.047 |
| | 20 | 3.617 | 8.521 |
| | 22 | 4.027 | 8.987 |
| | 24 | 4.516 | 9.452 |
| 极端，1 年一遇 | 40 | 9.686 | 16.654 |
| 极端，50 年一遇 | 50 | 11.307 | 18.505 |

m：米；m/s：米每秒；s：秒
图 6-1 各设计载荷工况下叶根弯矩与塔底弯矩最大值的排序

图 6-2 各设计载荷工况下叶尖变形与塔顶变形最大值的排序

## 6.1 结论

事实证明，公开发布的参考风机设计对风电科研界来说是一件非常趁手的工具。随着技术不断成熟、进步，后续的参考风机 [2, 3, 5–9] 也一代代做了出来，既跟上行业趋势，也保持了一定的前瞻性。参考风机要想对面向未来的技术开发和分析工作真正有用，就必须代表当前最先进、或者接近未来一代的风机技术水平。做这项工作，是因为现有的海上参考风机在 10 MW 到 20 MW 之间存在空白，而行业正在向 10 MW 以上走。

本报告介绍 IEA Wind 15 MW 参考风机的设计与性能。该机型由 NREL、DTU 和 UMaine 联合开发，并与 IEA Wind Task 37（风能系统工程）第二个工作包相互配合。这款参考风机是一个标准化设计，行业向更大机组发展的过程中，可以拿它来做各种概念研究。机型采用传统的三叶片、上风向布局：风轮直径 240 m，轮毂高度 150 m，变速、统一变桨控制，配一台低速直驱发电机。报告还给出了一个基准的钢制单桩支撑结构，按 30 m 水深做了尺寸设计。后续将与 UMaine 合作，另行发布一款采用钢制半潜式浮式基础的浮式支撑结构方案。

设计的更多细节，包括 OpenFAST、HAWC2 和 WISDEM 的输入文件，都可以在 IEA Wind Task 37 的 GitHub 上找到。

# 参考文献

 [1]   WindEurope. Offshore Wind in Europe. Key Trends and Statistics. Tech. rep. WindEurope, 2019.
 [2]   Pietro Bortolotti, Helena Canet Tarrés, Katherine Dykes, Karl Merz, Latha Sethuraman, David Verelst, and Frederik Zahle. IEA Wind TCP Task 37: Systems Engineering in Wind Energy - WP2.1 Reference Wind Turbines. Tech. rep. International Energy Agency, 2019. DOI: 10.2172/1529216.
 [3]   INNWIND.EU. http://www.innwind.eu/publications/deliverable-reports. 2017.
 [4]   International Electrotechnical Commission. Wind Turbines – Part 1: Design requirements. Tech. rep. IEC 61400-1 Ed.3. 2005.
 [5]   G. Bywaters, V. John, J. Lynch, P. Mattila, G. Norton, J. Stowell, M. Salata, O. Labath, A. Chertok, and D. Hablania. Northern Power Systems WindPACT Drive Train Alternative Design Study Report. Tech. rep. 2004.
 [6]   J. Jonkman, S. Butterfield, W. Musial, and G. Scott. Definition of a 5-MW Reference Wind Turbine for Offshore System Development. Tech. rep. NREL/TP-500-38060. National Renewable Energy Laboratory, 2009.
 [7]   C. Bak, F. Zahle, R. Bitsche, and T. Kim. Description of the DTU 10MW reference wind turbine. Tech. rep. DTU Wind Energy Report I-0092. DTU Wind Energy, 2013.
 [8]   C. Desmond, J. Murphy, L. Blonk, and W. Haans. “Description of an 8 MW reference wind turbine.” In: Journal of Physics: Conference Series (2016). DOI: 10.1088/1742-6596/753/9/092013.
 [9]   D. Griffith and T. Ashwill. The Sandia 100-meter All-glass Baseline Wind Turbine Blade : SNL100-00. Tech. rep. SAND2011-3779. Sandia National Laboratories, 2011.
[10]   Katherine Dykes, Peter Graf, George Scott, Andrew Ning, Ryan King, Yi Guo, Taylor Parsons, Rick Damiani, Fort Felker, and Paul Veers. “Introducing WISDEM: An Integrated System Model of Wind Turbines and Plants.” In: Third Wind Energy Systems Engineering Workshop, January 14, 2015. Boulder, CO, 2015.
[11]   WISDEM. 2019. URL: https://github.com/WISDEM/WISDEM.
[12]   “Aero-Elastic Optimization of a 10 MW Wind Turbine.” English. In: Proceedings - 33rd Wind Energy Symposium. Vol. 1. American Institute of Aeronautics and Astronautics, 2015, pp. 201–223.
[13]   “Design of an aeroelastically tailored 10 MW wind turbine rotor.” English. In: vol. 753. IOP Publishing, 2016. DOI : 10.1088/1742-6596/753/6/062008.
[14]   S. A. Ning. CCBlade Documentation: Release 1.1.0. Tech. rep. National Renewable Energy Laboratory (NREL), Golden, CO (United States), 2013. URL: http://wisdem.github.io/CCBlade/.
[15]   SA Ning. RotorSE Documentation: Release 0.1.0. Tech. rep. National Renewable Energy Lab. (NREL), Golden, CO (United States), 2014. URL: http://wisdem.github.io/RotorSE/.
[16]   Gunjit S. Bir. User’s Guide to PreComp. Tech. rep. Golden, CO: National Renewable Energy Laboratory, 2005.
[17]   José Pedro Albergaria Amaral Blasques. User’s Manual for BECAS: A cross section analysis tool for anisotropic and inhomogeneous beam sections of arbitrary geometry. Tech. rep. 2012.
[18]   G. Bir. User’s Guide to BModes. Tech. rep. NREL/TP-500-39133. Golden, Colorado: National Renewable Energy Laboratory, 2005.
[19]   Jason M. Jonkman and Marshall L. Buhl Jr. FAST User’s Guide. Tech. rep. NREL/EL-500-38230. Golden, Colorado: National Renewable Energy Laboratory, 2005. DOI: 10.2172/15020796.
[20]   OpenFAST Documentation. 2019. URL: https://openfast.readthedocs.io/en/master/.
[21]   Torben J. Larsen and Anders Melchior Hansen. How 2 HAWC2, the user’s manual. Tech. rep. 2007.
[22]   M. Hansen, L. Henriksen, C. Tibaldi, L. Bergami, D. Verelst, G. Pirrung, and R. Riva. HAWCStab2 User Manual. Tech. rep. Roskildem, Denmark: Technical University of Denmark, 2018.
[23]   Justin S. Gray, John T. Hwang, Joaquim R. R. A. Martins, Kenneth T. Moore, and Bret A. Naylor. “OpenMDAO: An open-source framework for multidisciplinary design, analysis, and optimization.” In: Structural and Multidisciplinary Optimization 59.4 (Apr. 2019), pp. 1075–1104. DOI: 10.1007/s00158-019-02211-z.
[24]   Gordon M. Stewart, Amy Robertson, Jason Jonkman, and Matthew A. Lackner. “The creation of a comprehensive metocean data set for offshore wind turbine simulations.” In: Wind Energy 19.6 (2016), pp. 1151–1159. DOI: 10.1002/we.1881.
[25]   Jess A Michelsen. Basis3D-a platform for development of multiblock PDE solvers. Tech. rep. AFM 92-05, Technical University of Denmark, 1992.
[26]   Jess A Michelsen. “Block structured Multigrid solution of 2D and 3D elliptic PDE’s.” PhD thesis. 1994.
[27]   Niels N. Sørensen. “General purpose flow solver applied to flow over hills.” Published 2003. PhD thesis. 1995.
[28] Niels N. Sørensen. HypGrid2D a 2-D mesh generator. Tech. rep. 1035(EN). 1998.
[29] Florian Menter. “Zonal two equation kw turbulence models for aerodynamic flows.” In: 23rd fluid dynamics, plasmadynamics, and lasers conference, p. 2906.
[30] Mark Drela and Michael B Giles. “Viscous-inviscid analysis of transonic and low Reynolds number airfoils.” In: AIAA journal 25.10 (1987), pp. 1347–1355.
[31] Zhaohui Du and Michael S. Selig. “A 3-D stall-delay model for horizontal axis wind turbine performance prediction.” English (US). In: AIAA/ASME Wind Energy Symposium, 1998 ; Conference date: 12-01-1998 Through 15-01-1998. Jan. 1998, pp. 9–19.
[32] K. Dykes et al. System Modeling Frameworks for Wind Turbines and Plants. Tech. rep. In preparation. International Energy Agency.
[33] Yu Wenbin. VABS Manual for Users. Tech. rep. West Jordan, UT: AnalySwift, 2011.
[34] T. Pflumm, W. Garre, and M. Hajek. “A preprocessor for parametric composite rotor blade cross-sections.” In: 44th European Rotocraft Forum. Delft, The Netherlands, 2018.
[35] José Pedro Albergaria Amaral Blasques and Mathias Stolpe. “Multi-material topology optimization of laminated composite beam cross sections.” In: Composite Structures 94.11 (2012), pp. 3278–3289. ISSN: 0263-8223. DOI: https://doi.org/10.1016/j.compstruct.2012.05.002.
[36] J. Rinker, E. Gaertner, P. Bortolotti, W. Skrzypinski, F. Zahle, H. Bredsmoe, G. Barter, and K. Dykes. “Comparison of loads from HAWC2 and FAST for the IEA 15 MW Reference Wind Turbine.” In: Torque 2020.
[37] National Renewable Energy Laboratory. ROSCO. Version 0.1.0. 2019. URL: https://github.com/NREL/rosco.
[38] M. H. Hansen and L. C. Henriksen. Basic DTU Wind Energy controller. Tech. rep. DTU Wind Energy Report E-0018. DTU Wind Energy, 2013.
[39] N. J. Abbas, L. Pao, and A. Wright. “An Update to the National Renewable Energy Laboratory Wind Turbine Controller.” In: Journal of Physics: Conference Series (). In preparation.
[40] Laszlo Arany, S. Bhattacharya, John Macdonald, and S. J. Hogan. “Design of monopiles for offshore wind turbines in 10 steps.” In: Soil Dynamics and Earthquake Engineering 92 (2017), pp. 126–152. ISSN: 0267-7261. DOI: https://doi.org/10.1016/j.soildyn.2016.09.024. URL: http://www.sciencedirect.com/science/article/pii/S0267726116302937.
[41] Suresh C. Arya, Michael W. O’Neill, and George Pincus. Design of structures and foundations for vibrating machines. Gulf Pub Co, 1979.
[42] Johan N. Stander, Gerhard Venter, and Maarten J. Kamper. “Review of direct-drive radial flux wind turbine generator mechanical design.” In: Wind Energy 15.3 (2012), pp. 459–472. DOI: 10.1002/we.484.
[43] E. Smith. “DESIGN AV NACELLE FOR EN 10 MW VINDTURBIN.” MA thesis. Norwegian university of science and technology, 2012.
[44] Latha Sethuraman and Katherine Dykes. GeneratorSE: A Sizing Tool for Variable-Speed Wind Turbine Generators. Tech. rep. NREL/TP-5000-66462. National Renewable Energy Laboratory, 2017. URL: https://www.nrel.gov/docs/fy17osti/66462.pdf.
[45] Hung Vu Xuan. “Modeling of Exterior Rotor Permanent Magnet Machines with Concentrated Windings.” PhD thesis. 2012.
[46] Ion Boldea. Synchronous generators. CRC Press, 2015.
[47] Alasdair Stewart McDonald. “Structural analysis of low speed, high torque electrical generators for direct drive renewable energy converters.” PhD thesis. University of Edinburgh, 2008.
[48] P. C. J. Hoogenboom and R. Spaan. “Shear Stiffness and Maximum Shear Stress of Tubular Members.” In: Proceedings of the Fifteenth International Offshore and Polar Engineering Conference. International Society of Offshore and Polar Engineers. (Jan. 1, 2005). ISOPE-I-05-399. Seoul, Korea, 2005.

# 附录 A 叶片截面

本节给出叶片沿展向各截面的渲染图。70% 展向位置的截面见图 2-6。

图 A-1 0% 展向位置的叶片截面

图 A-2 10% 展向位置的叶片截面

图 A-3 20% 展向位置的叶片截面

图 A-4 30% 展向位置的叶片截面

图 A-5 40% 展向位置的叶片截面

图 A-6 50% 展向位置的叶片截面

图 A-7 60% 展向位置的叶片截面

图 A-8 80% 展向位置的叶片截面
图 A-9 90% 叶展处叶片截面

图 A-10 100% 叶展处叶片截面

# B 塔架与地基建模

## B.1 塔架数据

本节给出塔架截面特性参数的计算公式。图 4-3 中各符号的含义如下：

- 质量密度为 m
- 挥舞方向惯量为 m rix²
- 摆振方向惯量为 m riy²
- 挥舞方向刚度为 EIx
- 摆振方向刚度为 EIy
- 扭转刚度为 GK
- 轴向刚度为 EA

### B.1.1 测站位置 r [m]

沿塔架自底部起算的距离。陆上 HAWC2 模型中，塔架自 0 m 起、至 145.0 m 止，因此该塔架模型包含过渡段，过渡段范围为 0 m 至 15 m。

### B.1.2 单位长度质量 m [kg/m]

塔架单位长度质量：

m = ρA (B.1)

= ρπ[(D/2)² − (D/2 − t)²] (B.2)

式中，A 为截面面积，D 为外径，t 为该测站处的壁厚。

### B.1.3 质心位置 xm [m]

质心的 x 坐标。塔架为轴对称结构，故该值为零，即 xm = 0。

### B.1.4 质心位置 ym [m]

质心的 y 坐标。塔架为轴对称结构，故该值为零，即 ym = 0。

### B.1.5 回转半径 rix [m]

绕主弯曲轴 xe 的回转半径。截面质量惯性矩的计算需要用到回转半径，它是惯量计算的基础。对于各向同性圆管：

rix = √(Ix/A) (B.3)

= √{ (π[(D/2)⁴ − (D/2 − t)⁴]/4) / (π[(D/2)² − (D/2 − t)²]) } (B.4)

= √( (1/4)[(D/2)² + (D/2 − t)²] ) (B.5)

### B.1.6 回转半径 riy [m]

绕主弯曲轴 ye 的回转半径。由对称性可知，其值与 rix 相同。

### B.1.7 剪切中心 xs [m]

剪切中心的 x 坐标。截面关于 x、y 两轴均对称，故剪切中心与弹性中心重合（位于原点），即 xs = 0。

### B.1.8 剪切中心 ys [m]

剪切中心的 y 坐标。截面关于 x、y 两轴均对称，故剪切中心与弹性中心重合（位于原点），即 ys = 0。

### B.1.9 杨氏模量 E [Pa]

杨氏模量，取值见表 4-1。

### B.1.10 剪切模量 G [Pa]

剪切模量，取值见表 4-1。

### B.1.11 截面惯性矩 Ix [m⁴]

绕主弯曲轴 xe 的截面惯性矩：

Ix = ∫∫ x² dxdy (B.6)

= (π/4)[(D/2)⁴ − (D/2 − t)⁴] (B.7)

### B.1.12 截面惯性矩 Iy [m⁴]

绕主弯曲轴 ye 的截面惯性矩：

Iy = ∫∫ y² dxdy (B.8)

= (π/4)[(D/2)⁴ − (D/2 − t)⁴] (B.9)

### B.1.13 扭转刚度常数 K [m⁴/rad]

绕剪切中心处 z 轴计算的扭转刚度常数。截面取为圆形，故该常数与极惯性矩等价：

K = ∫∫ r² dxdy (B.10)

= (π/2)[(D/2)⁴ − (D/2 − t)⁴] (B.11)

### B.1.14 剪切折减系数 kx [-]

x 方向剪切的剪切系数，又称剪切折减系数。按文献 [48]，剪切系数取为：

kx = 1/2 + (3/4)(2t/D) (B.12)

### B.1.15 剪切折减系数 ky [-]

y 方向剪切的剪切系数，又称剪切折减系数。按文献 [48]，剪切系数取为：

ky = 1/2 + (3/4)(2t/D) (B.13)

### B.1.16 截面面积 A [m²]

截面面积：

A = ∫∫ dxdy (B.14)

= π[(D/2)² − (D/2 − t)²] (B.15)

### B.1.17 结构扭角 θs [deg]

x 轴与最接近 x 方向的主弯曲轴之间的夹角。塔架为轴对称结构，故该值为零，即 θs = 0。

### B.1.18 弹性中心 xe [m]

弹性中心的 x 坐标，弹性中心即两条主弯曲轴的交点。塔架关于 z 轴轴对称，故该值为 0，即 xe = 0。

### B.1.19 弹性中心 ye [m]

弹性中心的 y 坐标。塔架关于 z 轴轴对称，故该值为 0，即 ye = 0。

## B.2 地基模型

### B.2.1 竖向刚度

圆形结构地基的竖向刚度。单桩和塔架在轴向上相对较刚，有时可忽略该项：

ηz = 1 + 0.6(1 − ν)(h/r0) (B.16)

kz = [4Gr0/(1 − ν)] ηz (B.17)

### B.2.2 水平刚度

圆形结构地基的侧向刚度：

ηx = 1 + 0.55(2 − ν)(h/r0) (B.18)

kx = [32(1 − ν)Gr0/(7 − 8ν)] ηz (B.19)

### B.2.3 摇摆刚度

圆形结构地基的摇摆方向刚度：

ηψ = 1 + 1.2(1 − ν)(h/r0) + 0.2(2 − ν)(h/r0)³ (B.20)

kψ = [8Gr0³/(3(1 − ν))] ηψ (B.21)

### B.2.4 扭转刚度

圆形结构地基的扭转方向刚度：

kφ = 16Gr0³/3 (B.22)
