# W7 decision support #2 (16-body): A/B response test, viscous damping ON vs OFF,
# for the ASSEMBLED rigid platform (the level at which the zero-vs-Table5 claim
# lives). Frequency-domain 6-DOF solve about the total CoG:
#   [-w^2 (M + A(w)) + i w (B(w) + Beq) + K] X = F(w, heading)
# A, B: rigid synthesis of the as-run AH1 blocks (same transport as GATE-A).
# F:   GATE-A corr+ synthesised excitation (npz anchor, about total CoG).
# K:   diag(0,0,K33,K44,K55,0); K33 = GATE-A AH1 synthesis 4.460323e6;
#      K44/K55 = GATE-A direct waterplane aggregation (5.22067e9 / 5.22637e9).
# Case Z: Beq = 0.  Case V: Beq from NREL Table 5 quadratic matrix, transported
# from its SWL reference point to the total CoG by congruence, then equivalent-
# linearised per source DOF: Beq_ij = (8/3pi) * Bq_ij * w * a_j, iterated to
# self-consistency with the response amplitudes a_j (RAO case), or with
# a_j = sqrt(2) * sigma_Xj (JONSWAP spectrum case, stochastic linearisation).
# Scope: heave / roll / pitch are the stiffened DOFs under dispute; surge /
# sway / yaw carry no hydrostatic stiffness here (no mooring in this model),
# they are solved but not reported.
import numpy as np, json

AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
NPZ = '/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work/excitation-full-spectrum-16body.npz'
NB = 16
z = np.load(NPZ); freqs = np.array(z['freqs'], float); NF = len(freqs)
headings = np.array(z['headings']); Fsyn = z['Fsyn_corr_plus']  # (25, 47, 6)
lines = open(AH1, encoding='latin1').read().splitlines()

def sec(name):
    hits = [i for i, l in enumerate(lines) if l.strip() == name]
    assert len(hits) == 1; return hits[0]
def parse_simple(name, ncols):
    i0 = sec(name); out = {}
    for b in range(1, NB + 1):
        toks = lines[i0 + b].split(); assert int(toks[0]) == b
        out[b] = np.array([float(x) for x in toks[1:1 + ncols]])
    return out
def parse_mat(name):
    i0 = sec(name); mats = {}; pos = i0 + 1
    for b in range(1, NB + 1):
        rows = []
        for r in range(6):
            toks = lines[pos].split()
            if r == 0: assert int(toks[0]) == b; toks = toks[1:]
            rows.append([float(x) for x in toks]); pos += 1
        mats[b] = np.array(rows)
    return mats

COG = np.array([parse_simple('COG', 3)[b] for b in range(1, NB + 1)])
MASS = parse_mat('MASS')
mass = np.array([MASS[b][0, 0] for b in range(1, NB + 1)])
Mtot = mass.sum(); CGtot = (mass[:, None] * COG).sum(0) / Mtot
Itot = np.zeros((3, 3))
for b in range(NB):
    r = COG[b] - CGtot; m = mass[b]
    Itot += MASS[b + 1][3:, 3:] + m * ((r @ r) * np.eye(3) - np.outer(r, r))
M6 = np.zeros((6, 6)); M6[:3, :3] = Mtot * np.eye(3); M6[3:, 3:] = Itot

def skew(r): return np.array([[0, -r[2], r[1]], [r[2], 0, -r[0]], [-r[1], r[0], 0.]])
def S_mat(r):
    S = np.zeros((6, 6)); S[:3, :3] = np.eye(3); S[3:, 3:] = np.eye(3); S[3:, :3] = skew(r); return S

def block_reader(section):
    i0 = sec(section)
    def blk(i, j, k):
        n = ((i - 1) * NB + (j - 1)) * NF + (k - 1); base = i0 + 1 + n * 6; rows = []
        for r in range(6):
            toks = lines[base + r].split()
            if r == 0: toks = toks[3:]
            rows.append([float(x) for x in toks])
        return np.array(rows)
    return blk
add_blk = block_reader('ADDEDMASS'); dmp_blk = block_reader('DAMPING')
Slist = [S_mat(COG[i] - CGtot) for i in range(NB)]
def synth(blk, k):
    M = np.zeros((6, 6))
    for i in range(NB):
        for j in range(NB):
            M += Slist[i] @ blk(i + 1, j + 1, k) @ Slist[j].T
    return M
Aarr = np.stack([synth(add_blk, k) for k in range(1, NF + 1)])
Barr = np.stack([synth(dmp_blk, k) for k in range(1, NF + 1)])
print("A/B synthesised for all 47 freqs")

