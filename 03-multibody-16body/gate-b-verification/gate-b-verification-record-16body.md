# GATE-B 复核记录（16 体更正 W6：BEMIO 生成 .h5 的数据复核）

日期：2026-11-16。执行口径：16 体更正方案（每浮筒 4 段，16 体 / 96 DOF）。判据沿 19 体 GATE-B（计划书 §W6 / GATE-B）：合成激励对 GATE-A corr+ 锚幅值 max <1%、相位 max <1°；A/B 对 AH1；Ainf 刚体合成对 NREL 表 4（±2.5% 内）；附 ω ≤ 0.15 低频力矩残差带在 .h5↔AH1 口径的复查（GATE-A 记录 §4 处置项）。

**结论：GATE-B（16 体）通过，W6 关闭。** 全部判据满足（见 §3）；GATE-A 低频残差带在 .h5↔AH1 比对中不复现（带内幅值 max 0.0018%），维持「分体口径差异、非数据错误」的判读。下一步 W7 / GATE-C 前置仍为表 5 粘性阻尼拆分口径待 Saber 拍板（届时先按 16 体重算逐体投影面积份额）。

## 1. 被验文件与校验链

| 文件 | 大小 | SHA-256 / 说明 |
|---|---|---|
| `futi_16body.h5` | 115,902,180 B | `ceb2231f98df83b1d5a72280f3b8eb09154189be04864036af436d27bc859b7c`（解压后实测；大小与运行日志记录分毫不差） |
| `futi_16body_hydro.mat` | 98,007,095 B | `fe2e7ecbbac7bed6694afe164fa57ad9b180bdbad124d96600afed08720c2ce4`（解压后实测） |
| `futi_16body.zip`（上两件打包） | 194,391,226 B | `6eeab5943af3822c7293e29d92d04ce064e1074ebfdfacf33a89c21d38b88497`，与 GitHub Release `16-output` 附件登记的 digest 一致；助理经浏览器下载后实测 |
| 运行日志 `bemio_futi_16body_log.txt` | 2,043 B | 入仓 `03-multibody-16body/w6-bemio/output/`；MD5 `0442effbbd6f992a6b070febeef24928` |

运行事实（日志）：2026-11-16 23:11:06 启动，MATLAB R2025a Update 1（25.1.0.2973910）；输入 AH1 15,506,571 B / LIS 70,936,631 B 与原件一致；readAQWA 162.7 s（Nb = 16、DOF = 96、47 频 0.02–2.10 rad/s、25 浪向，脚本断言全过）；radiationIRF 66.9 s；excitationIRF 28.3 s；writeBEMIOH5 11.9 s。脚本 = 入仓版 `03-multibody-16body/w6-bemio/bemio_futi_16body.m`（由 19 体已实跑 REV 1 脚本适配）。Ainf 在 readAQWA 后已存在（96×96），radiationIRF 后数值改变（首块 A11 764→968 等）——与 19 体同型，Ainf 由 radiationIRF 重算（LHFR 关、AH1 的 FIDD 块全零，readAQWA 不取用）。

复核脚本：`gate-b-check-16body.py`（本目录；由 19 体 `gate-b-check.py` 适配，结构项并入同一脚本），结果数据 `gate-b-results-16body.json`，合成阵 `gate-b-synthesis-16body.npz`（二进制，网页上传入仓本目录）。对照锚：GATE-A 的 `../gate-a-verification/excitation-full-spectrum-16body.npz` 之 `Fsyn_corr_plus`。

## 2. BEMIO 激励力约定（19 体已证，16 体再次验证成立）

.h5 逐体激励与 AH1 FORCERAO 的关系仍为 **F_h5 = conj(F_AH1) · exp(−ik·r_b)**（k = ω²/g，r_b 为各体重心水平坐标向浪向的投影）。复核时先逆变换（取共轭并乘 exp(−ik·r_b)，见脚本 §1）再比对；不逆变换直接比对会得到约 124% 量级的伪误差（19 体实测），不是数据错误。逆变换后逐体保真度见 §3.1（中位为机器精度量级），该约定在 16 体数据上同样精确成立。

## 3. 复核结果

### 3.1 激励力

