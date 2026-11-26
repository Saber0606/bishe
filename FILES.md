# 文件清单

仓库按阶段编号组织（结构图见 `README.md` 的「仓库结构」一节）。本表按当前路径登记仓库文件树内的全部 117 个文件（另有 16 体 `.AH1` 一个文件待网页上传入仓，见 03-multibody-16body 节），另有 3 组大文件以 Release 附件存放（见文末）。

入仓通道说明（2026-11-13 起，Saber 定：毕设相关文件一律入仓）：文本文件走连接器快照推送；二进制文件 ≤25 MB 走 GitHub 网页上传；超过 25 MB 的走 Release 附件。原先因文本通道限制未入仓的二进制文件已于 2026-11-13 全部补齐。

## 根目录（总览）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `AGENTS.md` | 接手说明（2026-11-13 新增）：供接入本仓库的 AI / 协作者先读——项目内容、进度快照（带证据出处）、文件分类、下一步工作队列、口径红线与同步纪律 |
| `README.md` | 仓库总览（题目、技术主线、仓库结构、当前进度、参考基准） |
| `PROGRESS.md` | 进度记录（阶段进度、19 体验证结论、后续待办、易混口径备忘） |
| `FILES.md` | 本文件 |
| `.gitignore` | 仅忽略系统垃圾与本地同步元数据（二进制成果文件自 2026-11-13 起正常入仓，不再排除） |

## 00-route（全程执行路线）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `00-route/technical-route-v2.5.md` | 技术路线（现行版 **V2.7**，2026-11-25 覆盖更新：对齐 16 体主线、W7 直连 `MOST` 全系统合并 GATE 1B、阶段 4 并入 `Baseline 0`、阶段 5 定型为外柱干舱内置惯性式 WEC/馈能 TMD `nonHydro=1` 免重跑 AQWA；含 §九可选柔性铰；沿用原路径防断链） |

## 01-single-body-validation（阶段 1：整体纯浮体验证）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `01-single-body-validation/gate1a-verification-report-brief.md` | 《浮体模型验证报告（简明版）》（2026-11-08，GATE 1A 验证报告）的文本转存版：15 项可比指标全过，几何/静水最大偏差 0.51%、固有频率最大 1.8% |
| `01-single-body-validation/gate1a-verification-report-brief.docx` | 上条报告的 `.docx` 原件（132,150 B，2026-11-13 经网页上传补入，与 `.md` 转存版同目录并存） |
| `01-single-body-validation/output/FUTI_LOWFREQ.LIS` | 整体单体模型（阶段 1A）AQWA 实跑输出原件（5,095,547 B，AQWA-Line 2022 R1，2026-11-08 运行；2026-11-13 由 Saber 补交）：5,454 面元、排水量 20,157.8 m³、K33 4.46027×10⁶，与 GATE 1A 基准逐项吻合；含 FK / 绕射 / 合并三套激励力表，是 GATE-A 相位修正符号裁决的外部基准（见 `03-multibody-19body/gate-a-verification/sign-adjudication-record.md`） |
| `01-single-body-validation/output/futi_lowfreq.dat` | 上条运行的 AQWA 输入 Deck 原件（927,444 B，2026-11-13 由 Saber 补交） |

## 02-two-body-segmentation（阶段 2：二体切分）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `02-two-body-segmentation/pontoon-splitting-plan-v2.md` | 《阶段2_浮筒切分划分方案_V2》（2026-11-08）：180° 浮筒盒选规则、Body 2 = 1,507 面元、m₂ = 3,870 t、CoG₂ (−42.8, 0, −14.1)，含 dat 改法操作手册与 GATE 2 一级验收表 |
| `02-two-body-segmentation/cross-ai-review-package.md` | 《阶段2_分段方案_跨AI复核包》（2026-11-08）：供独立复核的背景、参数出处与 10 个复核问题 |
| `02-two-body-segmentation/interface-nodes.csv` | 阶段 2 界面节点清单：32 个界面节点坐标与 Body 2 侧新编号 20001–20032 映射 |