K = np.diag([0., 0., 4.460323e6, 5.22067e9, 5.22637e9, 0.])
Bq_swl = np.array([
    [9.225e5, 0, 0, 0, -8.918e6, 0],
    [0, 9.225e5, 0, 8.918e6, 0, 0],
    [0, 0, 2.296e6, 0, 0, 0],
    [0, 8.918e6, 0, 1.676e10, 0, 0],
    [-8.918e6, 0, 0, 0, 1.676e10, 0],
    [0, 0, 0, 0, 0, 4.798e10]])
r_swl = np.array([0., 0., 0.]) - CGtot  # SWL tower-axis point rel. to total CoG
S_swl = S_mat(r_swl)
Bq = S_swl @ Bq_swl @ S_swl.T
print(f"Bq transported to CoG: diag = {np.diag(Bq)}")

F8 = 8 / (3 * np.pi)
def solve_case(k, F, viscous, a_init=None):
    w = freqs[k]
    D0 = -w**2 * (M6 + Aarr[k]) + 1j * w * Barr[k] + K
    if not viscous:
        return np.linalg.solve(D0, F), None
    a = np.array(a_init, float) if a_init is not None else \
        np.array([1., 1., 1., 0.02, 0.02, 0.02])
    X = None
    for it in range(500):
        Beq = F8 * Bq * (w * a)[None, :]
        X = np.linalg.solve(D0 + 1j * w * Beq, F)
        a_new = np.abs(X)
        if np.max(np.abs(a_new - a) / np.maximum(a, 1e-12)) < 1e-7:
            a = a_new; break
        a = 0.5 * a + 0.5 * a_new
    return X, a

hidx = {h: i for i, h in enumerate(headings)}
out = {'freqs': freqs.tolist(), 'cases': {}}
rao_store = {}
for hdeg in [0, 90]:
    hi = hidx[hdeg]
    XZ = np.zeros((NF, 6), complex); XV = np.zeros((NF, 6), complex)
    for k in range(NF):
        XZ[k], _ = solve_case(k, Fsyn[hi, k], False)
        XV[k], _ = solve_case(k, Fsyn[hi, k], True)
    rao_store[hdeg] = (XZ, XV)
    pk = {}
    for nm, X, dof in [('heave', XZ, 2), ('heave', XV, 2)]:
        pass
    def peak(X, dof): 
        m = np.abs(X[:, dof]); i = int(np.argmax(m)); return float(m[i]), float(freqs[i])
    pk['heave_Z'] = peak(XZ, 2); pk['heave_V'] = peak(XV, 2)
    rot = 3 if hdeg == 90 else 4; rn = 'roll' if hdeg == 90 else 'pitch'
    pk[f'{rn}_Z_deg'] = (peak(XZ, rot)[0] * 180 / np.pi, peak(XZ, rot)[1])
    pk[f'{rn}_V_deg'] = (peak(XV, rot)[0] * 180 / np.pi, peak(XV, rot)[1])
    pk['heave_ratio'] = pk['heave_Z'][0] / pk['heave_V'][0]
    pk[f'{rn}_ratio'] = pk[f'{rn}_Z_deg'][0] / pk[f'{rn}_V_deg'][0]
    out['cases'][f'heading_{hdeg}'] = pk
    print(f"heading {hdeg}: heave peak Z={pk['heave_Z'][0]:.1f} m/m @ {pk['heave_Z'][1]:.2f} | "
          f"V={pk['heave_V'][0]:.2f} m/m @ {pk['heave_V'][1]:.2f} | ratio x{pk['heave_ratio']:.1f}")
    print(f"           {rn} peak Z={pk[f'{rn}_Z_deg'][0]:.1f} deg/m @ {pk[f'{rn}_Z_deg'][1]:.2f} | "
          f"V={pk[f'{rn}_V_deg'][0]:.2f} deg/m @ {pk[f'{rn}_V_deg'][1]:.2f} | ratio x{pk[f'{rn}_ratio']:.1f}")

# sanity: long-wave heave limit
XZ0 = rao_store[0][0]
print(f"sanity: heave RAO Z @ w=0.02 = {abs(XZ0[0,2]):.3f} (expect ~Fz/K33 ~ 0.996)")

