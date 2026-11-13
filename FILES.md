# 文件清单

仓库按阶段编号组织（结构图见 `README.md` 的「仓库结构」一节）。本表按当前路径登记全部 16 个文件。

## 根目录（总览）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `AGENTS.md` | 接手说明（2026-11-13 新增）：供接入本仓库的 AI / 协作者先读——项目内容、进度快照（带证据出处）、文件分类、下一步工作队列、口径红线与同步纪律 |
| `README.md` | 仓库总览（题目、技术主线、仓库结构、当前进度、参考基准） |
| `PROGRESS.md` | 进度记录（阶段进度、19 体验证结论、后续待办、易混口径备忘） |
| `FILES.md` | 本文件 |
| `.gitignore` | 大文件与二进制输出的忽略规则 |

## 00-route（全程执行路线）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `00-route/technical-route-v2.5.md` | 技术路线 V2.5 原文（2026-11-09，用户上传的 `upload.md`） |

## 01-single-body-validation（阶段 1：整体纯浮体验证）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `01-single-body-validation/gate1a-verification-report-brief.md` | 《浮体模型验证报告（简明版）》（2026-11-08，GATE 1A 验证报告）的文本转存版：15 项可比指标全过，几何/静水最大偏差 0.51%、固有频率最大 1.8%。`.docx` 原件为二进制，不在连接器文本快照通道内（且 `.gitignore` 排除 `*.docx`），故以同内容 `.md` 上仓，原件本地存档于 `~/workspace/graduation-design/new_uploads_1113/`；如需原件上仓，需走网页上传另行处理 |

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
| `03-multibody-19body/gate-a-verification/19body-synthesis-verification.md` | 19 体合成验证记录（原文文件名为 `19BODY_合成验证记录.md`，2026-11-13 验证通过一级合成验收口径） |
| `03-multibody-19body/gate-a-verification/verify_19body.py` | 19 体合成验证脚本（运行时需与被验 `futi_19body.AH1` 同目录） |
| `03-multibody-19body/gate-a-verification/synthesis_log.txt` | 合成验证运行日志 |
| `03-multibody-19body/gate-a-verification/synthesis_results.json` | 合成验证结果数据 |
| `03-multibody-19body/gate-a-verification/output/FUTI_19BODY.MES` | AQWA 原始消息文件（1,265 条全部为 WARNING，0 ERROR / FATAL） |

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

## 未同步到仓库的文件（仅本地存档）

以下文件是二进制或体积超出同步通道的上限（文本快照总上限 16 MiB，单个大文件亦不适合），未上传到 GitHub：

| 文件 | 大小 | 原因 |
|---|---|---|
| `FUTI_19BODY.LIS` | 89,926,233 B（约 90 MB） | 体积过大 |
| `futi_19body.AH1` | 21,146,564 B（约 21 MB） | 二进制且体积过大 |
| `___0 / ___1 / ___2.zip`（3 个，内容 MD5 相同，为同一文件） | 各 21,638,174 B | 与上两项重复的压缩包，二进制 |
| NREL 参考报告 PDF 2 份（NREL/TP-5000-76773、NREL/TP-5000-75698） | 约 2.3 MB / 6.3 MB | 第三方公开发表文献，本仓库仅作引用（见 README 参考基准） |
| 《中国海洋大学本科毕业论文（设计）撰写规范》`.doc` | 273,689 B | 学校规范文件（格式模板类），非毕设成果内容 |

如需把 `.LIS` / `.AH1` 等大文件也纳入版本管理，建议改用 Git LFS 或其他大文件存档方式，另行商定。