## 03-multibody-19body（阶段 3：19 体多体链路）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `03-multibody-19body/plan-22body-superseded/segmentation-plan-v1.2.md` | 《阶段3_22体分段与多体链路计划书》V1.2（2026-11-11）：W1–W7 工作包与 GATE-A/B/C 验收门。**口径已确认（2026-11-13，Saber）**：计划原为 22 体（3 浮筒 × 6 段 + 中心柱 + 3 外柱、21 截面），实际改为 **19 体**执行（每筒 5 段 + 外柱）；Saber 所述理由是 AQWA 多体数量上限约 20 个结构、22 体超限（此上限数值尚未独立核实）。计划书文件头已加变更说明，按历史计划存档；执行口径以 19 体为准，其 W1–W7 / GATE-A·B·C 框架沿用 |
| `03-multibody-19body/design-basis-w1-w2/w1-segmentation-scheme-19body.md` | W1 分段方案（复原版，2026-11-13）：W1 原件遗失后据实跑 AH1/LIS 复原——三浮筒各均分 5 段（段长 7.6014 m，段界径向 7.409–45.416 m）+ 四立柱各一体 = 19 体编号表、18 道界面清单（W7 约束对应表） |
| `03-multibody-19body/design-basis-w1-w2/w2-mass-accounting-19body.md` | W2 质量分账（复原版，2026-11-13）：W2 原件遗失后复原——质量要求结合 NREL/TP-5000-76773 浮体参数（总 17,854 t = 钢 3,914 + 固定压载 2,540 三等分置外柱柱底 + 流体压载 11,300 灌浮筒 + 接口 100 t）与浮体验证报告；实跑分账取自 AH1 全精度（每体质量/重心/惯量），三笔账核对通过（总质量 +0.0003%、惯量 −0.35%/−1.42%） |
| `03-multibody-19body/design-basis-w1-w2/19body-property-allocation.md` | 19 体各物理性质分配说明（2026-11-16，AQWA 复盘产出）：性质分三类——人工分配（质量/重心/惯量：论文表 2 总量 + 构件布置规则 → 逐体点质量，三笔账验证）、求解器按几何算出（静水刚度/附加质量/激励力，只做合成验证，含 corr+ 相位修正与 A∞ 对论文表 4 比对）、尚未分配（表 5 粘性阻尼，待 W7 拍板）；含计算过程与论文比对总表，配图 4 张在同目录 `figs/` |
| `03-multibody-19body/design-basis-w1-w2/19body-property-allocation.docx` / `.pdf` | 上条说明文档的 Word / PDF 版（图片内嵌于文件本体，便于离线阅读与论文摘录；内容与 .md 版一致） |
| `03-multibody-19body/design-basis-w1-w2/figs/fig1-layout.png` | 配图 1：19 体切分布局俯视图（编号与 W1 编号表一致） |
| `03-multibody-19body/design-basis-w1-w2/figs/fig2-composition.png` | 配图 2：质量构成双图（按成分=论文表 2 / 按部位=19 体实跑汇总） |
| `03-multibody-19body/design-basis-w1-w2/figs/fig3-mass-by-body.png` | 配图 3：逐体质量分布柱状图（总计 17,854.06 t） |
| `03-multibody-19body/design-basis-w1-w2/figs/fig4-paper-deviation.png` | 配图 4：与论文数据比对偏差汇总图 |
| `03-multibody-19body/gate-a-verification/19body-synthesis-verification.md` | 19 体合成验证记录（原文文件名为 `19BODY_合成验证记录.md`，2026-11-13 验证通过一级合成验收口径） |
| `03-multibody-19body/gate-a-verification/sign-adjudication-record.md` | GATE-A 相位修正符号裁决记录（2026-11-13）：以整体单体 LIS 为外部基准全谱比对，裁定 corr+（计划书公式）正确、corr− 排除（中位复数误差 0.102% 对 96.6%）；`verify_19body.py` 的 corr− 抽查列作废；附低频（ω≤0.15）力矩残差带观察项（≤峰值约 5%，W6 同频段复查） |
| `03-multibody-19body/gate-a-verification/adjudicate_sign.py` | 符号裁决脚本（解析 LIS 合并激励力表与 `.npz` 三变体全谱比对） |
| `03-multibody-19body/gate-a-verification/verify_19body.py` | 19 体合成验证脚本（运行时需与被验 `futi_19body.AH1` 同目录） |
| `03-multibody-19body/gate-a-verification/synthesis_log.txt` | 合成验证运行日志 |
| `03-multibody-19body/gate-a-verification/synthesis_results.json` | 合成验证结果数据 |
| `03-multibody-19body/gate-a-verification/excitation-full-spectrum-note.md` | 激励力全谱合成参考记录（2026-11-13，W5 / GATE-A 最后一项）：25 浪向 × 47 频点 × 6 自由度全谱合成，长波极限通过；计划书（corr+）与验收脚本（corr−）的符号矛盾已由 `sign-adjudication-record.md` 裁决为 corr+（裁决前状态：最不利点 My 相差约 13 倍）；AQWA“约 20 体上限”经核查无官方出处（公开资料称上限 50 结构）；含复核记录与 W6 预飞检查单 |
| `03-multibody-19body/gate-a-verification/excitation-full-spectrum.py` | 全谱合成脚本（可重复运行；与 `verify_19body.py` 抽查点逐位一致） |
| `03-multibody-19body/gate-a-verification/excitation-full-spectrum.csv` | 全谱合成参考数据表（1,175 行：逐浪向/频点的 corr+ / corr− 幅值与相位 + naive 幅值） |
| `03-multibody-19body/gate-a-verification/excitation-full-spectrum.json` | 全谱合成汇总指标（RMS、最不利点、长波极限、120° 对称性检验） |
| `03-multibody-19body/gate-a-verification/excitation_full_spectrum.npz` | 全谱合成的复数数据存档（340,528 B：naive / corr+ / corr− 三变体复数合成力，形状 25×47×6；与上表 `.csv` 为同一数据的二进制版，2026-11-13 按“毕设文件一律入仓”的新政策经网页上传补入） |
| `03-multibody-19body/gate-a-verification/dat-deck-check-record.md` | 19 体 dat Deck 级核查记录（2026-11-16，W3 关闭件）：Saber 补交 `futi_19body.dat` 后逐 Deck 核查——Deck 01 节点集与整体 dat 对照（新增 602 个界面复制节点 + 18 个 PMAS 节点、99999 复用）、Deck 02 逐块面元数与 LIS 逐结构计数逐个相等、Deck 03 质量与 Deck 04 惯量与 AH1 实跑分账在 dat 精度内逐个相等、仅用 dat 重算三笔账与 AH1 口径一致；**Deck 级核查通过**。附更正：W1 复原表中体 17 的 DIFF 面元 196 为转录笔误，正确值 198（dat 与 LIS 两处一致；W1 表逐体相加 5,452≠其自述总数 5,454 的矛盾由此消除；合成验证记录的组行列示本就是 198，无此误；不影响任何计算结论）。附实证结论：dat 全文无单体内钢/压载成分分拆，W2 原始分配过程仍不可复原 |
| `03-multibody-19body/gate-a-verification/dat-deck-check.py` | 上条核查的解析脚本（解析 Deck 01–06 并与 W2 分账 / W1 分段表 / 整体 dat / LIS 计数对照，可重复运行） |
| `03-multibody-19body/gate-a-verification/dat-deck-check-results.json` | 上条核查的结果数据（逐体对照、逐块面元、三笔账重算值） |
| `03-multibody-19body/gate-a-verification/output/futi_19body.dat` | 19 体运行的 AQWA 输入 Deck 原件（976,953 B，2026-11-15 由 Saber 补交；ANSYS 2022 R1 于 2026-11-03 导出底稿 + W3 组装，SHA-256 `a1f87ca0…`；Deck 级核查见 `../dat-deck-check-record.md`） |
| `03-multibody-19body/gate-a-verification/output/FUTI_19BODY.MES` | AQWA 原始消息文件（1,265 条全部为 WARNING，0 ERROR / FATAL） |
| `03-multibody-19body/gate-a-verification/output/futi_19body.AH1` | AQWA 水动力数据库原件（21,146,564 B，2026-11-13 经网页上传补入；BEMIO 的输入） |
| `03-multibody-19body/gate-a-verification/output/futi-19body-run-bundle.zip` | 本次运行的原始打包件（21,638,174 B，内含 `FUTI_19BODY.LIS` + `futi_19body.AH1`，2026-11-13 经网页上传补入） |
| `03-multibody-19body/gate-b-verification/gate-b-verification-record.md` | GATE-B 复核记录（2026-11-15）：W6 产出 `.h5` / hydro.mat 经 SHA-256 校验链下载复核——合成激励力对 corr+ 锚幅值最大偏差 0.357%、相位最大 0.168°（判据 <1% / <1°），A/B 矩阵与 AH1 逐元素一致，Ainf 由 radiationIRF 重算确认、与 NREL 表 4 偏差 ≤2.24%，body 顺序/重心逐位一致；**GATE-B 通过**。含 BEMIO 激励力相位约定（共轭 + 参考点换算）的识别与逆变换说明、GATE-A 低频残差带复查结论（不复现，源于分体口径而非 BEMIO） |
| `03-multibody-19body/gate-b-verification/gate-b-check.py` | GATE-B 复核脚本（计算部分与实跑脚本逐字相同，输入来源对应关系见脚本头注） |
| `03-multibody-19body/gate-b-verification/gate-b-results.json` | GATE-B 复核结果数据（激励力两级比对、A/B 矩阵、Ainf、结构项汇总指标） |
| `03-multibody-19body/w6-bemio/bemio_futi_19body.m` | W6 BEMIO 生成脚本（REV 1，2026-11-15）：readAQWA → radiationIRF → excitationIRF → writeBEMIOH5，产出 `futi_19body.h5`；体序以 W1 编号表为准（19 体、361 耦合块、47 频点 0.02–2.10 rad/s、25 浪向）；含 hydro.Nb 体数/频点检查、hydro.file 基名断言（writeBEMIOH5 写出 `[hydro.file '.h5']`，已据 WEC-Sim 源码核实）、读入后检查点保存与 Ainf 记录点。2026-11-15 首次运行：readAQWA 成功（252.8 s，R2025a Update 1），IRF/写出未跑；REV 1 于当日 14:27 重跑完成并产出 `futi_19body.h5`，GATE-B 复核已通过（2026-11-15，见 `../gate-b-verification/`）。文件名用下划线是 MATLAB 可运行名的例外（见脚本头注释） |
| `03-multibody-19body/w6-bemio/output/README.md` | W6 运行产出存放说明（2026-11-15 建）：登记各产出文件的存放位置与状态；大文件（.h5 / 完整 hydro.mat）以 ZIP 形式存于 Release（实际标签 `W6-output`），SHA-256 已登记在本文件末节；GATE-B 复核记录在 `../../gate-b-verification/` |
| `03-multibody-19body/w7-wecsim-assembly/w7-damping-split-options-pending.md` | W7 前置决策备案（2026-11-15 入仓，**待 Saber 拍板、未定口径**）：表 5 二次粘性阻尼拆到 19 体的三选项——A 按迎流投影面积拆分（草稿推荐：平动对角逐体值已算清、全精度加总与表 5 精确一致，转动/交叉项由刚体输运产生）/ B 表 5 整体等效不拆（退路）/ C 逐体 Morison Cd 标定；含表 5 原值回源（NREL 76773 p. 12）、参考点在 SWL 塔轴与四工况出处的核实、GATE-C 验证集与入仓复核记录。源稿为 2026-11-13 本地决策草稿，入仓版已按 GATE-B 通过后的状态更新 |
| `03-multibody-19body/w6-bemio/output/bemio_futi_19body_log.txt` | W6 BEMIO 运行日志（2026-11-15，Saber 网页上传，5,023 B）：含初版脚本失败运行（文件名断言）与 REV 1 成功运行两段记录；REV 1 段为运行证据——readAQWA 255.6 s、Nb = 19、DOF = 114、radiationIRF 96.9 s、excitationIRF 32.5 s、writeBEMIOH5 13.5 s、产出 `futi_19body.h5` 155,612,740 B；含 Ainf 在 readAQWA 后与 radiationIRF 后的两组打印值（GATE-B 核查材料） |
| `03-multibody-19body/gate-a-verification/lis-waveforce-sum-check.md` | GATE-A 补充核查记录（2026-11-16）：Saber 提问"19 体 LIS 逐体波浪力复数相加应等于整体同频率值"——解析 19 体 LIS 全部 475 个 FK+绕射合并力表块与整体单体 LIS 25 个块、两端都用印刷值独立复现：字面直接相加全谱复数误差中位 99.99%（不成立），补每体相位修正 exp(+ik·r) 与力矩平移到总重心后（corr+ 口径）中位 0.168%，印刷精度内成立；含术语指认（力表可叠加、运动 RAO 表不可逐体求和）与小量相消通道的判读说明；与符号裁决记录（AH1 口径 0.102%）互为交叉验证 |
| `03-multibody-19body/gate-a-verification/check-lis-waveforce-sum.py` | 上条核查的解析脚本（解析两份 LIS 的合并力表、三种求和口径全谱比对；输入路径为执行时本机路径，对应关系见记录文件） |
| `03-multibody-19body/gate-a-verification/check-lis-waveforce-sum-results.json` | 上条核查的结果数据（抽查点逐通道复数误差 + 全谱掩膜统计） |