# ---- JONSWAP RMS comparison (stochastic linearisation for case V) ----
def jonswap(w, Hs, Tp, gamma=3.3):
    wp = 2 * np.pi / Tp
    sig = np.where(w <= wp, 0.07, 0.09)
    S = w**-5 * np.exp(-1.25 * (wp / w)**4) * gamma**np.exp(-(w - wp)**2 / (2 * sig**2 * wp**2))
    S = S / np.trapezoid(S, w) * (Hs / 4)**2
    return S
def rms_case(hdeg, Hs, Tp, viscous):
    hi = hidx[hdeg]; S = jonswap(freqs, Hs, Tp)
    if not viscous:
        XZ, _ = rao_store[hdeg][0], None
        var = np.trapezoid(np.abs(XZ)**2 * S[:, None], freqs, axis=0)
        return np.sqrt(var)
    a = np.array([0.5, 0.5, 0.5, 0.01, 0.01, 0.01])
    sig_x = None
    for it in range(60):
        XVa = np.zeros((NF, 6), complex)
        for k in range(NF):
            w = freqs[k]
            D0 = -w**2 * (M6 + Aarr[k]) + 1j * w * Barr[k] + K
            Beq = F8 * Bq * (w * a)[None, :]
            XVa[k] = np.linalg.solve(D0 + 1j * w * Beq, Fsyn[hi, k])
        var = np.trapezoid(np.abs(XVa)**2 * S[:, None], freqs, axis=0)
        sig_new = np.sqrt(var)
        if sig_x is not None and np.max(np.abs(sig_new - sig_x) / np.maximum(sig_x, 1e-12)) < 1e-6:
            sig_x = sig_new; break
        sig_x = sig_new; a = np.sqrt(2) * sig_x
    return sig_x

spec = {}
for hdeg in [0, 90]:
    for Tp in [6, 8, 10, 12, 14, 16, 18, 20]:
        sZ = rms_case(hdeg, 3.0, Tp, False); sV = rms_case(hdeg, 3.0, Tp, True)
        rot = 3 if hdeg == 90 else 4; rn = 'roll' if hdeg == 90 else 'pitch'
        row = dict(heading=hdeg, Tp=Tp, heave_Z=float(sZ[2]), heave_V=float(sV[2]),
                   heave_ratio=float(sZ[2] / sV[2]),
                   rot_Z_deg=float(sZ[rot] * 180 / np.pi), rot_V_deg=float(sV[rot] * 180 / np.pi),
                   rot_ratio=float(sZ[rot] / sV[rot]), rot_name=rn)
        spec[f'h{hdeg}_Tp{Tp}'] = row
        print(f"Hs=3 heading {hdeg} Tp={Tp:2d}s: heave RMS Z={row['heave_Z']:.3f} m vs V={row['heave_V']:.3f} m "
              f"(x{row['heave_ratio']:.2f}) | {rn} RMS Z={row['rot_Z_deg']:.3f} deg vs V={row['rot_V_deg']:.3f} deg (x{row['rot_ratio']:.2f})")
out['jonswap_Hs3'] = spec
json.dump(out, open('/home/hatch/workspace/graduation-design/stage3-correction-16body/w7-prep/rao-damping-ab-results.json', 'w'), indent=1)
# CSV of RAOs (heading 0 and 90): freq, heave Z/V, rot Z/V (deg)
import csv as _csv
with open('/home/hatch/workspace/graduation-design/stage3-correction-16body/w7-prep/rao-damping-ab.csv', 'w', newline='') as f:
    wr = _csv.writer(f)
    wr.writerow(['freq_rad_s', 'heave_Z_m_per_m_h0', 'heave_V_m_per_m_h0', 'pitch_Z_deg_per_m_h0', 'pitch_V_deg_per_m_h0',
                 'heave_Z_m_per_m_h90', 'heave_V_m_per_m_h90', 'roll_Z_deg_per_m_h90', 'roll_V_deg_per_m_h90'])
    XZ0, XV0 = rao_store[0]; XZ9, XV9 = rao_store[90]
    for k in range(NF):
        wr.writerow([f"{freqs[k]:.2f}", f"{abs(XZ0[k,2]):.4f}", f"{abs(XV0[k,2]):.4f}",
                     f"{abs(XZ0[k,4])*180/np.pi:.4f}", f"{abs(XV0[k,4])*180/np.pi:.4f}",
                     f"{abs(XZ9[k,2]):.4f}", f"{abs(XV9[k,2]):.4f}",
                     f"{abs(XZ9[k,3])*180/np.pi:.4f}", f"{abs(XV9[k,3])*180/np.pi:.4f}"])
print("saved rao-damping-ab-results.json + .csv")
