# W7 decision support #2b (16-body): A/B response test, REFINED frequency grid.
# The AQWA grid (0.03-0.05 rad/s spacing near resonance) cannot resolve the
# low-damping resonance peaks (bandwidth 2*zeta*w ~ 1e-4..2e-2 rad/s), so the
# coarse-grid run (rao-damping-ab-test.py) understates peak/RMS differences.
# Here the SMOOTH hydrodynamic quantities A(w), B(w), F(w) are cubic-spline
# interpolated onto a fine grid (dw = 0.0005 over w in [0.15, 0.65]) and the
# response is solved there; JONSWAP RMS uses a composite grid (fine inside
# [0.20, 0.60], AQWA grid outside). Everything else as in the coarse script.
# Verified input fact: the heave excitation has a deep cancellation notch at
# w ~ 0.33 in the SINGLE-BODY LIS itself (Fz = 1.26e5 vs 4.44e6 long-wave),
# i.e. AQWA physics of the whole platform, not a synthesis artefact.
import numpy as np, json
from scipy.interpolate import CubicSpline

AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
NPZ = '/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work/excitation-full-spectrum-16body.npz'
NB = 16
z = np.load(NPZ); freqs = np.array(z['freqs'], float); NF = len(freqs)
headings = np.array(z['headings']); Fsyn = z['Fsyn_corr_plus']
lines = open(AH1, encoding='latin1').read().splitlines()
def sec(name):
    hits = [i for i, l in enumerate(lines) if l.strip() == name]; assert len(hits) == 1; return hits[0]
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
MASS = parse_mat('MASS'); mass = np.array([MASS[b][0, 0] for b in range(1, NB + 1)])
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
K = np.diag([0., 0., 4.460323e6, 5.22067e9, 5.22637e9, 0.])
Bq_swl = np.array([[9.225e5,0,0,0,-8.918e6,0],[0,9.225e5,0,8.918e6,0,0],[0,0,2.296e6,0,0,0],
                   [0,8.918e6,0,1.676e10,0,0],[-8.918e6,0,0,0,1.676e10,0],[0,0,0,0,0,4.798e10]])
S_swl = S_mat(np.array([0., 0., 0.]) - CGtot); Bq = S_swl @ Bq_swl @ S_swl.T
F8 = 8 / (3 * np.pi)
hidx = {h: i for i, h in enumerate(headings)}

def spline_stack(arr):  # (NF,6,6) real -> function of w
    cs = [[CubicSpline(freqs, arr[:, i, j]) for j in range(6)] for i in range(6)]
    return lambda w: np.array([[cs[i][j](w) for j in range(6)] for i in range(6)])
def spline_cplx(vec):  # (NF,) complex
    return CubicSpline(freqs, vec.real), CubicSpline(freqs, vec.imag)
Afun, Bfun = spline_stack(Aarr), spline_stack(Barr)
Fspl = {h: [spline_cplx(Fsyn[hidx[h], :, j]) for j in range(6)] for h in [0, 90]}
def Ffun(h, w):
    return np.array([Fspl[h][j][0](w) + 1j * Fspl[h][j][1](w) for j in range(6)])
def Aof(w): return Aarr[np.argmin(abs(freqs - w))] if np.min(abs(freqs - w)) < 1e-9 else Afun(w)
def Bof(w): return Barr[np.argmin(abs(freqs - w))] if np.min(abs(freqs - w)) < 1e-9 else Bfun(w)

def solve_w(w, F, viscous, a0=None):
    D0 = -w**2 * (M6 + Aof(w)) + 1j * w * Bof(w) + K
    if not viscous: return np.linalg.solve(D0, F)
    a = np.array(a0, float) if a0 is not None else np.array([1., 1., 1., .02, .02, .02])
    for _ in range(800):
        X = np.linalg.solve(D0 + 1j * w * (F8 * Bq * (w * a)[None, :]), F)
        an = np.abs(X)
        if np.max(np.abs(an - a) / np.maximum(a, 1e-12)) < 1e-8: return X
        a = 0.5 * a + 0.5 * an
    return X

