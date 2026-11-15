# 文件清单

仓库按阶段编号组织（结构图见 `README.md` 的「仓库结构」一节）。本表按当前路径登记仓库文件树内的全部 38 个文件，另有 2 组大文件以 Release 附件存放（见文末）。

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
| `00-route/technical-route-v2.5.md` | 技术路线 V2.5 原文（2026-11-09，用户上传的 `upload.md`） |

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
| `03-multibody-19body/gate-a-verification/output/FUTI_19BODY.MES` | AQWA 原始消息文件（1,265 条全部为 WARNING，0 ERROR / FATAL） |
| `03-multibody-19body/gate-a-verification/output/futi_19body.AH1` | AQWA 水动力数据库原件（21,146,564 B，2026-11-13 经网页上传补入；BEMIO 的输入） |
| `03-multibody-19body/gate-a-verification/output/futi-19body-run-bundle.zip` | 本次运行的原始打包件（21,638,174 B，内含 `FUTI_19BODY.LIS` + `futi_19body.AH1`，2026-11-13 经网页上传补入） |
| `03-multibody-19body/gate-b-verification/gate-b-verification-record.md` | GATE-B 复核记录（2026-11-15）：W6 产出 `.h5` / hydro.mat 经 SHA-256 校验链下载复核——合成激励力对 corr+ 锚幅值最大偏差 0.357%、相位最大 0.168°（判据 <1% / <1°），A/B 矩阵与 AH1 逐元素一致，Ainf 由 radiationIRF 重算确认、与 NREL 表 4 偏差 ≤2.24%，body 顺序/重心逐位一致；**GATE-B 通过**。含 BEMIO 激励力相位约定（共轭 + 参考点换算）的识别与逆变换说明、GATE-A 低频残差带复查结论（不复现，源于分体口径而非 BEMIO） |
| `03-multibody-19body/gate-b-verification/gate-b-check.py` | GATE-B 复核脚本（计算部分与实跑脚本逐字相同，输入来源对应关系见脚本头注） |
| `03-multibody-19body/gate-b-verification/gate-b-results.json` | GATE-B 复核结果数据（激励力两级比对、A/B 矩阵、Ainf、结构项汇总指标） |
| `03-multibody-19body/w6-bemio/bemio_futi_19body.m` | W6 BEMIO 生成脚本（REV 1，2026-11-15）：readAQWA → radiationIRF → excitationIRF → writeBEMIOH5，产出 `futi_19body.h5`；体序以 W1 编号表为准（19 体、361 耦合块、47 频点 0.02–2.10 rad/s、25 浪向）；含 hydro.Nb 体数/频点检查、hydro.file 基名断言（writeBEMIOH5 写出 `[hydro.file '.h5']`，已据 WEC-Sim 源码核实）、读入后检查点保存与 Ainf 记录点。2026-11-15 首次运行：readAQWA 成功（252.8 s，R2025a Update 1），IRF/写出未跑；REV 1 于当日 14:27 重跑完成并产出 `futi_19body.h5`，GATE-B 复核已通过（2026-11-15，见 `../gate-b-verification/`）。文件名用下划线是 MATLAB 可运行名的例外（见脚本头注释） |
| `03-multibody-19body/w6-bemio/output/README.md` | W6 运行产出存放说明（2026-11-15 建）：登记各产出文件的存放位置与状态；大文件（.h5 / 完整 hydro.mat）以 ZIP 形式存于 Release（实际标签 `W6-output`），SHA-256 已登记在本文件末节；GATE-B 复核记录在 `../../gate-b-verification/` |
| `03-multibody-19body/w6-bemio/output/bemio_futi_19body_log.txt` | W6 BEMIO 运行日志（2026-11-15，Saber 网页上传，5,023 B）：含初版脚本失败运行（文件名断言）与 REV 1 成功运行两段记录；REV 1 段为运行证据——readAQWA 255.6 s、Nb = 19、DOF = 114、radiationIRF 96.9 s、excitationIRF 32.5 s、writeBEMIOH5 13.5 s、产出 `futi_19body.h5` 155,612,740 B；含 Ainf 在 readAQWA 后与 radiationIRF 后的两组打印值（GATE-B 核查材料） |

## references（参考文献与规范原件）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `references/SOURCES.md` | 本目录索引（出处对照表） |
| `references/nrel-tp-5000-76773-volturnus-s-platform.pdf` | NREL/TP-5000-76773（2020-07）原件 PDF，2,327,676 B：UMaine VolturnUS-S 平台定义 |
| `references/nrel-tp-5000-75698-iea-15mw-turbine.pdf` | NREL/TP-5000-75698（2020-03）原件 PDF，6,290,390 B：IEA 15 MW 参考风机定义 |
| `references/ouc-undergraduate-thesis-spec.doc` | 《中国海洋大学本科毕业论文（设计）撰写规范》，273,689 B |

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

## 未单独入仓的副本

| 文件 | 说明 |
|---|---|
| 原始打包的另两份副本（与已入仓打包件共 3 份） | 三份 MD5 完全相同（`c5cb8e5a144d19cec202296e1077ed4f`），为字节级重复副本，不重复入仓；其内容已由入仓的 `futi-19body-run-bundle.zip` 及 `.LIS` / `.AH1` 单件完整代表 |