## 03-multibody-16body（阶段 3 更正：16 体多体链路，2026-11-16 新建）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `03-multibody-16body/design-basis-w1-w2/w1-segmentation-scheme-16body.md` | 更正 W1 分段方案（设计版，2026-11-16；**v2 修订 2026-11-16 晚**：面积改逐片精确裁切、计数改 W3 劈分片数、补端截面站位定义、合计面积订正、文件尾部截断污染修复，详见文件内 v2 修订注）：Saber 与导师商定浮筒由均分 5 段改均分 **4 段**——5 段时浮筒 1/2 处（径向 26.4125 m）落在段内、无界面不可验证；4 段段长 9.50175 m、中点恰为段界（已核精确相等）。16 体编号表（中央柱 1、每链 4 段 + 外柱）、15 道界面清单；含相互作用组上限 20 的出处核查（16 ≤ 20 满足、22 体方案排除成立，2022 R1 原文待版本对齐）。**推导依据（同日晚修订版）**：逐体几何量（面元/DIFF/表面积/排水体积/浮心）全部由整体单体 dat `futi_lowfreq.dat` 的网格独立实测——浮筒面元按切平面逐片精确裁切积分，12 段体积同为 831.40 m³（等截面自证），总量对该 dat 的 LIS 核对：排水体积 20,157.85 vs 20,157.8 m³、总浮心 z −13.6394 vs −13.6393 m；不参照 19 体实跑结果 |
| `03-multibody-16body/design-basis-w1-w2/w2-mass-accounting-16body.md` | 更正 W2 质量分账（设计版，2026-11-16；**v2 修订 2026-11-16 晚**：按 W1 v2 精确面积重解——段 961.5 t、外柱 1,731.9 t、中央柱 1,120.1 t，Ixx/Iyy 独立核查 +0.70%，详见文件内 v2 修订注）：总账锚点 = 整体单体 dat 的 Deck 03/04（17,854 t、重心 −14.940、惯量 1.251×10¹⁰ / 2.367×10¹⁰），构成 = NREL 表 2（钢 3,914 + 固定压载 2,540 + 流体压载 11,300 + 接口 100）；按构件放置规则（固定压载柱底成块、流体灌满浮筒 φ=1 余量入柱底、钢按表面积比例为基准）分配，再以三笔账（质量/重心 z/Izz）做最小修正闭合；独立核查 Ixx/Iyy +0.70%/+0.70%（判据 <2%）。逐体（v2）：段 961.5 t、外柱 1,731.9 t、中央柱 1,120.1 t；明示设计值待实跑、钢份额闭合不唯一的边界。不参照 19 体实跑分账（同日早先的重叠重组版未入仓、已被本版取代，见 PROGRESS 留痕） |
| `03-multibody-16body/design-basis-w1-w2/design-16body-from-singlebody-geometry.py` | W1 几何推导脚本（v2：表面积/面积形心改逐片精确裁切）：解析整体单体 dat 的 Deck 01/02，逐面元归属构件、浮筒面元按切平面精确裁切后散度积分（可重复运行；输入路径为执行时本地路径，仓库对应文件见 W1 §2） |
| `03-multibody-16body/design-basis-w1-w2/design-16body-from-singlebody-geometry-results.json` | W1 几何推导结果 v2（逐体面元/DIFF/精确面积/体积/浮心与总量核对；含 v1 质心口径面积备查） |
| `03-multibody-16body/design-basis-w1-w2/design-16body-w2-allocation.py` | W2 分账脚本（v2：输入 W1 v2 几何）：构件放置规则 + 三笔账最小修正闭合求解、三笔账合成核对（输入为上条几何结果 JSON，可重复运行） |
| `03-multibody-16body/design-basis-w1-w2/design-16body-w2-allocation-results.json` | W2 分账结果数据 v2（逐体质量/重心/惯量、构件份额与合成总量） |
| `03-multibody-16body/w3-dat-assembly/w3-assembly-check-record-16body.md` | 更正 W3 组装与核查记录（v2 劈分版，2026-11-16 晚）：组装方法（整体单体 dat 切分 + I-1/I-3 六平面劈分 195 元 + EL10 式表头）、组装统计（面元 7,140、DIFF 碎片 5,651、复制节点 506）、独立核查 29/29、逐体体积残差归因、今晚试运行核对点。**2026-11-16 晚附记 §6（实跑与关门）**：v2/v3 两版试运行均死于 Deck 8 读入 EOF，Argon 修复版实跑成功并经 as-run 核查，**W3 关闭**；实跑 dat 已入仓 `w3-dat-assembly/output/`（见下行） |
| `03-multibody-16body/w3-dat-assembly/assemble-16body-dat-v2.py` | W3 v2 组装脚本：在整体单体 dat 上切分 16 体、劈分跨 I-1/I-3 面元、按 W2 v2 填 Deck 03/04（可重复运行；内部路径为执行时本地路径） |
| `03-multibody-16body/w3-dat-assembly/check-16body-dat-v2.py` | W3 v2 独立核查脚本：重解析写出的 dat，核对结构/计数/Deck 03-04/三笔账/逐体体积面积/劈分节点位置（29 项） |
| `03-multibody-16body/w3-dat-assembly/assemble-16body-dat-v2-manifest.json` | W3 v2 组装清单（dat MD5、逐体片数、劈分统计） |
| `03-multibody-16body/w3-dat-assembly/output/futi_16body.dat` | 更正 W3 **实跑定版** dat（2026-11-16 20:33 AQWA 实跑成功）：Muse v2 组装 → Argon 修复（Deck 05/06 表头尾注释去除、末尾补 Deck 09–18 NONE、全部单元行改 80 字符式等，血统与 as-run 核查见 W3 记录 §6）；987,594 B，MD5 `5cbc0e8475fb84f2acc553fca0b63bdd`，SHA-256 `128d27b111c33ebb6cdf2c05c530e619568e6ab0059e94026d650429aeafb8b8`；按 Saber 2026-11-16 指示统一命名（上传原名 `futi_16body_fixed.dat`）。v2/v3 两版（MD5 `8c77dcf0…` / `01dcdd8e…`）试运行死于 Deck 8 EOF、未入仓，本地保留 |
| `03-multibody-16body/w4-aqwa-run/w4-run-check-record-16body.md` | 更正 W4 求解与运行产物核查记录（2026-11-16）：`.MES` 清点 1,064 条 WARNING 分 7 类、0 ERROR/FATAL；`.LIS` 逐结构核查——DIFF 计数 16/16 与 W3 清单一致（Σ 5,651）、逐体质量/重心对 W2 v2 设计、装配总量 Σ 排水 20,157.83 m³ / Σ K33 4.46024×10⁶ / 体积加权浮心 z −13.6393 与整体单体基准一致；含逐体网格排水体积的开口归属口径说明（−0.83%…+2.08%，总量精确，非网格错误） |
| `03-multibody-16body/w4-aqwa-run/check-lis-w4.py` | W4 LIS 核查脚本：解析 16 个静水块与绕射建模检查块，逐体对 W1/W2 v2 设计表与 W3 清单、合成总量对整体单体 LIS 基准（可重复运行） |
| `03-multibody-16body/w4-aqwa-run/output/futi_16body.MES` | 16 体实跑求解器消息原件（321,555 B，5,257 行，MD5 `eed20cbb0ec6c4d772e3757d5e7a9e35`，SHA-256 `5925f40171446275353d4e822f3ce71cdc1edabbf48f8200dd7dbbe745304776`）：0 ERROR/FATAL；按 Saber 指示统一命名（上传原名 `FUTI_16BODY_2.MES`） |
| `03-multibody-16body/w4-aqwa-run/output/futi_16body.AH1` | 16 体实跑水动力数据原件（15,506,571 B，MD5 `cb2d1c4477df8bdfdb3c55804bb54206`，SHA-256 `a997f35c146f7919850bf84f2dc12db8490e019db19ed4f6b6f084a136b86616`）：**二进制 ≤25 MB，待网页上传入仓本目录**（本地原件已核验登记；上传原名 `futi_16body_3_i6na.AH1`）；W5/GATE-A 与 W6/BEMIO 的输入 |
| `03-multibody-16body/gate-a-verification/gate-a-verification-record-16body.md` | 更正 W5 / **GATE-A 关门记录**（2026-11-16）：AH1 三笔账（逐体对 W2 v2 在印刷精度内一致；合成总量——质量 +0.0009%、重心 z +0.00003 m、Izz +0.001%、独立核查 Ixx/Iyy +0.698% <2%）；激励力 corr+ 全谱合成对整体单体基准（5,745 掩膜点）中位复数误差 **0.104%**、相位中位 0.004°，corr− 95.7% / naive 102.9% 排除；LIS 印刷版独立核查 0.172%；低频残差带复测（≤6.04×10⁶ N·m/m、约峰值 5.4%，与 19 体同量级，处置沿 19 体）；含 K44/K55 输运方法学更正（同余输运 −3.84% 为方法受限、直接水线面聚合 −0.165%/−0.055% 为准） |
| `03-multibody-16body/gate-a-verification/verify-16body-ah1.py` | W5 三笔账脚本：解析 16 体 AH1 的 COG/COB/DISPLACEMENT/MASS/HYD，逐体对 W2 v2 分账 JSON、合成总量对单体 Deck 03/04 锚点，附静水刚度（两法）、附加质量抽查与固有频率（可重复运行；内部路径为执行时本地路径） |
| `03-multibody-16body/gate-a-verification/ah1-three-accounts-results.json` | 三笔账结果数据（逐体质量/重心/惯量偏差、合成总量、K33/K44/K55 两法、附加质量抽查频点、固有频率） |
| `03-multibody-16body/gate-a-verification/excitation-full-spectrum-16body.py` | W5 激励力全谱脚本：AH1 FORCERAO 三变体（naive/corr+/corr−）合成至总重心 + 与整体单体 LIS 合并表全谱裁决（5% 掩膜、逐自由度/分频段/低频带统计，可重复运行） |
| `03-multibody-16body/gate-a-verification/gate-a-adjudication-results.json` | 激励力裁决结果数据（三变体统计、corr+ 逐自由度与分频段、最不利点、抽查点、低频带逐通道） |
| `03-multibody-16body/gate-a-verification/excitation-full-spectrum-16body.npz` | 16 体激励力合成参考数据（25 浪向 × 47 频 × 6 自由度，三变体复数阵 + 合成重心）：**GATE-B 的 corr+ 对照锚**；二进制走网页上传 |
| `03-multibody-16body/gate-a-verification/excitation-full-spectrum-16body.csv` | 同上数据的表格版（逐浪向/频点的 corr+/corr− 幅值相位与 naive 幅值） |
| `03-multibody-16body/gate-a-verification/check-lis-waveforce-sum-16body.py` | LIS 印刷精度独立交叉核查脚本：16 体 LIS 逐结构 FK+绕射合并表（400 块）三法（plain/transfer/corr+）合成对整体单体 LIS（可重复运行） |
| `03-multibody-16body/gate-a-verification/check-lis-waveforce-sum-16body-results.json` | LIS 交叉核查结果（corr+ 中位 0.172%、plain 99.99%、transfer 102.97%） |
| `03-multibody-16body/w6-bemio/bemio_futi_16body.m` | 更正 W6 BEMIO 脚本（2026-11-16 备妥，**已于同日 23:11 由 Saber 在本地 MATLAB 运行成功**）：由已实跑通过的 19 体 REV 1 脚本机械适配（Nb=16、DOF=96、256 耦合块；hydro.file 基名 / hydro.Nb / 读后检查点等 REV 1 经验全数沿袭）；输入 = 本地 `futi_16body.AH1` + `futi_16body.LIS`，输出 `futi_16body.h5` + hydro.mat + 日志（产出存放见同目录 `output/README.md`） |
| `03-multibody-16body/w6-bemio/output/README.md` | 更正 W6 运行产出存放说明（2026-11-16 建）：登记各产出文件的存放位置与校验值；大文件（.h5 / hydro.mat）以 ZIP 形式存于 Release `16-output`，SHA-256 已登记在本文件末节；GATE-B 复核记录在 `../../gate-b-verification/` |
| `03-multibody-16body/w6-bemio/output/bemio_futi_16body_log.txt` | 更正 W6 BEMIO 运行日志（2026-11-16 23:11，Saber 回传，2,043 B，MD5 `0442effbbd6f992a6b070febeef24928`）：readAQWA 162.7 s、Nb = 16、DOF = 96、radiationIRF 66.9 s、excitationIRF 28.3 s、writeBEMIOH5 11.9 s、产出 `futi_16body.h5` 115,902,180 B；含 Ainf 在 readAQWA 后与 radiationIRF 后的两组打印值（GATE-B 核查材料） |
| `03-multibody-16body/gate-b-verification/gate-b-verification-record-16body.md` | 更正 W6 / **GATE-B 关门记录**（2026-11-16）：被验文件校验链（zip 与 GitHub digest 一致、解压实测）；BEMIO 激励约定在 16 体再证；逐体激励逆变换后对 AH1 中位 2.0×10⁻¹⁶；合成对 GATE-A corr+ 锚**幅值 max 0.386%、相位 max 0.187°**（最不利点全在 Mz 相消通道）；**低频带（ω ≤ 0.15）幅值 max 0.0018%——GATE-A 残差带不复现**；A/B 对 AH1（B 最差 4.8×10⁻⁸）；Ainf 对 NREL 表 4（+1.30/−0.80/−0.99/−0.99/+2.24/+0.34%）、对称残差 1.00×10⁻³；结构项（cg 逐位一致、ΣK33 与 GATE-A 一致到印刷精度、Σ 排水 +0.0002%） |
| `03-multibody-16body/gate-b-verification/gate-b-check-16body.py` | GATE-B 复核脚本：结构项 + 逐体激励逆约定比对 + corr+ 合成对锚（全谱与低频带）+ A/B 对 AH1 + Ainf 三项（可重复运行；内部路径为执行时本地路径） |
| `03-multibody-16body/gate-b-verification/gate-b-results-16body.json` | GATE-B 复核结果数据（结构项、逐体/合成激励统计、A/B 最差值、Ainf 对表 4 逐项偏差） |
| `03-multibody-16body/gate-b-verification/gate-b-synthesis-16body.npz` | GATE-B 合成数据（h5 口径合成阵 Fsyn_h5 + 逆变换逐体阵 Frec，25 浪向 × 47 频 × 6 自由度）：二进制，**待网页上传入仓本目录** |
| `03-multibody-16body/w7-wecsim-assembly/w7-damping-decision-annex-16body.md` | W7 前置决策附件（16 体，2026-11-17，决策过程记录；**口径已于 2026-11-21 定案**，见阻尼方案三行）：导师置零建议（选项 D，Saber 转述）与前提核查（分布不可核验成立 / 整体可核验不成立，附 GATE-A 与 GATE-C 证据）；共振量级实算（ζ_rad 垂荡 0.012% / 纵摇 0.087% vs 表 5 ζ_visc 2.16% / 1.02%，置零峰值高估约 ×186 / ×12.7）；选项 A 的 16 体投影面积份额与逐体 Bq（方法经 19 体备案复现验证）；四选项对照与待定事项 |
| `03-multibody-16body/w7-wecsim-assembly/area-shares-16body.py` | 选项 A 的 16 体逐体投影面积份额计算脚本：与 19 体备案同一方法，先以 5 段几何复现备案全部公布值验证，再算 4 段 16 体（可重复运行） |
| `03-multibody-16body/w7-wecsim-assembly/area-shares-16body.json` | 同上结果数据：三向总账（2,160.81 / 2,138.32 / 1,916.13 m²）、浮筒占比（53.72% / 53.23% / 74.38%）、16 体逐体 Bq（三向加总与表 5 精确一致） |
| `03-multibody-16body/w7-wecsim-assembly/zeta-rad-visc-16body.py` | 共振阻尼比量级计算脚本：实跑 AH1 的 DAMPING/ADDEDMASS 全耦合块刚体合成至整体重心，在垂荡/纵摇固有频率处插值算 ζ_rad，并与表 5 等效线性 ζ_visc 对比（可重复运行；内部路径为执行时本地路径） |
| `03-multibody-16body/w7-wecsim-assembly/zeta-rad-visc-16body.json` | 同上结果数据（ζ_rad、临界阻尼、逐幅值 ζ_visc 与置零峰值高估倍数） |
| `03-multibody-16body/w7-wecsim-assembly/w7-damping-ab-test-note.md` | W7 决策支持 #2（2026-11-17，**非已定口径**）：粘性阻尼加/不加的整体刚体频域 A/B 对比——细化网格共振峰比 ×43（垂荡）/×36（纵摇）/×42（横摇）；JONSWAP（Hs=3）RMS 比：Tp ≤ 8 s 时 ≤×1.1、Tp ≥ 10 s 纵摇 ×4.5–7.0、Tp=20 s 垂荡 ×4.0；结论「置零影响不大」仅短周期海况成立；含粗网格分辨率伪影警告（粗网格峰值比 ×1.1–1.2 不得引用）与垂荡激励相消凹陷的单体 LIS 回查证据 |
| `03-multibody-16body/w7-wecsim-assembly/rao-damping-ab-refined.py` | A/B 对比细化网格脚本：A/B/F 样条插值至 Δω=0.0005 求峰、复合网格谱积分、等效线性化自洽迭代（可重复运行；内部路径为执行时本地路径） |
| `03-multibody-16body/w7-wecsim-assembly/rao-damping-ab-refined-results.json` | 同上结果数据（细化峰值与逐 Tp 的 RMS 对比） |
| `03-multibody-16body/w7-wecsim-assembly/rao-damping-ab-test.py` | A/B 对比粗网格版脚本（AQWA 原网格）：其峰值/RMS 因共振带宽不可分辨而系统性低估，**仅留存备查、数字不得引用**（见试验说明 §1/§5） |
| `03-multibody-16body/w7-wecsim-assembly/rao-damping-ab-results.json` | 粗网格版结果数据（留存备查，不得引用） |
| `03-multibody-16body/w7-wecsim-assembly/rao-damping-ab.csv` | 粗网格版 RAO 表（0°/90° 浪向，垂荡/纵摇/横摇，两工况；留存备查） |
| `03-multibody-16body/w7-wecsim-assembly/w7-viscous-damping-brief-report.md` | 粘性阻尼简要报告（2026-11-18，按 Saber 要求汇编，简明排版）：粘性阻尼的重要性（表 5 出处与共振阻尼比量级）、加/不加粘性阻尼的初步验算对比（细化网格 A/B 试验：共振峰比值与逐 Tp 的 RMS 比值）、四种备选处理方式（置零/整体施加/投影面积拆分/Morison 标定）；数据均引自本节决策附件与 A/B 试验说明（阻尼口径已于 2026-11-21 定案，见阻尼方案） |
| `03-multibody-16body/w7-wecsim-assembly/w7-damping-scheme-16body.md` | **W7 阻尼方案（16 体，2026-11-21 定案，W7 装配执行口径）**：主版 S1 = Cd 加权面积分配（水平 Cd 先验 DNV-RP-C205 立柱 1.2 / 浮筒段 2.0；垂向面积分配 × 径向标定权重，β*=16.77，使装配纵摇涌现二次阻尼对齐表 5——未标定时涌现为表 5 的 2.88 倍）+ 置零版 Z 作 GATE-C 对照（同装配并行衰减/RAO，预期被证伪留档）；装配对账预测（平动总量精确、横摇涌现 +3.1%、艏摇 −14.6%、交叉项 +48%～+53% 为模型形式局限并附下限论证）；敏感性版 S2/S3 与阶段 4 不确定性带安排；两版对比的步骤与基准（衰减对论文、RAO 对 AQWA、截面力只互比） |
| `03-multibody-16body/w7-wecsim-assembly/cd-weighted-damping-16body.py` | 阻尼方案计算脚本：Cd 加权分配（含 S2/S3 变体）+ 装配涌现对账（转动/交叉项公式见脚本头注）+ β 二分求解；自检 = 比例 1、β=0 时复现 `area-shares-16body.json` 逐体值（最大相对偏差 5.5×10⁻¹⁶）（可重复运行） |
| `03-multibody-16body/w7-wecsim-assembly/cd-weighted-damping-16body.json` | 同上结果数据：S1/S2/S3 三版逐体 Bq 全表、三向总量（与表 5 精确一致）与涌现对账值、β* |
| `03-multibody-16body/w7-wecsim-assembly/custom-coefficient-damping-16body.py` | 自定义系数面积分配脚本（2026-11-22 草案，2026-11-25 随三版并行修订入仓）：按导师意见改自定义系数法（权重 = 投影面积 × 自定义系数 k，不用 Cd、不引 DNV 先验）；K1 主版数据（系数比 1.0 + 垂向径向标定 β=15.9886）；自检含复现旧 S1（r_k=5/3）与旧 S0（r_k=1、β=0）两项（可重复运行） |
| `03-multibody-16body/w7-wecsim-assembly/custom-coefficient-damping-16body.json` | 同上结果数据：K1 及 K_sens1667/K_sens250/K_nocal 四组逐体 Bq 全表、三向总量（与表 5 精确一致）与涌现对账值、β*；K1 数组已进装配数据文件 `w7-assembly-data-16body.m`（`quadDragK1`） |
| `03-multibody-16body/w7-wecsim-assembly/w7-assembly-checklist-16body.md` | **W7 装配清单（16 体，2026-11-22，执行用核对表）**：输入清单（.h5 校验值、AH1 实跑值出处）、16 体逐体质量/重心/惯量赋值表（AH1 值，总质量自检 17,854.16 t）、15 个刚性约束体对与界面径向位置、S1 逐体阻尼赋值表与 Z/S2/S3/S0 安排、装配后单位运动试验复测表（涌现预测值）、GATE-C 执行顺序（衰减对论文、RAO 对 AQWA、约束反力检查）与阶段 4 交接；阻尼挂法为未定项，建模时按软件功能定；数字逐项回源，衰减周期判据处注明 0.315/0.466 与 0.316/0.474 两种口径的来源；2026-11-22 晚 §1 补记惯量积 Ixy 更正说明 |
| `03-multibody-16body/w7-wecsim-assembly/w7-assembly-data-16body.m` | **W7 装配数据脚本（16 体，2026-11-22，机器可读数据）**：16 体质量（kg）/质心/主惯量对角（AH1 实跑值）、逐体二次阻尼矩阵 quadDragS1/S2/S3/S0 与 quadDragZ（6 列，转动列恒 0）、15 个约束体对与全局位置（W1 段界半径 × 链方向，z=−16.5）；文件头注明阻尼挂法为 WEC-Sim 原生 `body(i).quadDrag.drag`（2026-11-22 查官方文档确认：逐体二次拖曳、按体自身速度计、静水口径；待装配单位运动试验实证后正式补记方案 §六）；由生成脚本从已核 JSON 自动生成，勿手改数值；**2026-11-22 晚更正**：补 `bodyInertiaProducts` 惯量积数组（60° 链 4 段 +2.289×10⁶、300° 链 4 段 −2.289×10⁶ kg·m²，AH1 实跑值），文件头阻尼挂法改注为 diag() 展开 6×6（WEC-Sim v7.1.0 bodyClass 断言 drag 须为 6×6）；修正版 7,225 B、SHA-256 0a75d5f4…；**当晚 21:15 巡检所推为更正前版本（commit 8ddb83c），作废，以修正版为准** |
| `03-multibody-16body/w7-wecsim-assembly/gen-w7-assembly-data.py` | 上一行的生成脚本：读 GATE-A 三笔账与 Cd 加权分配结果 JSON 生成 .m 数据文件，内嵌自检（总质量 17,854.16 t、四版阻尼三向总量与表 5 一致、段质心半径与 W1 段界中点吻合 <0.01 m）（可重复运行；2026-11-22 晚已按惯量积更正修订） |
| `03-multibody-16body/w7-wecsim-assembly/wecSimInputFile_16body.m` | **16 体 WEC-Sim 输入文件（2026-11-22 初版；2026-11-25 修订）**：按 MOST 模板口径改写——删 wind/windTurbine/mooring 三段（纯浮体状态 B）；16 个 body 引 `futi_16body.h5` 与装配数据脚本；`simu.b2b=1`、gravity=9.81、rho=1025、`explorer='off'`、逐体二次阻尼 `diag(quadDragS1(i,:))`；**2026-11-25 补齐根体 `Floating (6DOF)` 接地对象 `Constraint16`（`location=[0 0 0]`）及 15 道界面局部 `orientation.z/y`**，同日 Saber 实机跑通输入变量核对 |
| `03-multibody-16body/w7-wecsim-assembly/build_SModel_16body.m` | **16 体 Simulink 自动建模脚本（2026-11-25 新增）**：依据 Saber 上传的官方模板 `SModel_16body.slx` 解析出本机库路径与端口结构后编写；支持备份原模板并清空旧风机/系泊块（保留官方 Simscape Multibody 配置），一键自动生成 `Global Reference Frame` + `Constraint16`（`Floating 6DOF`）+ 16 个 `Rigid Body` + 15 个 `Fixed` 约束的完整无闭环树形拓扑 |
| `03-multibody-16body/w7-wecsim-assembly/build_SModel_16body_full.m` | **16 体 + MOST 全系统自动建模脚本（2026-11-26 新增，V2.7 主线）**：在 `build_SModel_16body.m` 基础上保留纯浮体备份 `SModel_16body_pure_backup.slx`，自动接入 `MOST_Lib/Wind turbine`（`IEA15MW`）与 `WECSim_Lib_Moorings/MooringNLStatic` 并连线至 `Body1`（共 35 个模块） |
| `03-multibody-16body/w7-wecsim-assembly/wecSimInputFile_16body_full.m` | **16 体 + MOST 全系统输入文件（2026-11-26 新增，V2.7 主线）**：16 体 `.h5` + `quadDragK1`（1.0 版）+ `MOST` `wind`/`windTurbine`（8 m/s `WIND_8mps.mat`）+ `MooringNLStatic`（3 根 850 m 悬链线）；保留 `b2b=1`、`gravity=9.81`、`rho=1025`、`inertiaProducts`；已在 R2025a/v7.1.0 跑通 30 s `noWave` 静水+风首跑（工作机运行时改名为 `wecSimInputFile.m`） |
| `03-multibody-16body/w7-wecsim-assembly/output/simulation_16body_full_30s.log` | **全系统 30 s 首跑控制台日志（2026-11-26 归档，6,077 B）**：16 体质量/CG/惯量积 + 16 约束全数正确读入，`noWave` + `8 m/s` 风 61.87 s 零报错跑完；实测 `body(1)` CG 垂向坐标均值 `−4.1920 m`（相对初值 `−3.7310 m` 净下沉 `Δz = −0.4610 m`）、系泊垂向力 `−6.021 MN`、塔基垂向力 `−23.83 MN` |
| `03-multibody-16body/w7-wecsim-assembly/wecSimInputFile_16body_case.m` | **全系统参数化工况输入驱动（2026-11-26 新增，V2.7 W7/GATE 1B）**：读取 `w7_case_cfg.mat` 动态切换 `noWaveCIC`（自由衰减）/ `regular` / `noWave`、风况（`still` 0 m/s LUT 停机 / `constant` / `turbulent`）、阻尼三版（`K1`/`S1`/`Z`）与 `deduct100t` 开关；保留全部 V2.7 红线设置 |
| `03-multibody-16body/w7-wecsim-assembly/run_w7_gate1b_suite.m` | **W7 / GATE 1B 总验收批处理脚本（2026-11-26 新增，V2.7 主线）**：在工作机上顺序执行单位运动 `quadDrag` 代数自检、静风 4 自由度（垂荡/纵摇/纵荡/艏摇）× 两版阻尼（`K1`/`Z`，已取消 `5/3` 版 `S1`）全系统自由衰减（借 `SModel_16body_decay.slx` 中 `Constraint16` `Bushing Joint` PositionTarget 整体施加初位移并实机复核 `forceMorisonAndViscous`）、以及 `0°` 对称风浪规则波校核（RAO + 60°/300° 对称性 + 15 截面反力），输出 `output/gate1b_verification_summary.txt` 与 `output/gate1b_summary.json` |

