# 参考文献阅读清单（按阅读顺序编排）

> 课题：《基于阻抗控制的风浪融合机组互馈增益研究》。本清单共 21 篇，2026-11-16 编制，同日按 Saber 要求补充 2020 年以来前沿文献 3 篇（[17][18][20]）。
> 每条的出版信息（作者、题名、刊名/出版者、年份、卷期页码）均经公开检索逐条核对；DOI 只标注已核实者，未标注不等于不存在（专著与早期文献本无 DOI 或未逐字核到）。条目格式按 GB/T 7714 风格书写，可直接改编进论文参考文献表。

## 编排原则（为什么是这个顺序）

全表只有一条主线：**年份严格由老到新**（1950 → 2025，跨 75 年），同时内容由广入深，两条线是重合的——因为这个领域本身就是这样长起来的：

1. 先有"波浪对结构的作用力怎么算"（工程起点），才有"波浪能可以被振荡体吸收"（思想诞生）；
2. 吸收理论成立后，需要势流理论体系（辐射/绕射、多体相互作用）把它算出来；
3. 理论成熟后被系统化为"阻抗匹配 / 最优控制"——这是本课题核心章的理论母体，必须排在应用文献之前读，否则看不懂后面论文里 PTO 参数为什么那样设；
4. 然后浮式风机参考机型方法论与风浪混合概念出现、时域工具链落地；
5. 再落到本课题的两份基准定义（2020）；
6. 最后是与本课题几乎同题的最新工作（同平台、同方法、同"发电+减载互馈"命题），读它们是为了对照与找差异，不是为了模仿。

换序即乱的检验：把 [21] 提到最前面，读者没有阻抗最优的概念，无法判断其 PTO 设置的依据；把 [7] 放在 [3] 之前，最优吸收的效率上限从哪来就没有出处。按本顺序读，每一篇用到的概念都在前一篇里出现过。

时间分布：1950s 1 篇、1970s 3 篇、1980s 1 篇、1990s 1 篇、2000s 3 篇、2010s 4 篇、2020s 8 篇。前 13 篇（1950–2015）是经典与方法论骨架，分布均匀；2020s 的 8 篇里 2 篇是本课题基准定义（不可替换）、6 篇是前沿对照——这一段偏密是领域事实：半潜平台风浪混合的一体化研究本身主要出现在 2020 年以后，骨架段不受影响。

---

## 第一阶段：源头——波浪力与波浪能思想的诞生（1950–1977）

**[1]** MORISON J R, O'BRIEN M P, JOHNSON J W, et al. The force exerted by surface waves on piles[J]. Journal of Petroleum Technology, 1950, 2(5): 149-154.
> 定位：海洋工程波浪力的工程起点，Morison 方程（惯性力+拖曳力分解）的出处。本课题 AQWA 网格里的 Morison 单元、以及 W7 粘性阻尼 Morison 标定选项（选项 C）的源头。读它是为了知道"粘性/拖曳"这一支在整条路线里站在哪。

**[2]** BUDAL K, FALNES J. A resonant point absorber of ocean-wave power[J]. Nature, 1975, 256(5517): 478-479. DOI: 10.1038/256478a0
> 定位：波浪能思想的诞生点——首次提出让浮子在共振状态下吸收波浪能、且需要相位控制。篇幅只有两页，但本课题"阻抗控制"的全部想法都从这里发源。排在 Evans 之前是因为它是概念首发，Evans 是随后的理论化。

**[3]** EVANS D V. A theory for wave-power absorption by oscillating bodies[J]. Journal of Fluid Mechanics, 1976, 77(1): 1-25. DOI: 10.1017/S0022112076001109
> 定位：振荡体波浪能吸收的理论奠基：给出吸收效率的一般表达式与最优条件，是后面一切"最优吸收/最大俘获宽度"论证的引用源头。课题里谈 WEC 发电上限时引它。

**[4]** NEWMAN J N. Marine Hydrodynamics[M]. Cambridge: MIT Press, 1977.
> 定位：势流理论的体系化专著：辐射/绕射、附加质量与阻尼、Haskind 关系等都在此成体系。AQWA 求解的边值问题、以及本课题"系数可合成、RAO 不可合成"这类判断的理论依据都在这本书里。读在 Evans 之后，是因为先有具体突破、再读体系整理更易进入。

## 第二阶段：多体相互作用与工程载荷（1986–1990）

**[5]** KAGEMOTO H, YUE D K P. Interactions among multiple three-dimensional bodies in water waves: an exact algebraic method[J]. Journal of Fluid Mechanics, 1986, 166: 189-209.
> 定位：多体水动力相互作用的经典理论工作。本课题 19 体 AQWA 计算里的体间耦合块（361 个耦合块）不是数值花招，其理论根基就是这类多体相互作用方法。阶段 3 论文写多体方法时引它。

