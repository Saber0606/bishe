#!/usr/bin/env python3
"""W4 (second half) / W5 starting point, 16-body:
AH1 three-account check (per-body mass / CoG / inertia vs W2 v2 design,
full values from the W2 allocation JSON; totals synthesised to the
combined CoG and compared with the single-body Deck 03/04 anchors),
plus hydrostatic-stiffness synthesis, added-mass spot synthesis and
pure-floater natural frequencies (same machinery as the 19-body
verify_19body.py, NB=16).

AH1 print precision note: COG/COB are printed to 0.001 m, MASS/HYD
entries to 5 significant figures (%.4E).  Deviations at that scale are
print rounding, not model error; the design JSON carries the unrounded
design values that were filled into the dat Deck 03/04 (themselves
printed at %.4E in the dat, so the AH1 read-back cannot exceed that
precision).
"""
import numpy as np, json

AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
W2JSON = '/home/hatch/workspace/bishe-sync/03-multibody-16body/design-basis-w1-w2/design-16body-w2-allocation-results.json'
OUT = '/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work/ah1-three-accounts-results.json'

NB, NF = 16, 47
NAMES = ['CEN', '180_S1', '180_S2', '180_S3', '180_S4', '180_COL',
         '60_S1', '60_S2', '60_S3', '60_S4', '60_COL',
         '300_S1', '300_S2', '300_S3', '300_S4', '300_COL']
freqs = np.array([0.02, 0.04, 0.07, 0.10, 0.15, 0.2094, 0.23, 0.25, 0.27,
                  0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65,
                  0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10,
                  1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55,
                  1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00,
                  2.05, 2.10])

lines = open(AH1, encoding='latin1').read().splitlines()

def sec(name):
    hits = [i for i, l in enumerate(lines) if l.strip() == name]
    assert len(hits) == 1, (name, len(hits))
    return hits[0]

def parse_simple(name, ncols):
    i0 = sec(name); out = {}
    for b in range(1, NB + 1):
        toks = lines[i0 + b].split(); assert int(toks[0]) == b, (name, toks)
        out[b] = np.array([float(x) for x in toks[1:1 + ncols]])
    return out

def parse_mat(name):
    i0 = sec(name); mats = {}; pos = i0 + 1
    for b in range(1, NB + 1):
        rows = []
        for r in range(6):
            toks = lines[pos].split()
            if r == 0:
                assert int(toks[0]) == b; toks = toks[1:]
            rows.append([float(x) for x in toks]); pos += 1
        mats[b] = np.array(rows)
    return mats

COG = np.array([parse_simple('COG', 3)[b] for b in range(1, NB + 1)])
COB = np.array([parse_simple('COB', 3)[b] for b in range(1, NB + 1)])
DISP = np.array([parse_simple('DISPLACEMENT', 1)[b][0] for b in range(1, NB + 1)])
MASS = parse_mat('MASS')
HYD = parse_mat('HYDSTIFFNESS')
mass = np.array([MASS[b][0, 0] for b in range(1, NB + 1)])  # kg

design = json.load(open(W2JSON))
dbodies = design['bodies']

def skew(r):
    return np.array([[0, -r[2], r[1]], [r[2], 0, -r[0]], [-r[1], r[0], 0.]])
def S_mat(r):
    S = np.zeros((6, 6)); S[:3, :3] = np.eye(3); S[3:, 3:] = np.eye(3); S[3:, :3] = skew(r); return S
def T_mat(r):
    return S_mat(r).T

# ---------- per-body three accounts vs W2 v2 design ----------
per_body = []
for b, name in enumerate(NAMES):
    d = dbodies[name]
    # design inertia order in JSON: [Ixx, Iyy, Izz, Ixy, Ixz, Iyz] about own CoG
    dI = np.array([[d['inertia'][0], d['inertia'][3], d['inertia'][4]],
                   [d['inertia'][3], d['inertia'][1], d['inertia'][5]],
                   [d['inertia'][4], d['inertia'][5], d['inertia'][2]]])
    aI = MASS[b + 1][3:, 3:]
    per_body.append(dict(
        body=b + 1, name=name,
        mass_ah1_t=float(mass[b] / 1000), mass_design_t=float(d['mass_t']),
        mass_dev_pct=float((mass[b] / 1000 - d['mass_t']) / d['mass_t'] * 100),
        cog_ah1=COG[b].tolist(), cog_design=d['cog'],
        cog_dev_m=(COG[b] - np.array(d['cog'])).tolist(),
        Idiag_ah1=np.diag(aI).tolist(), Idiag_design=np.diag(dI).tolist(),
        Idiag_dev_pct=((np.diag(aI) - np.diag(dI)) / np.diag(dI) * 100).tolist(),
        Ixy_ah1=float(aI[0, 1]), Ixy_design=float(dI[0, 1]),
        disp_ah1_m3=float(DISP[b]), cob_ah1=COB[b].tolist()))
    print(f"{b+1:2d} {name:8s} m {mass[b]/1000:9.2f} vs {d['mass_t']:9.2f} t "
          f"({per_body[-1]['mass_dev_pct']:+.4f}%)  dCoG={np.array(per_body[-1]['cog_dev_m'])}  "
          f"dI%={np.array(per_body[-1]['Idiag_dev_pct']).round(4)}")