## references（参考文献与规范原件）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `references/SOURCES.md` | 本目录索引（出处对照表） |
| `references/nrel-tp-5000-76773-volturnus-s-platform.pdf` | NREL/TP-5000-76773（2020-07）原件 PDF，2,327,676 B：UMaine VolturnUS-S 平台定义 |
| `references/nrel-tp-5000-75698-iea-15mw-turbine.pdf` | NREL/TP-5000-75698（2020-03）原件 PDF，6,290,390 B：IEA 15 MW 参考风机定义 |
| `references/nrel-tp-5000-76773-volturnus-s-platform-zh.md` | NREL/TP-5000-76773 中文版（2026-11-16 翻译）：自然中文（非直译），数字/单位/公式原样保留，表格译表头表题、数据照搬，图只译图题、图面未重绘，参考文献条目保留英文 |
| `references/nrel-tp-5000-76773-volturnus-s-platform-zh.docx` / `.pdf` | 同上中文版的 Word / PDF 版（PDF 19 页） |
| `references/nrel-tp-5000-75698-iea-15mw-turbine-zh.md` | NREL/TP-5000-75698 中文版（2026-11-16 翻译）：口径同 76773 中文版（含附录 A 叶片截面、附录 B 塔架与地基建模） |
| `references/nrel-tp-5000-75698-iea-15mw-turbine-zh.docx` / `.pdf` | 同上中文版的 Word / PDF 版（PDF 34 页） |
| `references/ouc-undergraduate-thesis-spec.doc` | 《中国海洋大学本科毕业论文（设计）撰写规范》，273,689 B |

