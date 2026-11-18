# Decision support for the W7 Table-5 question (16-body):
# rigid-body synthesised RADIATION damping ratio at the heave/pitch natural
# frequencies (from the as-run AH1 DAMPING/ADDEDMASS blocks, same transport
# machinery as the GATE-A verification script), vs the equivalent-linear
# VISCOUS damping ratio of the NREL Table 5 quadratic term at stated motion
# amplitudes. Resonance peak response scales ~ 1/zeta_total, so the factor
# (zeta_rad+zeta_visc)/zeta_rad is the peak overprediction if viscous = 0.
import numpy as np, json

AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
NB = 16
_npz = np.load('/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work/excitation-full-spectrum-16body.npz')
freqs = np.array(_npz['freqs'], dtype=float)
NF = len(freqs)
lines = open(AH1, encoding='latin1').read().splitlines()

def sec(name):
    hits = [i for i, l in enumerate(lines) if l.strip() == name]
    assert len(hits) == 1, (name, len(hits)); return hits[0]

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

def synth(blk, k):
    M = np.zeros((6, 6))
    for i in range(1, NB + 1):
        Si = S_mat(COG[i - 1] - CGtot)
        for j in range(1, NB + 1):
            M += Si @ blk(i, j, k) @ S_mat(COG[j - 1] - CGtot).T
    return M

add_blk = block_reader('ADDEDMASS'); dmp_blk = block_reader('DAMPING')

_k1 = int(np.where(freqs == 1.00)[0][0]) + 1
_A1 = synth(add_blk, _k1); _B1 = synth(dmp_blk, _k1)
print(f"sanity @w=1.00: A33={_A1[2,2]:.4e}, B33={_B1[2,2]:.4e}, B55={_B1[4,4]:.4e} "
      f"(radiation damping substantial at wave freq, ->0 at low freq: expected)")

def interp_syn(blk, wtarget, idxs):
    below = [k for k in range(1, NF + 1) if freqs[k - 1] <= wtarget]
    above = [k for k in range(1, NF + 1) if freqs[k - 1] >= wtarget]
    ks = [below[-1], above[0]] if below and above and below[-1] != above[0] else [above[0], above[0]]
    assert len(ks) == 2, (wtarget, ks)
    k1, k2 = ks; w1, w2 = freqs[k1 - 1], freqs[k2 - 1]
    M1, M2 = synth(blk, k1), synth(blk, k2)
    t = (wtarget - w1) / (w2 - w1)
    M = M1 + t * (M2 - M1)
    return {f'{a}{a}': float(M[i, i]) for i, a in enumerate([1, 2, 3, 4, 5, 6])}, M

out = {}
# GATE-A natural frequencies (pure floater, state A)
cases = {
    'heave': dict(w=0.31431, K=4.46027e6, Minertia=Mtot, dof='33', Bq=2.296e6,
                  amps=[('0.5 m', 0.5), ('1.0 m', 1.0), ('2.0 m', 2.0)]),
    'pitch': dict(w=0.46235, K=5.22925e9, Minertia=Itot[1, 1], dof='55', Bq=1.676e10,
                  amps=[('1 deg', np.deg2rad(1)), ('2 deg', np.deg2rad(2)), ('3 deg', np.deg2rad(3))]),
}
F = 8 / (3 * np.pi)  # equivalent-linearisation factor for quadratic damping
for name, c in cases.items():
    A, _ = interp_syn(add_blk, c['w'], None)
    B, _ = interp_syn(dmp_blk, c['w'], None)
    Aii = A[c['dof'] + c['dof']] if False else A[f"{c['dof'][0]}{c['dof'][0]}"]
    Bii = B[f"{c['dof'][0]}{c['dof'][0]}"]
    crit = 2 * np.sqrt(c['K'] * (c['Minertia'] + Aii))
    zrad = Bii / crit
    rows = []
    for lab, a in c['amps']:
        Beq = F * c['Bq'] * c['w'] * a
        zvis = Beq / crit
        rows.append(dict(amp=lab, zeta_visc_pct=zvis * 100,
                         peak_factor_if_zero=(zrad + zvis) / zrad))
    out[name] = dict(omega=c['w'], A_syn=Aii, B_rad_syn=Bii, crit=crit,
                     zeta_rad_pct=zrad * 100, amps=rows)
    print(f"{name}: w={c['w']}, A={Aii:.4e}, B_rad={Bii:.4e}, crit={crit:.4e}, "
          f"zeta_rad={zrad*100:.3f}%")
    for r in rows:
        print(f"   amp {r['amp']}: zeta_visc={r['zeta_visc_pct']:.2f}%, "
              f"peak x{r['peak_factor_if_zero']:.2f} if viscous=0")
json.dump(out, open('/home/hatch/workspace/graduation-design/stage3-correction-16body/w7-prep/zeta-rad-visc-16body.json', 'w'), indent=1)
print("saved zeta-rad-visc-16body.json")
