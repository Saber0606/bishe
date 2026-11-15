# W6 BEMIO 运行产出（output/）

本目录存放 W6 BEMIO 运行的产出文件。运行环境：Saber 本地 MATLAB R2025a Update 1（25.1.0.2973910），脚本 `../bemio_futi_19body.m` REV 1。输入为 19 体 AQWA 输出 `futi_19body.AH1` + `FUTI_19BODY.LIS`（原件位置见仓库 FILES.md）。

运行记录（据 `bemio_futi_19body_log.txt`）：2026-11-15 14:27 REV 1 全程跑通——readAQWA 255.6 s（Nb = 19、总自由度 114、频点 47、浪向 25 均核对通过）、radiationIRF 96.9 s、excitationIRF 32.5 s、writeBEMIOH5 13.5 s，产出 `futi_19body.h5`（155,612,740 B）。日志前半段另含初版脚本 14:14 的失败运行记录（文件名断言误设，见 PROGRESS.md）。

**GATE-B 复核已通过（2026-11-15）**：`.h5` 数据经下载解压、SHA-256 校验后完成复核（激励力合成对 corr+ 锚：幅值最大偏差 0.357%、相位最大 0.168°，判据 <1% / <1°；Ainf 处理与 body 顺序确认）。复核记录、脚本与结果数据在 `../../gate-b-verification/`，不在本目录。

产出文件存放状态（2026-11-15 更新）：

| 文件 | 存放位置 | 状态 |
|---|---|---|
| `bemio_futi_19body_log.txt`（运行日志，5,023 B） | 本目录 | 已上传 |
| `futi_19body_hydro_after_read.mat`（readAQWA 后检查点） | ≤25 MB 时放本目录；>25 MB 改走 Release | 未上传（非必需：GATE-B 已用完整产出复核通过，此检查点可不再补传） |
| `futi_19body.h5`（WEC-Sim 水动力文件，155,612,740 B） | Release `W6-output` | 已存入（见下注） |
| `futi_19body_hydro.mat`（完整 hydro 结构体，131,962,908 B） | Release `W6-output` | 已存入（见下注） |

注：`.h5` 与 hydro.mat 于 2026-11-15 由 Saber 打包为一个 ZIP（`futi_19body.zip`，261,904,581 B）上传至 Release `W6-output`（https://github.com/Saber0606/bishe/releases/tag/W6-output），Saber 当日决定保留压缩包形式、不再拆分为单独附件；Release 的说明文字中已注明该 ZIP 内含上述两个文件。三个文件的 SHA-256 登记在仓库根目录 `FILES.md` 末节。解压后两文件的 SHA-256 应与 FILES.md 登记一致。
