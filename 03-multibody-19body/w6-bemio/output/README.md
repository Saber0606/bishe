# W6 BEMIO 运行产出（output/）

本目录存放 W6 BEMIO 运行的产出文件。运行环境：Saber 本地 MATLAB R2025a Update 1（25.1.0.2973910），脚本 `../bemio_futi_19body.m` REV 1。输入为 19 体 AQWA 输出 `futi_19body.AH1` + `FUTI_19BODY.LIS`（原件位置见仓库 FILES.md）。

运行记录（据 `bemio_futi_19body_log.txt`）：2026-11-15 14:27 REV 1 全程跑通——readAQWA 255.6 s（Nb = 19、总自由度 114、频点 47、浪向 25 均核对通过）、radiationIRF 96.9 s、excitationIRF 32.5 s、writeBEMIOH5 13.5 s，产出 `futi_19body.h5`（155,612,740 B）。日志前半段另含初版脚本 14:14 的失败运行记录（文件名断言误设，见 PROGRESS.md）。

按仓库存储政策分流（网页上传单文件上限 25 MB；超过 100 MB 的文件无法进入 Git 文件树）：

| 文件 | 存放位置 | 状态（2026-11-15 核查） |
|---|---|---|
| `bemio_futi_19body_log.txt`（运行日志，5,023 B） | 本目录 | 已上传 |
| `futi_19body_hydro_after_read.mat`（readAQWA 后检查点） | ≤25 MB 时放本目录；>25 MB 改走 Release | 待上传 |
| `futi_19body.h5`（WEC-Sim 水动力文件，155,612,740 B） | Release `W6-output` 附件 | Release 已建，附件待传 |
| `futi_19body_hydro.mat`（完整 hydro 结构体，100+ MB） | Release `W6-output` 附件 | Release 已建，附件待传 |

注：Release 标签以实际创建的 `W6-output` 为准（https://github.com/Saber0606/bishe/releases/tag/W6-output）。附件上传完成后，其 SHA-256 登记到仓库根目录 `FILES.md` 末节，并在此表更新状态。GATE-B 复核记录不放在本目录，复核完成后另行成文放入 `../`（w6-bemio）或阶段 3 对应验证目录。