**[6]** FALTINSEN O M. Sea Loads on Ships and Offshore Structures[M]. Cambridge: Cambridge University Press, 1990.
> 定位：把势流理论落到工程载荷的专著：浮式结构运动、载荷与响应计算的工程口径。本课题阶段 4 由约束反力换算截面内力、做载荷校核时的方法背景。

## 第三阶段：波浪能理论的系统化——阻抗与最优控制（2002–2007）

**[7]** FALNES J. Ocean Waves and Oscillating Systems: Linear Interactions Including Wave-Energy Extraction[M]. Cambridge: Cambridge University Press, 2002.
> 定位：**本课题核心章的理论母体**。书中把振荡系统与电路类比，给出阻抗匹配与复共轭最优控制的系统表述——"阻抗控制"四个字的方法论出处就在这里。阶段 5 的 PTO 阻抗（阻尼+刚度）整定逻辑按此书立论。（注：2020 年有与 Kurniawan 合著的第 2 版，引用时用哪版须与正文一致。）

**[8]** FALNES J. A review of wave-energy extraction[J]. Marine Structures, 2007, 20(4): 185-201. DOI: 10.1016/j.marstruc.2007.09.001
> 定位：在专著之后的一篇领域综述：波浪能提取的物理极限、装置分类与控制需求的全景。读完 [7] 再读它，等于把理论放回领域地图里定位；写绪论的波浪能部分时引它。

## 第四阶段：参考机型方法论、混合概念与工具链（2009–2015）

**[9]** JONKMAN J, BUTTERFIELD S, MUSIAL W, et al. Definition of a 5-MW reference wind turbine for offshore system development[R]. NREL/TP-500-38060. Golden: National Renewable Energy Laboratory, 2009.
> 定位："参考机型"这一研究范式的源头文件：为什么要用公开定义的基准机型做研究、定义文件应包含什么。本课题用的两份 2020 基准（[14][15]）是它的直系后代；先读它，才知道 [14][15] 为什么长成那样。

**[10]** MULIAWAN M J, KARIMIRAD M, GAO Z, et al. Extreme responses of a combined spar-type floating wind turbine and floating wave energy converter (STC) system with survival modes[J]. Ocean Engineering, 2013, 65: 71-82.
> 定位：风浪混合系统的早期代表作（Spar 平台+同轴环式 WEC 的 STC 概念）。它证明了"风机平台与 WEC 一体化"从概念变成可计算的对象；本课题的混合命题排在它这一代工作之后。

**[11]** YU Y H, LAWSON M, RUEHL K, et al. Development and demonstration of the WEC-Sim wave energy converter simulation tool[C]//Proceedings of the 2nd Marine Energy Technology Symposium (METS 2014). Seattle: 2014.
> 定位：本课题时域工具链的出处：WEC-Sim 的多体动力学+BEM 输入架构在此发表。本课题 BEMIO→WEC-Sim 的整条链路、bodyClass/constraintClass 的建模方式都源于此。方法章节引它。

**[12]** RINGWOOD J V, BACELLI G, FUSCO F. Energy-maximizing control of wave-energy converters: the development of control system technology to optimize their operation[J]. IEEE Control Systems Magazine, 2014, 34(5): 30-55. DOI: 10.1109/MCS.2014.2333253
> 定位：能量最大化控制的权威综述：从复共轭/阻抗匹配到锁存、MPC 的控制技术谱系。[7] 给出理论最优，这篇给出"工程上怎么实现最优"的全景。阶段 5 选控制策略、说明为什么用阻抗（被动可实现）而非完全复共轭时引它。

**[13]** PÉREZ-COLLAZO C, GREAVES D, IGLESIAS G. A review of combined wave and offshore wind energy[J]. Renewable and Sustainable Energy Reviews, 2015, 42: 141-153. DOI: 10.1016/j.rser.2014.09.032
> 定位：风浪联合开发的领域地图：混合概念分类、协同收益与共址/一体化之争。绪论里交代"风浪融合"的研究谱系时引它；读完它，本课题在谱系中的位置（半潜平台一体化 WEC）自然清楚。

## 第五阶段：本课题的基准定义（2020）

**[14]** GAERTNER E, RINKER J, SETHI L, et al. Definition of the IEA Wind 15-megawatt offshore reference wind turbine[R]. NREL/TP-5000-75698. Golden: National Renewable Energy Laboratory, 2020.
> 定位：风机本体基准（转子 240 m、轮毂 150 m、额定风速 10.59 m/s）。原件 PDF 已存仓库 `references/`。全系统（状态 A）建模与阶段 5 风载工况的参数源。

**[15]** ALLEN C, VISSELLI A, DAGHER H, et al. Definition of the UMaine VolturnUS-S reference platform for IEA Wind 15-megawatt offshore reference wind turbine[R]. NREL/TP-5000-76773. Golden: National Renewable Energy Laboratory, 2020.
> 定位：平台基准（静水刚度表 3、无穷频率附加质量表 4、粘性阻尼表 5、全系统固有频率表 11）。原件 PDF 已存仓库 `references/`。本课题 GATE 1A 验收、W2 质量分账、W7 阻尼拆分的全部对照基准。与 [14] 同年同系列，必须成对出现，顺序按"先风机、后平台"与编号 75698 < 76773 一致。

