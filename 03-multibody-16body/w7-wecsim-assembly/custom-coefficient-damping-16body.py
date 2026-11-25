#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16 体 W7 粘性阻尼 自定义系数面积分配 (K 版, 2026-11-22 草案; 2026-11-25 入仓)

背景: 导师意见 (Saber 2026-11-22 转述) —— 本结构非细长结构, 莫里森方程
  不适用, 粘性阻尼改用自定义系数法分配。本脚本即该口径:
  权重 = 投影面积 A(i) x 自定义系数 k(i) (按构件组给), 不再使用莫里森
  拖曳系数 Cd, 不引 DNV-RP-C205 先验。

K1 (运行三版之一, 2026-11-25 Saber 定): 水平向两组自定义系数取同值,
  即比值 r_k = k_段/k_柱 = 1.0, 分配退化为纯面积分配; 垂向同值 + 径向
  标定权重 w = 1/(1+beta*(rho/51.75)^3), beta=15.9886 由 "装配纵摇涌现
  二次阻尼 = 表5 1.676e10" 解出。
运行三版 (同一装配并行对比, GATE-C 后定主版): 5/3 版 (旧 S1, Cd 加权
  + 标定 beta=16.77)、1.0 版 (本脚本 K1)、置零版 Z (全零)。
敏感性/对照: K_sens1667 = r_k 5/3 (即旧 S1 的数值); K_sens250 = r_k 2.5
  (旧 S2 数值); K_nocal = r_k 1.0 且 beta=0 (旧 S0 数值, 无标定纯面积)。

分配 q_i = k_i*A_i / sum(k*A) * 表5方向总量 -> 平动总量构造守恒。
转动/交叉项不逐体赋值, 装配涌现, 公式与旧脚本一致 (参考点=静水面塔轴点):
  Bq55_em = sum( qx*|z|^3 + qz*|x|^3 ); Bq44_em = sum( qy*|z|^3 + qz*|y|^3 )
  Bq66_em = sum( qx*|y|^3 + qy*|x|^3 ); cross = sum( qx*z_cg ) 或 sum( qx*z_drag )

输入 (只读, 仓库待同步区):
  area-shares-16body.json (逐体投影面积 + 表5 对角总量)
  ah1-three-accounts-results.json (AH1 实跑逐体质心)
  cd-weighted-damping-16body.json (旧 S1/S2/S3, 仅作复现对照)
  area-shares-16body.json 内逐体 Bq (旧 S0, 仅作复现对照)
输出: custom-coefficient-damping-16body.json (与本脚本同目录)
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = os.path.expanduser('~/workspace/bishe-sync/03-multibody-16body')
with open(os.path.join(SYNC, 'w7-wecsim-assembly', 'area-shares-16body.json')) as f:
    AREA = json.load(f)
with open(os.path.join(SYNC, 'gate-a-verification', 'ah1-three-accounts-results.json')) as f:
    GATEA = json.load(f)
with open(os.path.join(SYNC, 'w7-wecsim-assembly', 'cd-weighted-damping-16body.json')) as f:
    OLD = json.load(f)

T5 = AREA['table5_diag']
T5_44 = T5_55 = 1.676e10
T5_66 = 4.798e10
T5_CROSS = 8.918e6
RHO_MAX = 51.75

bodies = []
cg = {b['body']: b['cog_ah1'] for b in GATEA['per_body']}
for b in AREA['bodies']:
    n = int(b['body'].split()[0])
    is_col = ('CEN' in b['body']) or ('COL' in b['body'])
    x, y, z = cg[n]
    bodies.append(dict(n=n, name=b['body'], col=is_col,
                       A=dict(surge=b['area_surge'], sway=b['area_sway'], heave=b['area_heave']),
                       cg=[x, y, z], rho=math.hypot(x, y),
                       z_drag=(-10.0 if is_col else -16.5)))
assert len(bodies) == 16

def distribute(k_ratio, beta):
    """k_ratio = k_seg/k_col (水平向); 垂向两组同 k, 只按面积 x 径向权重。"""
    q = {}
    for d in ('surge', 'sway'):
        k = {b['n']: (k_ratio if not b['col'] else 1.0) for b in bodies}
        den = sum(k[b['n']] * b['A'][d] for b in bodies)
        for b in bodies:
            q.setdefault(b['n'], {})[d] = k[b['n']] * b['A'][d] / den * T5[d]
    w = {}
    den = 0.0
    for b in bodies:
        w[b['n']] = 1.0 / (1.0 + beta * (b['rho'] / RHO_MAX) ** 3)
        den += w[b['n']] * b['A']['heave']
    for b in bodies:
        q[b['n']]['heave'] = w[b['n']] * b['A']['heave'] / den * T5['heave']
    return q

def emergent(q):
    s = dict(Bq44=0.0, Bq55=0.0, Bq66=0.0, cross_cg=0.0, cross_drag=0.0)
    for b in bodies:
        x, y, z = b['cg']; qq = q[b['n']]
        s['Bq55'] += qq['surge'] * abs(z) ** 3 + qq['heave'] * abs(x) ** 3
        s['Bq44'] += qq['sway'] * abs(z) ** 3 + qq['heave'] * abs(y) ** 3
        s['Bq66'] += qq['surge'] * abs(y) ** 3 + qq['sway'] * abs(x) ** 3
        s['cross_cg'] += qq['surge'] * abs(z)
        s['cross_drag'] += qq['surge'] * abs(b['z_drag'])
    return s

