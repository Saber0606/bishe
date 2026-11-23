#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 W7 装配数据脚本 w7-assembly-data-16body.m (2026-11-22)
只含数据数组, 不含 WEC-Sim 类 API 调用 (挂法以装配时软件实际功能为准).

来源 (只读):
  gate-a-verification/ah1-three-accounts-results.json  逐体质量/质心/惯量 (AH1 实跑)
  w7-wecsim-assembly/cd-weighted-damping-16body.json   S1/S2/S3 逐体 Bq
  w7-wecsim-assembly/area-shares-16body.json           S0 逐体 Bq (纯面积)
  界面半径: W1 §3 段界 7.409/16.91075/26.4125/35.91425/45.416 m
  约束位置: 链方向 (由该链 S1 段 AH1 质心方向定) x 界面半径, z = -16.5 (浮筒轴线)
"""
import json, math, os

SYNC = os.path.expanduser('~/workspace/bishe-sync/03-multibody-16body')
HERE = os.path.dirname(os.path.abspath(__file__))
ga = json.load(open(os.path.join(SYNC, 'gate-a-verification', 'ah1-three-accounts-results.json')))
cd = json.load(open(os.path.join(SYNC, 'w7-wecsim-assembly', 'cd-weighted-damping-16body.json')))
s0 = json.load(open(os.path.join(SYNC, 'w7-wecsim-assembly', 'area-shares-16body.json')))

pb = ga['per_body']
assert len(pb) == 16
names = [b['name'] for b in pb]
mass_t = [b['mass_ah1_t'] for b in pb]
cg = [b['cog_ah1'] for b in pb]
idiag = [b['Idiag_ah1'] for b in pb]
# 惯量积: AH1 记录含 Ixy (60 度链段 +2.289e6, 300 度链段 -2.289e6, 其余 0);
# Ixz/Iyz AH1 未列, 按各体关于过质心水平面的对称性为 0。
ixy = [b['Ixy_ah1'] for b in pb]
for i, v in enumerate(ixy, start=1):
    expect = 2289000.0 if 7 <= i <= 10 else (-2289000.0 if 12 <= i <= 15 else 0.0)
    assert v == expect, (i, v, expect)
print('[check] Ixy pattern OK: bodies 7-10 +2.289e6, 12-15 -2.289e6, others 0')
print(f'[check] total mass AH1 = {sum(mass_t):.2f} t (GATE-A synthesis 17854.16)')

def bq_table(scheme_json, key=None):
    rows = scheme_json['per_body'] if key is None else scheme_json['schemes'][key]['per_body']
    assert [r['body'].split()[0] for r in rows] == [str(i) for i in range(1, 17)]
    return [[r['Bq_surge'], r['Bq_sway'], r['Bq_heave']] for r in rows]

qS1 = bq_table(cd, 'S1_main'); qS2 = bq_table(cd, 'S2_ratio2.5'); qS3 = bq_table(cd, 'S3_no_radial_cal')
assert [r['body'].split()[0] for r in s0['bodies']] == [str(i) for i in range(1, 17)]
qS0 = [[r['Bq_surge'], r['Bq_sway'], r['Bq_heave']] for r in s0['bodies']]
for tag, q in (('S1', qS1), ('S2', qS2), ('S3', qS3), ('S0', qS0)):
    tot = [sum(r[d] for r in q) for d in range(3)]
    print(f'[check] {tag} totals = {tot[0]:.1f}/{tot[1]:.1f}/{tot[2]:.1f} (Table5 922500/922500/2296000)')
    assert all(abs(t - T) < 1.0 for t, T in zip(tot, (922500, 922500, 2296000)))

RADII = [7.409, 16.91075, 26.4125, 35.91425, 45.416]
CHAINS = [(1, [2, 3, 4, 5], 6), (1, [7, 8, 9, 10], 11), (1, [12, 13, 14, 15], 16)]
cons = []
for cen, segs, col in CHAINS:
    s1cg = cg[segs[0] - 1]
    nrm = math.hypot(s1cg[0], s1cg[1])
    d = (s1cg[0] / nrm, s1cg[1] / nrm)
    seq = [cen] + segs + [col]
    for k in range(5):
        cons.append((seq[k], seq[k + 1], [d[0] * RADII[k], d[1] * RADII[k], -16.5]))
assert len(cons) == 15
# cross-check: segment CG radii vs boundary midpoints
for cen, segs, col in CHAINS:
    for j, s in enumerate(segs):
        r_cg = math.hypot(cg[s - 1][0], cg[s - 1][1])
        r_mid = 0.5 * (RADII[j] + RADII[j + 1])
        assert abs(r_cg - r_mid) < 0.01, (s, r_cg, r_mid)
print('[check] 15 constraints built; segment CG radii match W1 boundary midpoints (<0.01 m)')

def fmt_mat(rows, fmt='{:.4f}'):
    return '\n'.join('    ' + ' '.join(fmt.format(v) for v in r) + ';' for r in rows)

em = cd['schemes']['S1_main']['emergent']
L = []
L.append('% w7-assembly-data-16body.m')
L.append('% W7 WEC-Sim 装配数据 (16 体): 质量/质心/惯量 + 逐体二次阻尼 + 约束体对与位置')
L.append('% 生成: 2026-11-22, 由 gen-w7-assembly-data.py 从下列已核记录自动生成, 勿手改数值')
L.append('%   质量/质心/惯量: GATE-A AH1 实跑三笔账 (ah1-three-accounts-results.json)')
L.append('%   阻尼 S1/S2/S3: cd-weighted-damping-16body.json; S0: area-shares-16body.json')
L.append('%   约束位置: W1 §3 段界半径 x 链方向, z=-16.5 (浮筒轴线高)')
L.append('% 口径: 装配时质量特性以 .h5 内置为准, 用本表逐项核对; 不一致以 AH1 值为准排查。')
L.append('% 阻尼挂法: body(i).quadDrag.drag = diag(quadDragS1(i,:)) (WEC-Sim 原生逐体二次拖曳,')
L.append('%   按体自身速度计, 静水口径); Z 对照版同位置填 diag(quadDragZ(i,:)) (全零)。')
L.append('%   注: WEC-Sim v7.1.0 bodyClass.checkInputs 要求 quadDrag.drag 为 6x6 矩阵')
L.append('%   (v7.1.0 bodyClass.m 第 173 行断言), 故用 diag() 由 1x6 对角系数展开;')
L.append('%   2026-11-22 首版注释写的 1x6 直接赋值在该版本下会触发断言失败, 已更正。')
L.append('% 惯量积更正 (2026-11-22): 首版漏记 Ixy — 60 度链段 +2.289e6, 300 度链段')
L.append('%   -2.289e6 (AH1 实跑值), 其余体为 0; Ixz/Iyz 按对称性为 0。装配时以')
L.append('%   body(i).inertiaProducts = bodyInertiaProducts(i,:) 赋值, 不得只赋对角。')
L.append('')
L.append('% ---- 体编号与名称 (顺序同 .h5 / AH1) ----')
L.append('bodyName = {' + ', '.join(f"'{n}'" for n in names) + "};")
L.append('')
L.append('% ---- 质量 (kg) / 质心 (m, 全局系) / 主惯量对角 (kg*m^2, 绕各自质心) ----')
L.append('bodyMass = [' + ' '.join(f'{m * 1000:.1f}' for m in mass_t) + "]';  % sum = 1.785416e7 kg")
L.append('bodyCG = [')
L.append(fmt_mat(cg, '{:.3f}'))
L.append('];')
L.append('bodyInertiaDiag = [')
L.append(fmt_mat(idiag, '{:.4e}'))
L.append('];')
L.append('% ---- 惯量积 (kg*m^2, 绕各自质心, 全局系): 列 = [Ixy Ixz Iyz] ----')
L.append('bodyInertiaProducts = [')
L.append(fmt_mat([[v, 0.0, 0.0] for v in ixy], '{:.4e}'))
L.append('];')
L.append('')
L.append('% ---- 逐体二次阻尼 (N*s^2/m^2): 列 = [surge sway heave roll pitch yaw], 转动列恒 0 (涌现) ----')
for tag, q in (('S1', qS1), ('S2', qS2), ('S3', qS3), ('S0', qS0)):
    var = 'quadDrag' + tag
    L.append(f'{var} = [')
    L.append('\n'.join('    ' + ' '.join(f'{v:.1f}' for v in r) + ' 0 0 0;' for r in q))
    L.append('];')
L.append('quadDragZ = zeros(16,6);  % 对照版: 粘性阻尼置零')
L.append('')
L.append('% ---- 15 个刚性约束: [体A 体B 位置x 位置y 位置z] (全局系, m) ----')
L.append('constraintPair = [')
for a, b, p in cons:
    L.append(f'    {a:2d} {b:2d}  {p[0]:9.4f} {p[1]:9.4f} {p[2]:7.2f};')
L.append('];')
L.append('')
L.append('% ---- GATE-C 单位运动试验涌现预测 (S1, 参考点=静水面塔轴点) ----')
L.append(f"% Bq55 pitch emergent = {em['Bq55']:.4e}  (Table5 1.676e10, 标定对齐)")
L.append(f"% Bq44 roll  emergent = {em['Bq44']:.4e}  (Table5 1.676e10, +3.1%)")
L.append(f"% Bq66 yaw   emergent = {em['Bq66']:.4e}  (Table5 4.798e10, -14.6%)")
L.append(f"% cross surge-pitch    = {em['cross_cg']:.4e} (质心约定) / {em['cross_drag']:.4e} (形心约定), Table5 8.918e6")
out = '\n'.join(L) + '\n'
path = os.path.join(HERE, 'w7-assembly-data-16body.m')
with open(path, 'w') as f:
    f.write(out)
print('written:', path, len(out), 'bytes')