## 第六阶段：同平台集成仿真与互馈前沿（2022–2025）

**[16]** SIRIGU M, FARAGGIANA E, GHIGO A, et al. Development of MOST, a fast simulation model for optimisation of floating offshore wind turbines in Simscape Multibody[J]. Journal of Physics: Conference Series, 2022, 2257(1): 012003. DOI: 10.1088/1742-6596/2257/1/012003
> 定位：与本课题工具链同源的集成仿真工作：MOST 在 Simscape Multibody 里建 15 MW + VolturnUS 平台模型并与 FAST 对标。它是路线 V2.5 里"MOST/BEMIO 边界"纠偏的直接对象，也是 WEC-Sim 应用生态里与本课题平台完全相同的一例。

**[17]** PETRACCA E, FARAGGIANA E, GHIGO A, et al. Design and techno-economic analysis of a novel hybrid offshore wind and wave energy system[J]. Energies, 2022, 15(8): 2739. DOI: 10.3390/en15082739
> 定位：[16] 同一团队（都灵理工大学）的应用层工作：用 MOST+WEC-Sim 工具链做风浪混合系统的设计与技术经济分析。读它是为了看集成仿真工具链在"设计一台混合装置"时实际怎么用，与本课题阶段 5 的建模组织方式可直接对照。

**[18]** ZHOU B, HU J, JIN P, et al. Power performance and motion response of a floating wind platform and multiple heaving wave energy converters hybrid system[J]. Energy, 2023, 265: 126314. DOI: 10.1016/j.energy.2022.126314
> 定位：方法与本课题最同构的一篇：半潜平台+多个垂荡点吸收 WEC，用高阶边界元+多体约束动力学求解（与 AQWA→WEC-Sim 约束装配是同一建模思想）；发现平台与 WEC 的"同步模式"下单 WEC 功率可提高 41.4%、总功率提高 26.7%——这是文献中对"互馈增益"最直接的量化先例之一，阶段 5 讨论增益机理时引它。

**[19]** CHEN Z, SUN J, YANG J, et al. Experimental and numerical analysis of power take-off control effects on the dynamic performance of a floating wind-wave combined system[J]. Renewable Energy, 2024, 226: 120353. DOI: 10.1016/j.renene.2024.120353
> 定位：与本课题核心命题最接近的实证工作：半潜浮式风机集成 3 个垂荡 WEC，系统研究 PTO 控制参数对动力性能的影响，结论是恰当控制下发电增益、运动抑制与塔基载荷降低可以同时取得——正是本课题"互馈增益"要量化论证的三维指标。阶段 5 的对照与差异讨论以它为第一参照。

**[20]** XU S, JI B, XU F, et al. Dynamic response and power performance of a combined semi-submersible floating wind turbine and point absorber wave energy converter array[J]. Renewable Energy, 2024, 237: 121903. DOI: 10.1016/j.renene.2024.121903
> 定位：半潜平台+6 个环式点吸收 WEC 阵列，三维势流计算，系统考察 PTO 阻尼、WEC 浮子形状与季节变化（总功率较原系统高 2.5%–6.5%，PTO 阻尼主要影响垂荡与平均功率峰位）。与 [19] 互补：[19] 偏控制参数的影响，本篇偏阵列构型与阻尼的参数规律；本课题外柱多 WEC 布置与阻尼扫描可参照其参数组织。

**[21]** GU X, LIN F, JIANG W, et al. Power performance and dynamic characteristics of a 15 MW floating wind turbine with wave energy converter combined concept[J]. Sustainable Horizons, 2025, 13: 100125. DOI: 10.1016/j.horiz.2024.100125
> 定位：最新且平台完全相同的工作：UMaine VolturnUS-S + IEA 15 MW 平台立柱集成 4 个环式垂荡 WEC，全耦合时域分析（额定工况纵摇幅值降低 31.5%、波浪能约占年发电量 11.4%）。作为全表收尾：读完它，本课题与当前前沿的差距与差异点（本课题走 AQWA 多体截面力+阻抗控制路线、且关注横撑截面载荷）应当能自己说清。

---

## 使用说明

1. 论文参考文献表若采用顺序编码制，编号顺序应与正文首次引用顺序一致；本清单的顺序是**阅读顺序**，写正文时让引用大体沿此顺序首次出现，即可两用。
2. [14][15] 原件已在仓库 `references/`；其余期刊/会议文献按 DOI 或报告号检索获取；[4][6][7] 为专著，走图书馆渠道。
3. 本清单是"应读且可引"的精选，不是穷举。后续阶段（尤其阶段 5 动笔前）如需补控制理论或截面结构校核方向的文献，另行增补并在本文件留痕，不改动现有编号顺序。
