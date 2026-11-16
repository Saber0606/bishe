# W6 运行产出存放说明（16 体）

W6 于 2026-11-16 23:11 由 Saber 在本地 MATLAB R2025a Update 1 运行 `bemio_futi_16body.m` 完成（脚本在上一级 `../bemio_futi_16body.m`；日志 `bemio_futi_16body_log.txt` 与本说明同目录）。

| 产出 | 大小 | 存放 |
|---|---|---|
| `futi_16body.h5` | 115,902,180 B，SHA-256 `ceb2231f98df83b1d5a72280f3b8eb09154189be04864036af436d27bc859b7c` | 与 hydro.mat 打包为 `futi_16body.zip`，存 Release `16-output`（见下） |
| `futi_16body_hydro.mat` | 98,007,095 B，SHA-256 `fe2e7ecbbac7bed6694afe164fa57ad9b180bdbad124d96600afed08720c2ce4` | 同上 |
| `futi_16body.zip` | 194,391,226 B，SHA-256 `6eeab5943af3822c7293e29d92d04ce064e1074ebfdfacf33a89c21d38b88497`（与 GitHub 记录的附件 digest 一致） | Release `16-output`：https://github.com/Saber0606/bishe/releases/tag/16-output |
| `futi_16body_hydro_after_read.mat` | —（readAQWA 后检查点） | 仅 Saber 本地保留，不入仓（可由 AH1+LIS 重跑再生成） |
| `bemio_futi_16body_log.txt` | 2,043 B | 本目录（仓库文件树内） |

GATE-B 复核已通过（2026-11-16）：记录与脚本在 `../../gate-b-verification/`。校验方法：下载 zip 后核 SHA-256 应与上表一致；解压后两文件再分别核 SHA-256。
