# 毕业设计：基于阻抗控制的风浪融合机组互馈增益研究

> 私有仓库，仅用于毕业设计进度与成果的同步存档。

- **正式题目**：《基于阻抗控制的风浪融合机组互馈增益研究》
- **工作 / 建模标题**：基于 AQWA-WEC-Sim 的 IEA 15 MW VolturnUS-S 浮式风机横撑多体水动力与截面载荷分析

## 技术主线

AQWA 整体纯浮体 → 多体切分 → BEMIO → WEC-Sim 约束建模 → 横撑截面内力 → 外柱 WEC 阻抗控制与风浪互馈增益（阶段 5，核心章）

详细执行路线见 [`docs/technical-route-v2.5.md`](docs/technical-route-v2.5.md)（技术路线 V2.5，2026-11-09）。

## 当前进度（截至 2026-11-13）

- 阶段 0：已完成
- 阶段 1A：已通过（GATE 1A）
- 阶段 2：一级验收已通过（2026-11-09，合成偏差 ≤0.6%，多数 ≤0.002%）；多体 `.AH1` 已用 AHD1 补跑并通过 BEMIO 数据块核对
- 阶段 3：进行中
  - 19 体 AQWA 仿真已完成（2026-11-11 运行，AQWA-Line 2022 R1）
  - 19 体合成验证已通过一级验收口径（2026-11-13）：总质量 17,854.1 t、排水量 20,157.9 m³、DIFF 面元合计 5,454 与整体模型一致、K33 +0.01%、垂荡固有频率 0.3143 rad/s（-0.2%）、纵摇/横摇 0.4622 rad/s（-0.8%），各项偏差均 <2%。详见 [`stage3-multibody-check/19BODY-synthesis-verification.md`](stage3-multibody-check/19BODY-synthesis-verification.md)
  - `.MES` 报错清点完成：1,265 条消息全部为 WARNING，ERROR / FATAL 为 0；去重后 6 类，均为切分模型的预期警告
  - 下一步：BEMIO 读取 `.AH1` 生成 `.h5`，随后复核激励力相位合成（GATE 3 必查项）

全程进度与待办见 [`PROGRESS.md`](PROGRESS.md)。

## 参考基准

1. Allen et al., *Definition of the UMaine VolturnUS-S Reference Platform for IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-76773, July 2020.
2. Gaertner et al., *Definition of the IEA Wind 15-MW Offshore Reference Wind Turbine*, NREL/TP-5000-75698, March 2020.

注：以上为公开的 NREL 技术报告，本仓库仅作引用，不存其 PDF 原件。

## 文件说明与未同步文件

本仓库的文件清单、以及因体积 / 格式限制未在本次同步的大文件清单，见 [`FILES.md`](FILES.md)。
