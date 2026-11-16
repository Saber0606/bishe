# 毕业设计：基于阻抗控制的风浪融合机组互馈增益研究

> 私有仓库，仅用于毕业设计进度与成果的同步存档。
>
> **接入本仓库的 AI / 协作者请先读 [`AGENTS.md`](AGENTS.md)**：项目说明、当前进度快照、文件分类说明、下一步工作与口径红线都在该文件里，读完再看其他文件。

- **正式题目**：《基于阻抗控制的风浪融合机组互馈增益研究》
- **工作 / 建模标题**：基于 AQWA-WEC-Sim 的 IEA 15 MW VolturnUS-S 浮式风机横撑多体水动力与截面载荷分析

## 技术主线

AQWA 整体纯浮体 → 多体切分 → BEMIO → WEC-Sim 约束建模 → 横撑截面内力 → 外柱 WEC 阻抗控制与风浪互馈增益（阶段 5，核心章）

详细执行路线见 [`00-route/technical-route-v2.5.md`](00-route/technical-route-v2.5.md)（技术路线 V2.5，2026-11-09）。

## 仓库结构

按工作阶段编号归档，阶段内再按「计划 / 验证 / 原始输出」分开。根目录只放总览文件。

```
.
├── AGENTS.md                            # 接手说明（先读）：项目、进度、分类、下一步、口径红线
├── README.md / PROGRESS.md / FILES.md   # 总览、进度、文件清单（未上仓文件也在 FILES.md 登记）
├── 00-route/                            # 全程执行路线
│   └── technical-route-v2.5.md
├── 01-single-body-validation/           # 阶段 1：整体纯浮体验证（GATE 1A）
│   ├── gate1a-verification-report-brief.md / .docx
│   └── output/                          # 整体单体实跑输出：FUTI_LOWFREQ.LIS / futi_lowfreq.dat（符号裁决基准）
├── 02-two-body-segmentation/            # 阶段 2：180° 浮筒二体切分
│   ├── pontoon-splitting-plan-v2.md     # 切分方案 V2（含操作手册）
│   ├── cross-ai-review-package.md       # 跨 AI 复核包
│   └── interface-nodes.csv              # 界面节点清单
├── 03-multibody-19body/                 # 阶段 3：19 体多体链路（执行口径）
│   ├── plan-22body-superseded/          # 22 体计划书（未执行，历史存档；文件头有变更说明）
│   │   └── segmentation-plan-v1.2.md
│   ├── design-basis-w1-w2/              # W1 分段方案 + W2 质量分账（原件遗失，2026-11-13 复原）
│   ├── w6-bemio/                        # W6 BEMIO 生成脚本（REV 1，已跑通）+ 运行日志（大产出在 Release W6-output）
│   ├── gate-b-verification/             # GATE-B 复核记录 + 脚本 + 结果（2026-11-15 通过）
│   └── gate-a-verification/             # 19 体合成验证（GATE-A 口径）+ 符号裁决记录
│       ├── 19body-synthesis-verification.md
│       ├── verify_19body.py             # 验证脚本（与被验 .AH1 同目录运行时使用）
│       ├── synthesis_log.txt / synthesis_results.json
│       ├── excitation-full-spectrum-note.md / .py / .csv / .json / .npz   # 激励力全谱合成（W5 最后一项）
│       └── output/                      # AQWA 原始输出：.MES / .AH1 / 原始打包 zip（.LIS 在 Release，见 FILES.md）
├── 03-multibody-16body/                 # 阶段 3 更正：16 体链路（2026-11-16，每筒 4 段；W1/W2 设计 v2、W3 已关闭、W4 已求解）
│   ├── design-basis-w1-w2/              # 更正 W1 分段方案 + W2 设计分账 + 推导脚本/结果（以整体单体 dat 独立推导）
│   ├── w3-dat-assembly/                 # 更正 W3 组装核查记录（§6 附记：实跑定版与关门）+ 脚本 + output/（实跑定版 dat）
│   └── w4-aqwa-run/                     # 更正 W4 求解与产物核查记录 + LIS 核查脚本 + output/（.MES；.AH1 待网页上传、.LIS 在 Release）
└── references/                          # 参考文献与规范原件：NREL 两份报告 PDF + 学校撰写规范 .doc + SOURCES.md 索引
```

2026-11-13 之前的旧路径与新路径的对照表见 `FILES.md` 的「结构整理」一节。

## 当前进度（截至 2026-11-15）

- 阶段 0：已完成
- 阶段 1A：已通过（GATE 1A）
- 阶段 2：一级验收已通过（2026-11-09，合成偏差 ≤0.6%，多数 ≤0.002%）；多体 `.AH1` 已用 AHD1 补跑并通过 BEMIO 数据块核对
- 阶段 3：进行中
  - 19 体 AQWA 仿真已完成（2026-11-11 运行，AQWA-Line 2022 R1）
  - 19 体合成验证已通过一级验收口径（2026-11-13）：总质量 17,854.1 t、排水量 20,157.9 m³、DIFF 面元合计 5,454 与整体模型一致、K33 +0.01%、垂荡固有频率 0.3143 rad/s（-0.2%）、纵摇/横摇 0.4622 rad/s（-0.8%），各项偏差均 <2%。详见 [`03-multibody-19body/gate-a-verification/19body-synthesis-verification.md`](03-multibody-19body/gate-a-verification/19body-synthesis-verification.md)
  - `.MES` 报错清点完成：1,265 条消息全部为 WARNING，ERROR / FATAL 为 0；去重后 6 类，均为切分模型的预期警告
  - 激励力相位修正符号已裁决（2026-11-13）：以整体单体实跑 LIS 为外部基准全谱比对，corr+（计划书公式）中位误差 0.102%、corr− 96.6%，**corr+ 正确，GATE-A 已正式关门**，详见 `03-multibody-19body/gate-a-verification/sign-adjudication-record.md`
  - W1 分段方案与 W2 质量分账已复原入仓（`design-basis-w1-w2/`，原件遗失后据实跑数据复原）
  - W6 已完成（2026-11-15）：BEMIO 生成 `futi_19body.h5`（存于 Release `W6-output` 的 ZIP 内），**GATE-B 复核通过**——合成激励力对 corr+ 锚幅值最大偏差 0.357%、相位最大 0.168°（判据 <1% / <1°），Ainf 处理与 body 顺序确认，详见 `03-multibody-19body/gate-b-verification/gate-b-verification-record.md`
  - 下一步（W7）：表 5 粘性阻尼拆分口径由 Saber 拍板后，做 WEC-Sim 刚接装配与 GATE-C

全程进度与待办见 [`PROGRESS.md`](PROGRESS.md)。

## 参考基准

1. Allen et al., *Definition of the UMaine VolturnUS-S Reference Platform for IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-76773, July 2020.
2. Gaertner et al., *Definition of the IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-75698, March 2020.

注：以上为公开的 NREL 技术报告；其 PDF 原件已存入本仓库 `references/` 目录（私有仓内查阅用），《中国海洋大学本科毕业论文（设计）撰写规范》原件同在该目录。

## 文件说明

本仓库的完整文件清单（含以 Release 附件存放的大文件说明），见 [`FILES.md`](FILES.md)。