wf = np.arange(0.15, 0.6501, 0.0005)
res = {'fine_grid': [float(wf[0]), float(wf[-1]), 0.0005], 'peaks': {}}
rao_fine = {}
for h in [0, 90]:
    XZ = np.stack([solve_w(w, Ffun(h, w), False) for w in wf])
    XV = np.stack([solve_w(w, Ffun(h, w), True) for w in wf])
    rao_fine[h] = (XZ, XV)
    rot = 3 if h == 90 else 4; rn = 'roll' if h == 90 else 'pitch'
    def pk(X, d):
        m = np.abs(X[:, d]); i = int(np.argmax(m)); return float(m[i]), float(wf[i])
    p = dict(heave_Z=pk(XZ, 2), heave_V=pk(XV, 2), rot_Z=pk(XZ, rot), rot_V=pk(XV, rot), rot_name=rn)
    p['heave_ratio'] = p['heave_Z'][0] / p['heave_V'][0]; p['rot_ratio'] = p['rot_Z'][0] / p['rot_V'][0]
    p['rot_Z_deg'] = (p['rot_Z'][0] * 180 / np.pi, p['rot_Z'][1]); p['rot_V_deg'] = (p['rot_V'][0] * 180 / np.pi, p['rot_V'][1])
    res['peaks'][f'heading_{h}'] = p
    print(f"h={h} FINE peaks: heave Z={p['heave_Z'][0]:.1f} m/m @{p['heave_Z'][1]:.4f} | V={p['heave_V'][0]:.2f} @{p['heave_V'][1]:.4f} | x{p['heave_ratio']:.1f}")
    print(f"          {rn} Z={p['rot_Z_deg'][0]:.1f} deg/m @{p['rot_Z_deg'][1]:.4f} | V={p['rot_V_deg'][0]:.2f} @{p['rot_V_deg'][1]:.4f} | x{p['rot_ratio']:.1f}")

# composite-grid JONSWAP RMS
wc = np.concatenate([freqs[freqs < 0.20], np.arange(0.20, 0.6001, 0.001), freqs[freqs > 0.60]])
def jonswap(w, Hs, Tp, gamma=3.3):
    wp = 2 * np.pi / Tp; sig = np.where(w <= wp, 0.07, 0.09)
    S = w**-5 * np.exp(-1.25 * (wp / w)**4) * gamma**np.exp(-(w - wp)**2 / (2 * sig**2 * wp**2))
    return S / np.trapezoid(S, w) * (Hs / 4)**2
def rao_on(h, w, viscous, a_glob=None):
    if abs(w - freqs[np.argmin(abs(freqs - w))]) < 1e-9 and a_glob is None:
        k = int(np.argmin(abs(freqs - w)))
        D0 = -w**2 * (M6 + Aarr[k]) + 1j * w * Barr[k] + K
        return np.linalg.solve(D0, Fsyn[hidx[h], k])
    return solve_w(w, Ffun(h, w), viscous, a0=a_glob)
def rms(h, Hs, Tp, viscous):
    S = jonswap(wc, Hs, Tp)
    if not viscous:
        X = np.stack([rao_on(h, w, False) for w in wc])
        return np.sqrt(np.trapezoid(np.abs(X)**2 * S[:, None], wc, axis=0))
    a = np.array([0.5, 0.5, 0.5, 0.01, 0.01, 0.01]); sig = None
    for _ in range(40):
        X = np.stack([rao_on(h, w, True, a_glob=a) for w in wc])
        sn = np.sqrt(np.trapezoid(np.abs(X)**2 * S[:, None], wc, axis=0))
        if sig is not None and np.max(np.abs(sn - sig) / np.maximum(sig, 1e-12)) < 1e-5: sig = sn; break
        sig = sn; a = np.sqrt(2) * sig
    return sig
spec = {}
for h in [0, 90]:
    rot = 3 if h == 90 else 4; rn = 'roll' if h == 90 else 'pitch'
    for Tp in [6, 8, 10, 12, 13, 14, 15, 16, 18, 20]:
        sZ, sV = rms(h, 3.0, Tp, False), rms(h, 3.0, Tp, True)
        row = dict(Tp=Tp, heave_Z=float(sZ[2]), heave_V=float(sV[2]), heave_ratio=float(sZ[2]/sV[2]),
                   rot_Z_deg=float(sZ[rot]*180/np.pi), rot_V_deg=float(sV[rot]*180/np.pi),
                   rot_ratio=float(sZ[rot]/sV[rot]), rot_name=rn)
        spec[f'h{h}_Tp{Tp}'] = row
        print(f"Hs=3 h={h} Tp={Tp:2d}: heave RMS {row['heave_Z']:.3f} vs {row['heave_V']:.3f} (x{row['heave_ratio']:.2f}) | "
              f"{rn} RMS {row['rot_Z_deg']:.3f} vs {row['rot_V_deg']:.3f} deg (x{row['rot_ratio']:.2f})")
res['jonswap_Hs3'] = spec
json.dump(res, open('/home/hatch/workspace/graduation-design/stage3-correction-16body/w7-prep/rao-damping-ab-refined-results.json', 'w'), indent=1)
print("saved rao-damping-ab-refined-results.json")
