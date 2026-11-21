#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16 体 W7 粘性阻尼 Cd 加权面积分配 + 装配涌现对账 + 垂向径向标定 (2026-11-21)

方案 (Saber 2026-11-21 采纳助理推荐方案):
  水平向 (surge/sway): 按迎流投影面积加权, Cd 先验 DNV-RP-C205 形状系数
      立柱 (圆柱) Cd=1.2, 浮筒段 (箱型) Cd=2.0, 比例 r=5/3.
      分配 q_i = Cd_i*A_i / sum(Cd*A) * 表5方向总量 -> 平动总量精确守恒.
  垂向 (heave): 面积分配 x 径向标定权重 w_i = 1/(1+beta*(rho_i/rho_max)^3),
      beta 由"装配后纵摇涌现二次阻尼 = 表5 的 1.676e10"一个方程解出.
      动机: 纯面积/Cd 分配下垂向拖曳在大半径处经 |x|^3 杠杆涌现的纵摇阻尼
      约为表5 的 2.7 倍 (Morison 分量叠加与 CFD 四工况不自洽), 须以纵摇
      工况为第二个标定约束. 横摇涌现以同一权重计算并登记偏差 (120 度
      对称布局下应与纵摇接近).
  转动/交叉项不逐体赋值: 装配涌现, 本脚本给出涌现预测并与表5 对账.
      涌现公式 (逐体二次拖曳力作用于各体质心, 刚体装配, 参考点=静水面塔轴点):
        Bq55_em = sum( qx*|z|^3 + qz*|x|^3 )
        Bq44_em = sum( qy*|z|^3 + qz*|y|^3 )
        Bq66_em = sum( qx*|y|^3 + qy*|x|^3 )
        Bq51_em = sum( qx*z_cg )          (质心约定)
                或 sum( qx*z_drag )       (拖曳形心约定: 立柱 -10, 浮筒段 -16.5)
  敏感性变体: S2 = 水平比例 2.5; S3 = 无径向标定 (beta=0); S0 = 纯面积
      (已存 area-shares-16body.json, 本脚本以 r=1 复算校验一致性).

输入 (只读):
  bishe-sync/03-multibody-16body/w7-wecsim-assembly/area-shares-16body.json
      逐体迎流投影面积 + 表5 对角总量 (W1 精确几何)
  bishe-sync/03-multibody-16body/gate-a-verification/ah1-three-accounts-results.json
      AH1 实跑逐体质心 (涌现计算用)
输出: cd-weighted-damping-16body.json (与本脚本同目录)
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = os.path.expanduser('~/workspace/bishe-sync/03-multibody-16body')
with open(os.path.join(SYNC, 'w7-wecsim-assembly', 'area-shares-16body.json')) as f:
    AREA = json.load(f)
with open(os.path.join(SYNC, 'gate-a-verification', 'ah1-three-accounts-results.json')) as f:
    GATEA = json.load(f)

T5 = AREA['table5_diag']            # surge/sway/heave 二次阻尼总量 (N s^2/m^2)
T5_44 = T5_55 = 1.676e10            # 表5 roll/pitch (N m s^2/rad^2)
T5_66 = 4.798e10                    # 表5 yaw
T5_CROSS = 8.918e6                  # 表5 |surge-pitch| = |sway-roll| (N s^2/m)
CD_COL_H, CD_SEG_H = 1.2, 2.0       # DNV-RP-C205: 圆柱 1.2 / 矩形截面 2.0
RHO_MAX = 51.75                     # 外柱质心半径 (m)

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

