# W6 BEMIO 运行产出（output/）

本目录存放 W6 BEMIO 运行的产出文件。运行环境：Saber 本地 MATLAB R2025a Update 1（25.1.0.2973910），脚本 `../bemio_futi_19body.m` REV 1，运行日期 2026-11-15。输入为 19 体 AQWA 输出 `futi_19body.AH1` + `FUTI_19BODY.LIS`（原件位置见仓库 FILES.md）。

按仓库存储政策分流（网页上传单文件上限 25 MB；超过 100 MB 的文件无法进入 Git 文件树）：

| 文件 | 存放位置 | 状态 |
|---|---|---|
| `bemio_futi_19body_log.txt`（运行日志） | 本目录（网页上传） | 待上传 |
| `futi_19body_hydro_after_read.mat`（readAQWA 后检查点） | ≤25 MB 时放本目录；>25 MB 改走 Release | 待上传 |
| `futi_19body.h5`（WEC-Sim 水动力文件，100+ MB） | Release `stage3-w6-bemio-output` 附件 | 待上传 |
| `futi_19body_hydro.mat`（完整 hydro 结构体，100+ MB） | Release `stage3-w6-bemio-output` 附件 | 待上传 |

Release 附件的下载链接与 SHA-256 在上传完成后登记到仓库根目录 `FILES.md` 末节，并在此表更新状态。GATE-B 复核记录不放在本目录，复核完成后另行成文放入 `../`（w6-bemio）或阶段 3 对应验证目录。