# ---------- totals synthesis ----------
Mtot = mass.sum()
CGtot = (mass[:, None] * COG).sum(0) / Mtot
Vtot = DISP.sum()
CBtot = (DISP[:, None] * COB).sum(0) / Vtot
Itot = np.zeros((3, 3))
for b in range(NB):
    r = COG[b] - CGtot; m = mass[b]
    Itot += MASS[b + 1][3:, 3:] + m * ((r @ r) * np.eye(3) - np.outer(r, r))

# anchors: single-body dat Deck 03/04
ANCH = dict(mass_t=17854.0, cog=np.array([0., 0., -14.940]),
            Idiag=np.array([1.251e10, 1.251e10, 2.367e10]))
dtots = design['totals']
print(f"\nTotal mass AH1 synth = {Mtot/1000:.2f} t (anchor 17854, design synth {dtots['mass_t']:.2f})")
print(f"Combined CoG = {CGtot} (anchor {ANCH['cog']}, design {dtots['cog']})")
print(f"Combined CoB (disp-weighted) = {CBtot} (single-body LIS (0,0,-13.6393))")
print(f"Total mesh displacement = {Vtot:.2f} m3 (single-body LIS 20157.80)")
print(f"Inertia about combined CoG diag = {np.diag(Itot)}")
print(f"  vs anchor  {ANCH['Idiag']}  dev% = {(np.diag(Itot)-ANCH['Idiag'])/ANCH['Idiag']*100}")
print(f"  vs design synth {dtots['inertia'][:3]} dev% = "
      f"{(np.diag(Itot)-np.array(dtots['inertia'][:3]))/np.array(dtots['inertia'][:3])*100}")
print(f"Inertia offdiag = {Itot[0,1]:.4e} {Itot[0,2]:.4e} {Itot[1,2]:.4e} (design Ixy total {dtots['inertia'][3]:.1f})")

# ---------- hydrostatic stiffness synthesis about combined CoG ----------
Ktot = np.zeros((6, 6))
for b in range(NB):
    r = COG[b] - CGtot
    Ktot += S_mat(r) @ HYD[b + 1] @ T_mat(r)
Kn = sum(HYD[b] for b in range(1, NB + 1))
print(f"\nK33 synth (transferred) = {Ktot[2,2]:.6e} ; naive sum = {Kn[2,2]:.6e} (single-body LIS 4.46027e6)")
print(f"K44/K55 by S H S^T congruence = {Ktot[3,3]:.6e} / {Ktot[4,4]:.6e} "
      f"(single-body LIS total 5.22930e9 / 5.22925e9) -- METHOD-LIMITED, see below")

# Direct waterplane aggregation for K44/K55 (reference-point safe):
# per body, AH1 HYD diag about its own CoG obeys
#   K44_b = rho*g*[ Iwp_x(CoG_b) + V_b*(zB_b - zG_b) ],  K33_b = rho*g*Awp_b
# so Iwp can be recovered per body and re-aggregated about the total CoG:
#   K44 = sum_b rho*g*[ Iwp_x,b + Awp_b*(yG_b-y_tot)^2 + V_b*(zB_b-z_tot) ]
# This is needed for the 16-body case because the central column's CoG
# (z=-3.731) sits 11.2 m above the total CoG: its HYD K44 about its own
# CoG is -2.08e8, and the S H S^T congruence (which worked to -0.64% for
# the 19-body case, where every CoG lay within ~2.7 m of the total CoG)
# does not transport that own-CoG buoyancy term correctly.
RHO_G = 1025 * 9.81
K44d = K55d = 0.0
for b in range(NB):
    h = HYD[b + 1]; V = DISP[b]; zb = COB[b, 2]; zg = COG[b, 2]
    Awp = h[2, 2] / RHO_G
    Iwx = h[3, 3] / RHO_G - V * (zb - zg)
    Iwy = h[4, 4] / RHO_G - V * (zb - zg)
    K44d += RHO_G * (Iwx + Awp * (COG[b, 1] - CGtot[1]) ** 2 + V * (zb - CGtot[2]))
    K55d += RHO_G * (Iwy + Awp * (COG[b, 0] - CGtot[0]) ** 2 + V * (zb - CGtot[2]))
print(f"K44/K55 by direct waterplane aggregation = {K44d:.6e} / {K55d:.6e} "
      f"(dev vs LIS total {(K44d/5.22930e9-1)*100:+.3f}% / {(K55d/5.22925e9-1)*100:+.3f}%)")