## bibliography（参考文献阅读清单，2026-11-16 新建）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `bibliography/reading-list.md` | 参考文献阅读清单（2026-11-16 编制，同日补充后共 21 篇；2026-11-21 增补 Souza et al. 2024 为 [20] 后共 22 篇，原 [20] Xu、[21] Gu 顺延为 [21]、[22]，Gu 原文 PDF 文件名仍为 `21-` 前缀、待 Saber 确认后改名）：按"年份由老到新（1950–2025）+ 内容由广入深"的单一阅读顺序编排，分六个阅读阶段，每篇附定位说明与对应课题环节；出版信息逐条经公开检索核对，DOI 仅标注已核实者。其中 [14] Gaertner et al. 2020（NREL/TP-5000-75698）与 [15] Allen et al. 2020（NREL/TP-5000-76773）原件已在 `references/`，本目录只存清单、不重复存原件 |
| `bibliography/09-jonkman-2009-5mw-reference-turbine.pdf` | 清单 [9] 原文（852,209 B，75 页）：NREL/TP-500-38060 公开报告，经 NREL 官方 FAST 仓库镜像取得，2026-11-16 网页上传入仓（提交 949c32c） |
| `bibliography/11-yu-2014-wec-sim-tool.pdf` | 清单 [11] 原文（903,883 B，8 页）：WEC-Sim METS 2014 论文，OSTI 公开件 SAND2014-3013C，同上入仓 |
| `bibliography/13-perez-collazo-2015-combined-wave-wind-review.pdf` | 清单 [13] 原文（1,807,816 B，39 页含仓储封面）：风浪联合开发综述，普利茅斯大学 PEARL 仓储作者接受稿，2026-11-16 经浏览器通道下载、网页上传补入（提交 003af7a） |
| `bibliography/16-sirigu-2022-most.pdf` | 清单 [16] 原文（1,171,765 B，10 页）：MOST，IOP 开放获取，同上入仓 |
| `bibliography/17-petracca-2022-hybrid-wind-wave-design.pdf` | 清单 [17] 原文（4,219,855 B，28 页）：混合风浪系统设计与技术经济分析，MDPI 开放获取，同上入仓 |
| `bibliography/21-gu-2025-15mw-fowt-wec-combined.pdf` | 清单 [21] 原文（6,843,520 B，15 页）：15 MW 浮式风机+WEC 组合概念，CC 许可开放获取（Tethys 托管出版社版），同上入仓 |

