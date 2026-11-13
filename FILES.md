# 文件清单

## 本次已同步（2026-11-13）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `README.md` | 仓库总览（题目、技术主线、当前进度、参考基准） |
| `PROGRESS.md` | 进度记录（阶段进度、19 体验证结论、后续待办） |
| `.gitignore` | 大文件与二进制输出的忽略规则 |
| `docs/technical-route-v2.5.md` | 技术路线 V2.5 原文（2026-11-09，用户上传的 `upload.md`） |
| `stage3-multibody-check/19BODY-synthesis-verification.md` | 19 体合成验证记录（原文文件名为 `19BODY_合成验证记录.md`） |
| `stage3-multibody-check/verify_19body.py` | 19 体合成验证脚本 |
| `stage3-multibody-check/synthesis_log.txt` | 合成验证运行日志 |
| `stage3-multibody-check/synthesis_results.json` | 合成验证结果数据 |
| `stage3-multibody-check/FUTI_19BODY.MES` | AQWA 消息文件（1,265 条全部为 WARNING，0 ERROR / FATAL） |

## 第二批补充（2026-11-13，用户 upload.zip，已读入待同步区）

| 仓库路径 | 来源 / 说明 |
|---|---|
| `stage1-verification/floating-platform-verification-report-brief.md` | 《浮体模型验证报告（简明版）》（2026-11-08，GATE 1A 验证报告）的文本转存版：15 项可比指标全过，几何/静水最大偏差 0.51%、固有频率最大 1.8%。`.docx` 原件为二进制，不在连接器文本快照通道内（且 `.gitignore` 排除 `*.docx`），故以同内容 `.md` 上仓，原件本地存档于 `~/workspace/graduation-design/new_uploads_1113/`；如需原件上仓，需走网页上传另行处理 |
| `stage2-segmentation/stage2-pontoon-splitting-plan-v2.md` | 《阶段2_浮筒切分划分方案_V2》（2026-11-08）：180° 浮筒盒选规则、Body 2 = 1,507 面元、m₂ = 3,870 t、CoG₂ (−42.8, 0, −14.1)，含 dat 改法操作手册与 GATE 2 一级验收表 |
| `stage2-segmentation/stage2-cross-ai-review-package.md` | 《阶段2_分段方案_跨AI复核包》（2026-11-08）：供独立复核的背景、参数出处与 10 个复核问题 |
| `stage2-segmentation/stage2-interface-nodes.csv` | 阶段 2 界面节点清单：32 个界面节点坐标与 Body 2 侧新编号 20001–20032 映射 |
| `stage3-plan/stage3-22body-segmentation-plan-v1.2.md` | 《阶段3_22体分段与多体链路计划书》V1.2（2026-11-11）：W1–W7 工作包与 GATE-A/B/C 验收门。**注意与实跑不一致**：计划口径为 22 体（3 浮筒 × 6 段 + 中心柱 + 3 外柱、21 截面），而 2026-11-11 实跑并已验证的是 19 体（每筒 5 段 + 外柱）。该计划书按历史计划文档存档，体数口径以哪版为准待用户确认后再改 README/PROGRESS 表述 |

## 未在本次同步的文件

以下文件是二进制或体积超出本次同步通道的上限（文本快照总上限 16 MiB，单个大文件亦不适合），仅在本地存档，未上传到 GitHub：

| 文件 | 大小 | 原因 |
|---|---|---|
| `FUTI_19BODY.LIS` | 89,926,233 B（约 90 MB） | 体积过大 |
| `futi_19body.AH1` | 21,146,564 B（约 21 MB） | 二进制且体积过大 |
| `___0 / ___1 / ___2.zip`（3 个，内容 MD5 相同，为同一文件） | 各 21,638,174 B | 与上两项重复的压缩包，二进制 |
| NREL 参考报告 PDF 2 份（NREL/TP-5000-76773、NREL/TP-5000-75698） | 约 2.3 MB / 6.3 MB | 第三方公开发表文献，本仓库仅作引用（见 README 参考基准） |
| 《中国海洋大学本科毕业论文（设计）撰写规范》`.doc` | 273,689 B | 学校规范文件（格式模板类），非毕设成果内容 |

如需把 `.LIS` / `.AH1` 等大文件也纳入版本管理，建议改用 Git LFS 或其他大文件存档方式，另行商定。