- 逐体（逆变换后对 AH1 FORCERAO，5% 峰值掩膜，76,472 点）：复数相对误差中位 2.0×10⁻¹⁶、max 4.6×10⁻⁶；幅值误差中位 0、max 6.9×10⁻¹⁶；相位误差中位 ~0、max 2.7×10⁻⁴ °。即 .h5 逐体激励与 AH1 在印刷/存储精度内恒等。
- 合成（逐体 corr+ 修正、求和并输运到总重心，对 GATE-A corr+ 锚；逐浪向 5% 掩膜，5,683 点）：**幅值 max 0.386% <1% ✓、相位 max 0.187° <1° ✓**，中位均为 ~10⁻¹⁶ 量级。最不利点全在 Mz 近相消通道：幅值 max 在 Mz、120° 向、ω=1.85（|ref| 4.32×10⁴，通道峰值 8.17×10⁵）；相位 max 在 Mz、120° 向、ω=1.20。除 Mz 相消点外，其余全部点 ≤0.0003%。19 体同项实绩：0.357% / 0.168°，同型。
- **低频带复查（ω ≤ 0.15，705 点）：幅值 max 0.0018%、相位 max 3.5×10⁻⁴ °**——GATE-A 对整体单体基准见到的低频力矩残差带（≤6.04×10⁶ N·m/m、约峰值 5.4%）在 .h5↔AH1 之间**不复现**，与 19 体结论（带 max 0.0018%）一致：残差源于 16 体分体口径与整体单体基准之间的差异，不在 BEMIO 链路中。论文局限性按 GATE-A 记录 §4 的 16 体数值注明即可，GATE-B 侧无新增问题。

### 3.2 附加质量 / 辐射阻尼矩阵（A、B）

.h5 的 `added_mass/all`（×ρ）与 `radiation_damping/all`（×ρω）对 AH1 的 ADDEDMASS / DAMPING 全块（16×16 耦合块 × 47 频）逐频比对，误差以逐频峰值归一：A 最差相对误差 2.4×10⁻²⁰（ω=1.35）；B 最差 4.8×10⁻⁸（ω=2.10）。与 AH1 恒等（B 的 10⁻⁸ 量级为存储舍入）。

### 3.3 Ainf（无穷频率附加质量）

- .h5 的 `added_mass/inf_freq` 拼装阵与 hydro.mat 的 `hydro.Ainf` 转置逐元差 = 0.0（两处存储恒等）。
- 对称性残差：|Ainf − Ainfᵀ|max / |Ainf|max = 1.00×10⁻³（19 体 1.58×10⁻³，同量级；记录不强制对称化，与 19 体处置一致）。
- 刚体合成到静水面原点（SWL 塔轴）对 NREL/TP-5000-76773 表 4：A11 **+1.30%**、A33 **−0.80%**、A44 **−0.99%**、A55 **−0.99%**、A66 **+2.24%**、A15 **+0.34%**——全部在 ±2.5% 内 ✓，且与 19 体实绩（+1.30/−0.80/−0.99/−0.99/+2.24/+0.35%）逐项几乎重合（同一总几何的必然结果，互为旁证）。

### 3.4 结构项

- 逐体重心：.h5 `properties/cg` 与 AH1 COG 逐项最大偏差 **0.0 m**（逐位一致，体序与 GATE-A 一致）。
- DOF：逐体 `properties/dof` 合计 **96** ✓。
- 静水刚度：Σ `linear_restoring_stiffness`[2,2] ×ρg = **4,460,323.06**，与 GATE-A 的 AH1 合成 K33（4.460323×10⁶）一致到印刷精度（+0.0000013%）。
- 排水体积：Σ `properties/disp_vol` = **20,157.834 m³**，对整体单体 LIS 基准 20,157.80 为 +0.0002%（与 W4 的 LIS 口径 Σ 20,157.83 一致）。

## 4. 复核范围说明

- 本复核只判定 .h5 / hydro.mat 与 AH1、GATE-A 锚、NREL 表 4 之间的一致性；AQWA 本身的正确性已由 GATE-A 对整体单体基准关门，不在此重复。
- hydro.mat 只取用了 `hydro.Ainf` 与结构字段做交叉核对；IRF 时域核（radiation / excitation impulse response）未单独复核——其频域源数据（A、B、激励）已全量比对恒等，IRF 为确定性变换，与 19 体 GATE-B 范围一致。
- Release `16-output` 的页面说明为空；本记录与 FILES.md 末节登记（zip 与内含两文件的大小、SHA-256、存放位置）即为该 Release 的校验依据。