# ---------- added-mass synthesis (spot freqs) + natural frequencies ----------
i0a = sec('ADDEDMASS')
def added_block(i, j, k):
    n = ((i - 1) * NB + (j - 1)) * NF + (k - 1); base = i0a + 1 + n * 6; rows = []
    for r in range(6):
        toks = lines[base + r].split()
        if r == 0: toks = toks[3:]
        rows.append([float(x) for x in toks])
    return np.array(rows)
def synth_added(k):
    Aeq = np.zeros((6, 6))
    for i in range(1, NB + 1):
        Si = S_mat(COG[i - 1] - CGtot)
        for j in range(1, NB + 1):
            Aeq += Si @ added_block(i, j, k) @ T_mat(COG[j - 1] - CGtot)
    return Aeq

A_by_k = {}
print("\nAdded-mass synthesis about combined CoG:")
for k in [1, 6, 14, 47]:
    A = synth_added(k); A_by_k[k] = A
    print(f" w={freqs[k-1]:.4f}: A11={A[0,0]:.4e} A22={A[1,1]:.4e} A33={A[2,2]:.4e} "
          f"A44={A[3,3]:.4e} A55={A[4,4]:.4e} A66={A[5,5]:.4e} A15={A[0,4]:.4e} A24={A[1,3]:.4e}")

A33s, A55s, A44s = [], [], []
for k in range(1, NF + 1):
    A = synth_added(k); A33s.append(A[2, 2]); A55s.append(A[4, 4]); A44s.append(A[3, 3])
A33s, A55s, A44s = map(np.array, (A33s, A55s, A44s))
def natfreq(K, MI, Aarr):
    w = np.sqrt(K / (MI + Aarr)); diff = freqs - w
    for idx in range(NF - 1):
        if diff[idx] == 0: return float(freqs[idx])
        if diff[idx] * diff[idx + 1] < 0:
            t = diff[idx] / (diff[idx] - diff[idx + 1]); return float(freqs[idx] + t * (freqs[idx + 1] - freqs[idx]))
    return None
w_heave = natfreq(Ktot[2, 2], Mtot, A33s)
# pitch/roll use the direct-aggregation K (the S H S^T K is method-limited, above)
w_pitch = natfreq(K55d, Itot[1, 1], A55s)
w_roll = natfreq(K44d, Itot[0, 0], A44s)
print(f"\nNatural freq synth: heave={w_heave} (route target 0.315/0.316), pitch={w_pitch} (0.466/0.474), roll={w_roll}")

# symmetry of full added-mass matrix at k=47
full = np.zeros((NB * 6, NB * 6))
for i in range(1, NB + 1):
    for j in range(1, NB + 1):
        full[(i - 1) * 6:i * 6, (j - 1) * 6:j * 6] = added_block(i, j, 47)
asym = np.max(np.abs(full - full.T)) / np.max(np.abs(full))
print(f"Added-mass full-matrix asymmetry @2.10: {asym:.3e}")

out = dict(
    ah1=AH1, nb=NB,
    per_body=per_body,
    totals=dict(
        mass_t=float(Mtot / 1000), mass_dev_vs_anchor_pct=float((Mtot / 1000 - 17854) / 17854 * 100),
        cog=CGtot.tolist(), cog_design=dtots['cog'],
        cob_disp_weighted=CBtot.tolist(), disp_total_m3=float(Vtot),
        Idiag=np.diag(Itot).tolist(),
        I_dev_vs_anchor_pct=((np.diag(Itot) - ANCH['Idiag']) / ANCH['Idiag'] * 100).tolist(),
        I_dev_vs_design_pct=((np.diag(Itot) - np.array(dtots['inertia'][:3])) / np.array(dtots['inertia'][:3]) * 100).tolist(),
        I_offdiag=[float(Itot[0, 1]), float(Itot[0, 2]), float(Itot[1, 2])]),
    hydro=dict(K33_transferred=float(Ktot[2, 2]), K33_naive=float(Kn[2, 2]),
               K44_congruence=float(Ktot[3, 3]), K55_congruence=float(Ktot[4, 4]),
               K44_direct_agg=float(K44d), K55_direct_agg=float(K55d),
               K44_direct_dev_pct=float((K44d / 5.22930e9 - 1) * 100),
               K55_direct_dev_pct=float((K55d / 5.22925e9 - 1) * 100)),
    added_spot={str(freqs[k - 1]): dict(A11=float(A_by_k[k][0, 0]), A22=float(A_by_k[k][1, 1]),
                                        A33=float(A_by_k[k][2, 2]), A44=float(A_by_k[k][3, 3]),
                                        A55=float(A_by_k[k][4, 4]), A66=float(A_by_k[k][5, 5]),
                                        A15=float(A_by_k[k][0, 4]), A24=float(A_by_k[k][1, 3]))
                for k in A_by_k},
    natfreq=dict(heave=w_heave, pitch=w_pitch, roll=w_roll),
    added_asym_210=float(asym))
json.dump(out, open(OUT, 'w'), indent=1)
print(f"\nSaved {OUT}")