## 结构整理（2026-11-13，旧路径 → 新路径）

首次同步时的目录按「到达批次」组织（`docs/`、`stage1-verification/`、`stage2-segmentation/`、`stage3-plan/`、`stage3-multibody-check/` 混杂），现统一为「阶段编号 + 阶段内按计划/验证/原始输出分开」。文件内容除导航文档（README / PROGRESS / 本文件）与计划书文件头的路径指针外未作改动。

| 旧路径 | 新路径 |
|---|---|
| `docs/technical-route-v2.5.md` | `00-route/technical-route-v2.5.md` |
| `stage1-verification/floating-platform-verification-report-brief.md` | `01-single-body-validation/gate1a-verification-report-brief.md` |
| `stage2-segmentation/stage2-pontoon-splitting-plan-v2.md` | `02-two-body-segmentation/pontoon-splitting-plan-v2.md` |
| `stage2-segmentation/stage2-cross-ai-review-package.md` | `02-two-body-segmentation/cross-ai-review-package.md` |
| `stage2-segmentation/stage2-interface-nodes.csv` | `02-two-body-segmentation/interface-nodes.csv` |
| `stage3-plan/stage3-22body-segmentation-plan-v1.2.md` | `03-multibody-19body/plan-22body-superseded/segmentation-plan-v1.2.md` |
| `stage3-multibody-check/19BODY-synthesis-verification.md` | `03-multibody-19body/gate-a-verification/19body-synthesis-verification.md`（文件名同时改为小写） |
| `stage3-multibody-check/verify_19body.py` | `03-multibody-19body/gate-a-verification/verify_19body.py` |
| `stage3-multibody-check/synthesis_log.txt` | `03-multibody-19body/gate-a-verification/synthesis_log.txt` |
| `stage3-multibody-check/synthesis_results.json` | `03-multibody-19body/gate-a-verification/synthesis_results.json` |
| `stage3-multibody-check/FUTI_19BODY.MES` | `03-multibody-19body/gate-a-verification/output/FUTI_19BODY.MES` |

