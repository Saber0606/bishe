# 毕业设计：基于阻抗控制的风浪融合机组互馈增益研究

> 公开仓库，用于毕业设计进度与成果的同步存档（2026-11-22 起由私有改为公开）。
>
> **接入本仓库的 AI / 协作者请先读 [`AGENTS.md`](AGENTS.md)**：项目说明、当前进度快照、文件分类说明、下一步工作与口径红线都在该文件里，读完再看其他文件。

- **正式题目**：《基于阻抗控制的风浪融合机组互馈增益研究》
- **工作 / 建模标题**：基于 AQWA-WEC-Sim 的 IEA 15 MW VolturnUS-S 浮式风机横撑多体水动力与截面载荷分析

## 技术主线

AQWA 整体纯浮体 → 多体切分 → BEMIO → WEC-Sim 约束建模 → 横撑截面内力 → 外柱 WEC 阻抗控制与风浪互馈增益（阶段 5，核心章）

详细执行路线见 [`00-route/technical-route-v2.5.md`](00-route/technical-route-v2.5.md)（现已升级为技术路线 V2.6，2026-11-25）。

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
├── 03-multibody-19body/                 # 阶段 3：19 体多体链路（历史口径，2026-11-16 起由 16 体接棒）
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
├── 03-multibody-16body/                 # 阶段 3 更正：16 体链路（2026-11-16，每筒 4 段；现行执行口径，W1–W6 完成、双 GATE 关门）
│   ├── design-basis-w1-w2/              # 更正 W1 分段方案 + W2 设计分账 + 推导脚本/结果（以整体单体 dat 独立推导）
│   ├── w3-dat-assembly/                 # 更正 W3 组装核查记录（§6 附记：实跑定版与关门）+ 脚本 + output/（实跑定版 dat）
│   ├── w4-aqwa-run/                     # 更正 W4 求解与产物核查记录 + LIS 核查脚本 + output/（.MES；.AH1 待网页上传、.LIS 在 Release）
│   ├── gate-a-verification/             # 更正 W5/GATE-A 关门证据：三笔账 + corr+ 全谱合成（0.104%）+ LIS 印刷版交叉核查
│   ├── w6-bemio/                        # 更正 W6 BEMIO 脚本（已运行）+ output/（产出说明 + 日志；大产出在 Release 16-output）
│   └── gate-b-verification/             # 更正 W6/GATE-B 复核记录 + 脚本 + 结果（2026-11-16 通过）
└── references/                          # 参考文献与规范原件：NREL 两份报告 PDF + 学校撰写规范 .doc + SOURCES.md 索引
```

2026-11-13 之前的旧路径与新路径的对照表见 `FILES.md` 的「结构整理」一节。

## 当前进度（截至 2026-11-27）

- 阶段 0：已完成
- 阶段 1A：已通过（GATE 1A）
- 阶段 2：一级验收已通过（2026-11-09，合成偏差 ≤0.6%，多数 ≤0.002%）；多体 `.AH1` 已用 AHD1 补跑并通过 BEMIO 数据块核对
- 阶段 3：**16 体主线已全部关门（2026-11-27）**
  - 19 体口径（W1–W6、GATE-A/GATE-B）保留为历史执行证据（见 `03-multibody-19body/`）；
  - **16 体现行主线（W1–W7）全部完成**：W1–W6（AQWA + BEMIO，GATE-A 0.104% / GATE-B ≤0.386%）已关门；**W7 / GATE 1B**（16 体 + `MOST` IEA 15 MW + `MooringNLStatic`）已于 2026-11-27 完成 `quadDragK1` 全套自由衰减（表 11 频率偏差：垂荡 `+0.10%`、纵摇 `-0.54%`、纵荡 `+3.82%`、艏摇 `+1.50%`；`liveDragErr ≤ 1.99e-16`）与规则波基准验收，正式关门并锁定 `quadDragK1`（见 `03-multibody-16body/w7-wecsim-assembly/w7-gate1b-verification-record-16body.md`）。
- **下一步（阶段 4 + 阶段 5）**：拍板三轴 `Gimbal` 柔性铰结构阻尼并实施阶段 4 前置改造（3 线系泊分拆精准挂回外柱 `Body 6/11/16` + 15 界面换装三轴柔性铰 `dt ≤ 0.001 s` + `k×1000` 回归），在状态 A `Baseline 0` 提取 15 截面内力与应力校核，随后进入阶段 5 外柱干舱内置惯性式 WEC 阻抗控制与三维互馈增益研究（见 `00-route/technical-route-v2.5.md` V2.7）。

全程进度与待办见 [`PROGRESS.md`](PROGRESS.md)。

## 参考基准

1. Allen et al., *Definition of the UMaine VolturnUS-S Reference Platform for IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-76773, July 2020.
2. Gaertner et al., *Definition of the IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-75698, March 2020.

注：以上为公开的 NREL 技术报告；其 PDF 原件已存入本仓库 `references/` 目录（仓内查阅用），《中国海洋大学本科毕业论文（设计）撰写规范》原件同在该目录。

## 文件说明

本仓库的完整文件清单（含以 Release 附件存放的大文件说明），见 [`FILES.md`](FILES.md)。