def distribute(cd_h_ratio, beta):
    """返回逐体 q 表 {n: {surge,sway,heave}}; cd_h_ratio = Cd_SEG/Cd_COL (水平)."""
    q = {}
    for d in ('surge', 'sway'):
        cd = {b['n']: (cd_h_ratio if not b['col'] else 1.0) for b in bodies}
        den = sum(cd[b['n']] * b['A'][d] for b in bodies)
        for b in bodies:
            q.setdefault(b['n'], {})[d] = cd[b['n']] * b['A'][d] / den * T5[d]
    den = 0.0
    w = {}
    for b in bodies:
        w[b['n']] = 1.0 / (1.0 + beta * (b['rho'] / RHO_MAX) ** 3)
        den += w[b['n']] * b['A']['heave']
    for b in bodies:
        q[b['n']]['heave'] = w[b['n']] * b['A']['heave'] / den * T5['heave']
    return q

def emergent(q):
    """装配涌现对账 (参考点 = 静水面塔轴点)."""
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

# --- S0 自检: r=1, beta=0 必须复现 area-shares-16body.json 的等 Cd 逐体值 ---
q0 = distribute(1.0, 0.0)
maxdev = 0.0
for b in AREA['bodies']:
    n = int(b['body'].split()[0])
    for d in ('surge', 'sway', 'heave'):
        maxdev = max(maxdev, abs(q0[n][d] - b['Bq_' + d]) / b['Bq_' + d])
print(f'[self-check] r=1,beta=0 vs area-shares JSON: max rel dev = {maxdev:.2e}')
assert maxdev < 1e-9

# --- 主方案 S1: r=5/3; beta 二分求解 Bq55_em(beta) = T5_55 ---
r_main = CD_SEG_H / CD_COL_H
def pitch_em(beta):
    return emergent(distribute(r_main, beta))['Bq55']
lo, hi = 0.0, 1.0
while pitch_em(hi) > T5_55:
    hi *= 2
    assert hi < 1e7
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if pitch_em(mid) > T5_55:
        lo = mid
    else:
        hi = mid
beta_star = 0.5 * (lo + hi)
print(f'[solve] beta* = {beta_star:.4f}  (Bq55_em(beta=0) = {pitch_em(0.0):.4e}, target {T5_55:.4e})')

schemes = {}
for tag, r, beta in (('S1_main', r_main, beta_star),
                     ('S2_ratio2.5', 2.5, beta_star),
                     ('S3_no_radial_cal', r_main, 0.0)):
    q = distribute(r, beta)
    em = emergent(q)
    tot = {d: sum(q[b['n']][d] for b in bodies) for d in ('surge', 'sway', 'heave')}
    schemes[tag] = dict(cd_ratio_horizontal=r, beta=beta,
                        totals=tot, emergent=em, per_body=table(q))
    print(f"[{tag}] r={r:.4f} beta={beta:.4f} totals="
          f"{tot['surge']:.1f}/{tot['sway']:.1f}/{tot['heave']:.1f} "
          f"Bq44_em={em['Bq44']:.4e} Bq55_em={em['Bq55']:.4e} Bq66_em={em['Bq66']:.4e} "
          f"cross_cg={em['cross_cg']:.4e} cross_drag={em['cross_drag']:.4e}")

out = dict(
    meta=dict(date='2026-11-21',
              method='Cd-weighted projected-area distribution of NREL Table 5 quadratic '
                     'damping over 16 bodies; horizontal Cd prior DNV-RP-C205 '
                     '(cylinder 1.2 / rectangular 2.0); heave distribution radially '
                     'calibrated so assembled emergent pitch quadratic damping equals '
                     'Table 5; rotational/cross terms emergent, not assigned.',
              table5=dict(diag=T5, roll_pitch=T5_55, yaw=T5_66, cross_abs=T5_CROSS),
              reference_point='SWL tower-axis point (Table 5 reference); per-body '
                              'damping applied at body CG (as-run AH1 CGs).',
              self_check_S0_max_rel_dev=maxdev, beta_star=beta_star),
    schemes=schemes)
with open(os.path.join(HERE, 'cd-weighted-damping-16body.json'), 'w') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print('written: cd-weighted-damping-16body.json')