def table(q):
    return [dict(body=b['name'],
                 Bq_surge=round(q[b['n']]['surge'], 1),
                 Bq_sway=round(q[b['n']]['sway'], 1),
                 Bq_heave=round(q[b['n']]['heave'], 1)) for b in bodies]

def solve_beta(k_ratio):
    def pitch(beta):
        return emergent(distribute(k_ratio, beta))['Bq55']
    lo, hi = 0.0, 1.0
    while pitch(hi) > T5_55:
        hi *= 2
        assert hi < 1e7
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if pitch(mid) > T5_55:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

# --- 复现自检 1: r_k=5/3 + 旧 beta 应复现旧 S1 逐体表 ---
beta_old = OLD['meta']['beta_star']
q_old_repro = distribute(5.0 / 3.0, beta_old)
dev1 = 0.0
for row in OLD['schemes']['S1_main']['per_body']:
    n = int(row['body'].split()[0])
    for d, key in (('surge', 'Bq_surge'), ('sway', 'Bq_sway'), ('heave', 'Bq_heave')):
        dev1 = max(dev1, abs(q_old_repro[n][d] - row[key]) / row[key])
print(f'[check1] r_k=5/3,beta_old vs old S1 table: max rel dev = {dev1:.2e}')
assert dev1 < 2e-6  # 旧 JSON 逐体表保留 1 位小数, 舍入本身可致约 1.4e-6 相对偏差

# --- 复现自检 2: r_k=1, beta=0 应复现旧 S0 (area-shares 逐体 Bq) ---
q_s0 = distribute(1.0, 0.0)
dev2 = 0.0
for b in AREA['bodies']:
    n = int(b['body'].split()[0])
    for d in ('surge', 'sway', 'heave'):
        dev2 = max(dev2, abs(q_s0[n][d] - b['Bq_' + d]) / b['Bq_' + d])
print(f'[check2] r_k=1,beta=0 vs old S0 (area-shares): max rel dev = {dev2:.2e}')
assert dev2 < 1e-9

# --- 主版 K1: r_k=1.0, beta 重解 ---
beta_k1 = solve_beta(1.0)
print(f'[solve] K1 beta* = {beta_k1:.4f} (old S1 beta* = {beta_old:.4f})')

schemes = {}
for tag, r, beta in (('K1_main', 1.0, beta_k1),
                     ('K_sens1667_oldS1', 5.0 / 3.0, beta_old),
                     ('K_sens250_oldS2', 2.5, beta_old),
                     ('K_nocal_oldS0', 1.0, 0.0)):
    q = distribute(r, beta)
    em = emergent(q)
    tot = {d: sum(q[b['n']][d] for b in bodies) for d in ('surge', 'sway', 'heave')}
    schemes[tag] = dict(k_ratio_horizontal=r, beta=beta, totals=tot,
                        emergent=em, per_body=table(q))
    print(f"[{tag}] r_k={r:.4f} beta={beta:.4f} totals="
          f"{tot['surge']:.1f}/{tot['sway']:.1f}/{tot['heave']:.1f} "
          f"Bq44={em['Bq44']:.4e} Bq55={em['Bq55']:.4e} Bq66={em['Bq66']:.4e} "
          f"cross_cg={em['cross_cg']:.4e} cross_drag={em['cross_drag']:.4e}")

# 总量守恒断言 (全部版本)
for tag, s in schemes.items():
    for d in ('surge', 'sway', 'heave'):
        assert abs(s['totals'][d] / T5[d] - 1.0) < 1e-9, (tag, d)
print('[check3] all schemes: translational totals == Table 5 (rel dev < 1e-9)')

out = dict(
    meta=dict(date='2026-11-22', status='DRAFT - not yet in repo, pending Saber confirmation',
              method='Custom-coefficient projected-area distribution of NREL Table 5 '
                     'quadratic damping over 16 bodies (supervisor guidance 2026-11-22: '
                     'Morison equation not applicable to this non-slender structure; '
                     'allocation coefficient k is custom-defined, NOT a Morison drag '
                     'coefficient Cd; no DNV-RP-C205 prior). Main K1: k ratio '
                     'seg/col = 1.0 (pure area) horizontally; heave pure area x radial '
                     'calibration weight, beta solved so assembled emergent pitch '
                     'quadratic damping equals Table 5; rotational/cross emergent.',
              table5=dict(diag=T5, roll_pitch=T5_55, yaw=T5_66, cross_abs=T5_CROSS),
              reference_point='SWL tower-axis point (Table 5 reference)',
              check1_repro_oldS1_max_rel_dev=dev1,
              check2_repro_oldS0_max_rel_dev=dev2,
              beta_K1=beta_k1, beta_oldS1=beta_old),
    schemes=schemes)
with open(os.path.join(HERE, 'custom-coefficient-damping-16body.json'), 'w') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print('written: custom-coefficient-damping-16body.json')