## 大文件：以 Release 附件存放（仓库文件树之外、本项目之内）

| 文件 | 大小 | 存放与校验 |
|---|---|---|
| `FUTI_19BODY.LIS` | 89,926,233 B | 超过 GitHub 网页上传的单文件 25 MB 上限，存于 Release `stage3-19body-aqwa-output` 的附件：https://github.com/Saber0606/bishe/releases/tag/stage3-19body-aqwa-output ；SHA-256 `3a7c566f8646eb204b323a38531e516339897756ebe8e6e2eed21c8f5b99d16b`，与本地原件一致（2026-11-13 核验） |
| `futi_19body.zip`（内含下两行文件） | 261,904,581 B | W6 BEMIO 产出的打包件（Saber 2026-11-15 上传并决定以压缩包形式存放，不拆单独附件；Release 说明中已注明内含文件），存于 Release `W6-output` 的附件：https://github.com/Saber0606/bishe/releases/tag/W6-output ；SHA-256 `f7c4d7800c807a66d6c027cbd737ff4f65b43faadc07c75523f6aae9440f39b9`，与 GitHub 记录的附件摘要一致（2026-11-15 核验） |
| └ `futi_19body.h5` | 155,612,740 B | 上行 ZIP 内文件：BEMIO 生成的 19 体水动力数据库（WEC-Sim 输入）；SHA-256 `5d2cf6520e53f5af9db701a2bbe785987228d2914cc74db2df186d1077c7c612`（解压后核验，大小与运行日志记录一致）；GATE-B 复核已通过（见 `03-multibody-19body/gate-b-verification/`） |
| └ `futi_19body_hydro.mat` | 131,962,908 B | 上行 ZIP 内文件：同一次运行的完整 MATLAB hydro 结构体；SHA-256 `39cedbfa87d1c0a0c998764e9609d60505a73b061e77c971e013ca24632280f1`（解压后核验） |
| `futi_16body.LIS` | 70,936,631 B | 16 体更正链实跑 LIS（2026-11-16）：超过 25 MB 上限，存于 Release `stage3-16body-aqwa-output`（**待上传**，上传后补链接）；SHA-256 `2b78ec2555c9e45929d224dda822cc1fbf63ae55e77ac31de5ce8b373b47b9e0`、MD5 `fb9bdf57ec16846400f742eed7df9645`（本地原件，2026-11-16 核验）；按 Saber 指示统一命名（回传原名 `FUTI_16BODY.LIS`，zip 传输） |
| `futi_16body.zip`（内含下两行文件） | 194,391,226 B | 更正 W6 BEMIO 产出的打包件（Saber 2026-11-16 上传），存于 Release `16-output` 的附件：https://github.com/Saber0606/bishe/releases/tag/16-output ；SHA-256 `6eeab5943af3822c7293e29d92d04ce064e1074ebfdfacf33a89c21d38b88497`，与 GitHub 记录的附件摘要一致（2026-11-16 助理下载实测核验）；该 Release 页面说明为空，校验依据以本节登记为准 |
| └ `futi_16body.h5` | 115,902,180 B | 上行 ZIP 内文件：BEMIO 生成的 16 体水动力数据库（WEC-Sim 输入）；SHA-256 `ceb2231f98df83b1d5a72280f3b8eb09154189be04864036af436d27bc859b7c`（解压后核验，大小与运行日志记录一致）；GATE-B 复核已通过（见 `03-multibody-16body/gate-b-verification/`） |
| └ `futi_16body_hydro.mat` | 98,007,095 B | 上行 ZIP 内文件：同一次运行的完整 MATLAB hydro 结构体；SHA-256 `fe2e7ecbbac7bed6694afe164fa57ad9b180bdbad124d96600afed08720c2ce4`（解压后核验） |

## 未单独入仓的副本

| 文件 | 说明 |
|---|---|
| 原始打包的另两份副本（与已入仓打包件共 3 份） | 三份 MD5 完全相同（`c5cb8e5a144d19cec202296e1077ed4f`），为字节级重复副本，不重复入仓；其内容已由入仓的 `futi-19body-run-bundle.zip` 及 `.LIS` / `.AH1` 单件完整代表 |
