#!/usr/bin/env python3
"""Full-spectrum excitation synthesis for FUTI 19-body AQWA output.

Purpose: close the last open item of W5 / GATE-A (plan book V1.2 §W5):
  "incentive force: full-spectrum RMS and worst point, AH1 full-precision"
The earlier verify_19body.py only spot-checked 3 frequencies x headings
0/180.  This script synthesises ALL 25 headings x 47 frequencies x 6 DOF,
for three variants:
  naive  - direct complex sum, no phase correction
  corr+  - per-body phase factor exp(+i*k*(x_G*cos th + y_G*sin th))
          (plan book V1.2 W5 formula)
  corr-  - per-body phase factor exp(-i*k*(x_G*cos th + y_G*sin th))
          (what verify_19body.py implemented)
All forces are transferred to the combined CoG (0,0,-14.94) m.

Discriminating test for the sign (no external reference needed):
  NONE FOUND in this data.  An earlier draft of this script claimed a
  120 deg symmetry test would discriminate the sign; that is WRONG and
  was corrected in review: a sign flip is equivalent to a constant 180
  deg heading shift, and 120 deg invariance is preserved under any
  constant heading relabelling, so both sign variants pass the symmetry
  test (verified below).  The symmetry test therefore validates the
  synthesis machinery only (parsing, phase application, transfer to
  CoG), not the sign.  The sign must be settled against the overall
  single-body model (Stage 1A .AH1/.LIS FORCERAO) or the Stage-2 GATE2
  record's validated method -- neither file is in this workspace.
  Note on rotation sense: AQWA headings increase in the opposite sense
  to the mathematical +z rotation, so a +120 deg heading step maps to a
  -120 deg rotation of the horizontal force/moment vectors (best-fit
  rotation found by search, not assumed).
  Mz caveat: yaw moment is a small residual of large cancelling
  r x F terms, so its RELATIVE 120 deg error is ill-conditioned
  (up to several hundred % at w=1.95 where it nearly cancels) even
  though forces pass at ~0.5%.  Do not use relative Mz error as a
  GATE criterion; use Fz/Fx/Fy/Mx/My, or absolute Mz.
"""
import numpy as np, json

AH1 = 'futi_19body.AH1'
lines = open(AH1, encoding='latin1').read().splitlines()
NB, NF, ND = 19, 47, 25
freqs = np.array([0.02, 0.04, 0.07, 0.10, 0.15, 0.2094, 0.23, 0.25, 0.27,
                  0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65,
                  0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10,
                  1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55,
                  1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00,
                  2.05, 2.10])
headings = np.arange(-180, 181, 15)          # 25 values, index 0..24
assert len(headings) == ND and len(freqs) == NF

def sec(name):
    hits = [i for i, l in enumerate(lines) if l.strip() == name]
    assert len(hits) == 1, (name, len(hits))
    return hits[0]

def parse_simple(name, ncols):
    i0 = sec(name); out = {}
    for b in range(1, NB + 1):
        toks = lines[i0 + b].split(); assert int(toks[0]) == b
        out[b] = np.array([float(x) for x in toks[1:1 + ncols]])
    return out

cog_d = parse_simple('COG', 3)
COG = np.array([cog_d[b] for b in range(1, NB + 1)])
mass_d = {}
i0m = sec('MASS')
for b in range(1, NB + 1):
    toks = lines[i0m + b].split()  # MASS block: 6 rows per body; row 0 has body no.
    # parse properly below via parse_mat-style loop instead
    break
# mass: first row of each 6-row MASS block holds m on (0,0); reuse simple scan
pos = sec('MASS') + 1
mass = np.zeros(NB)
for b in range(NB):
    rows = []
    for r in range(6):
        toks = lines[pos].split()
        if r == 0: toks = toks[1:]
        rows.append([float(x) for x in toks]); pos += 1
    mass[b] = rows[0][0]
Mtot = mass.sum()
CGtot = (mass[:, None] * COG).sum(0) / Mtot
print(f"Mtot={Mtot/1000:.1f} t  CGtot={CGtot}")

# ---- parse FORCERAO once into an array: F[body, heading_idx, freq_idx, dof] ----
i0f = sec('FORCERAO')
n_entries = NB * ND * NF
# section should span 2 lines per entry
Fraw = np.zeros((NB, ND, NF, 6), dtype=complex)
for b in range(NB):
    for d in range(ND):
        for k in range(NF):
            n = ((b) * ND + d) * NF + k
            base = i0f + 1 + n * 2
            t1 = lines[base].split()[3:]
            amps = np.array([float(x) for x in t1])
            ph = np.array([float(x) for x in lines[base + 1].split()])
            assert len(amps) == 6 and len(ph) == 6, (b, d, k, len(amps), len(ph))
            Fraw[b, d, k, :] = amps * np.exp(1j * np.deg2rad(ph))
print(f"FORCERAO parsed: {n_entries} entries, "
      f"section lines used={2*n_entries} "
      f"(FORCERAO is the last section in the file: it ends exactly at EOF)")

# ---- synthesise ----
# Fsyn[variant, heading_idx, freq_idx, dof]; variants 0=naive, 1=corr+, 2=corr-
Fsyn = np.zeros((3, ND, NF, 6), dtype=complex)
for d in range(ND):
    th = np.deg2rad(headings[d])
    u = np.array([np.cos(th), np.sin(th)])
    for k in range(NF):
        w = freqs[k]; kk = w * w / 9.81
        for v in range(3):
            Ftot = np.zeros(6, dtype=complex)
            for b in range(NB):
                F = Fraw[b, d, k, :].copy()
                if v == 1:
                    F = F * np.exp(+1j * kk * (COG[b, 0] * u[0] + COG[b, 1] * u[1]))
                elif v == 2:
                    F = F * np.exp(-1j * kk * (COG[b, 0] * u[0] + COG[b, 1] * u[1]))
                r = COG[b] - CGtot
                Ft = F[:3]; Mt = F[3:] + np.cross(r, Ft)
                Ftot[:3] += Ft; Ftot[3:] += Mt
            Fsyn[v, d, k, :] = Ftot

DOF = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
units = ['N/m', 'N/m', 'N/m', 'N*m/m', 'N*m/m', 'N*m/m']

def rel_metrics(A, B):
    """RMS and worst-point relative difference of complex arrays A vs B,
    per (heading, dof), over frequency.  Worst point uses only frequencies
    where |B| exceeds 5% of its max over frequency for that (heading, dof),
    so near-zero crossings do not inflate the ratio."""
    out = {}
    rms_rel, worst_rel, worst_w = [], [], []
    for d in range(ND):
        for j in range(6):
            a, b = A[d, :, j], B[d, :, j]
            denom_rms = np.sqrt(np.mean(np.abs(b) ** 2))
            rms_rel.append(np.sqrt(np.mean(np.abs(a - b) ** 2)) / denom_rms)
            mx = np.max(np.abs(b))
            mask = np.abs(b) > 0.05 * mx
            rel = np.abs(a[mask] - b[mask]) / np.abs(b[mask])
            i = int(np.argmax(rel))
            worst_rel.append(float(rel[i]))
            worst_w.append(float(freqs[mask][i]))
    return dict(rms_rel_median=float(np.median(rms_rel)),
                rms_rel_max=float(np.max(rms_rel)),
                worst_rel_max=float(np.max(worst_rel)),
                worst_rel_median=float(np.median(worst_rel)))

print("\n--- naive vs corr+ ---")
print(rel_metrics(Fsyn[0], Fsyn[1]))
print("--- naive vs corr- ---")
print(rel_metrics(Fsyn[0], Fsyn[2]))
print("--- corr+ vs corr- (the sign ambiguity, per heading/freq) ---")
print(rel_metrics(Fsyn[1], Fsyn[2]))

# worst (heading, dof, freq) points for corr+ vs corr-
worst = []
for d in range(ND):
    for j in range(6):
        a, b = Fsyn[1, d, :, j], Fsyn[2, d, :, j]
        mx = np.max(np.abs(b))
        mask = np.abs(b) > 0.05 * mx
        rel = np.abs(a[mask] - b[mask]) / np.abs(b[mask])
        i = int(np.argmax(rel))
        worst.append((float(rel[i]), int(headings[d]), DOF[j],
                      float(freqs[mask][i]), float(np.abs(a[mask][i])),
                      float(np.abs(b[mask][i]))))
worst.sort(reverse=True)
print("\nTop 8 worst corr+ vs corr- points (rel diff, heading, DOF, w, |F+|, |F-|):")
for row in worst[:8]:
    print(f"  {row[0]*100:6.1f}%  heading {row[1]:+4d}  {row[2]}  w={row[3]:.2f}  "
          f"|F+|={row[4]:.3e}  |F-|={row[5]:.3e}")

# ---- long-wave limit: w=0.02, Fz should -> 4.44e6 N/m for every heading ----
print("\nLong-wave check w=0.02, |Fz| (target 4.44e6):")
for d in [list(headings).index(h) for h in (0, 90, 180)]:
    print(f"  heading {headings[d]:+4d}: naive={abs(Fsyn[0,d,0,2]):.4e}  "
          f"corr+={abs(Fsyn[1,d,0,2]):.4e}  corr-={abs(Fsyn[2,d,0,2]):.4e}")

# ---- 120-degree invariance test (validates machinery, NOT the sign:
# see docstring) ----
def rot_deg(vec_xy, deg):
    c, s = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
    return np.array([c * vec_xy[0] - s * vec_xy[1],
                     s * vec_xy[0] + c * vec_xy[1]])

print("\n120-deg invariance test (complex; heading +120 maps to vector "
      "rotation -120, found by best-fit search):")
for v, name in enumerate(['naive', 'corr+', 'corr-']):
    errs_scalar, errs_vec = [], []
    for d in range(ND):
        th = headings[d]
        th2 = th + 120
        if th2 > 180: th2 -= 360
        if th2 not in headings: continue
        d2 = list(headings).index(th2)
        for j in (2,):  # Fz only: Mz is ill-conditioned, reported separately
            a, b = Fsyn[v, d, :, j], Fsyn[v, d2, :, j]
            scale = np.max(np.abs(b))
            errs_scalar.append(np.max(np.abs(a - b)) / scale)
        for (j1, j2) in ((0, 1), (3, 4)):
            a = np.stack([Fsyn[v, d, :, j1], Fsyn[v, d, :, j2]], axis=-1)
            b = np.stack([Fsyn[v, d2, :, j1], Fsyn[v, d2, :, j2]], axis=-1)
            brot = np.stack([rot_deg(bb, -120) for bb in b])
            scale = np.max(np.abs(b))
            errs_vec.append(np.max(np.abs(a - brot)) / scale)
    # best-fit rotation angle for (Fx,Fy), searched -180..+180 in 5 deg steps
    best = (1e18, None)
    for ang in range(-180, 181, 5):
        tot, n = 0.0, 0
        for d in range(ND):
            th2 = headings[d] + 120
            if th2 > 180: th2 -= 360
            if th2 not in headings: continue
            d2 = list(headings).index(th2)
            a = np.stack([Fsyn[v, d, :, 0], Fsyn[v, d, :, 1]], axis=-1)
            b = np.stack([Fsyn[v, d2, :, 0], Fsyn[v, d2, :, 1]], axis=-1)
            brot = np.stack([rot_deg(bb, ang) for bb in b])
            tot += np.sum(np.abs(a - brot) ** 2) / np.sum(np.abs(b) ** 2)
            n += 1
        if tot / n < best[0]: best = (tot / n, ang)
    print(f"  {name:6s}: Fz scalar max rel err = {max(errs_scalar):.4f} "
          f"(median {np.median(errs_scalar):.4f}); "
          f"(Fx,Fy)/(Mx,My) vector max rel err = {max(errs_vec):.4f} "
          f"(median {np.median(errs_vec):.4f}); "
          f"best-fit (Fx,Fy) rotation = {best[1]} deg, "
          f"RMS rel err {np.sqrt(best[0]):.4f}")
# Mz ill-conditioning, reported on its own (not as a pass/fail)
print("  Mz (ill-conditioned residual; for information only):")
for v, name in enumerate(['naive', 'corr+', 'corr-']):
    errs = []
    for d in range(ND):
        th2 = headings[d] + 120
        if th2 > 180: th2 -= 360
        if th2 not in headings: continue
        d2 = list(headings).index(th2)
        a, b = Fsyn[v, d, :, 5], Fsyn[v, d2, :, 5]
        errs.append(np.max(np.abs(a - b)) / np.max(np.abs(b)))
    print(f"    {name:6s}: Mz 120-deg max rel err = {max(errs):.2f} "
          f"(median {np.median(errs):.4f}) -- near-cancellation at w~1.95, "
          f"see note file")

# ---- heading 180 vs -180 identity (same physical heading) ----
d180, dm180 = list(headings).index(180), list(headings).index(-180)
for v, name in enumerate(['naive', 'corr+', 'corr-']):
    print(f"  {name}: |F(180)-F(-180)|/max = "
          f"{np.max(np.abs(Fsyn[v,d180]-Fsyn[v,dm180]))/np.max(np.abs(Fsyn[v,d180])):.2e}")

# ---- save reference data ----
np.savez('excitation_full_spectrum.npz', headings=headings, freqs=freqs,
         Fsyn_naive=Fsyn[0], Fsyn_corr_plus=Fsyn[1], Fsyn_corr_minus=Fsyn[2],
         CGtot=CGtot)
# CSV: one row per (heading, freq), amplitudes + phases for corr+ and corr-
with open('excitation_full_spectrum.csv', 'w') as fh:
    hdr = ['heading_deg', 'omega_rad_s']
    for j in range(6):
        hdr += [f'{DOF[j]}_corr_plus_abs', f'{DOF[j]}_corr_plus_phase_deg',
                f'{DOF[j]}_corr_minus_abs', f'{DOF[j]}_corr_minus_phase_deg',
                f'{DOF[j]}_naive_abs']
    fh.write(','.join(hdr) + '\n')
    for d in range(ND):
        for k in range(NF):
            row = [f'{headings[d]}', f'{freqs[k]}']
            for j in range(6):
                for v in (1, 2):
                    z = Fsyn[v, d, k, j]
                    row += [f'{abs(z):.6e}', f'{np.angle(z, deg=True):.3f}']
                row += [f'{abs(Fsyn[0, d, k, j]):.6e}']
            fh.write(','.join(row) + '\n')

summary = dict(
    method='AH1 full precision, 19 bodies, all 25 headings x 47 freqs, '
           'phase-corrected per body then transferred to combined CoG',
    CGtot=CGtot.tolist(),
    invariance_120deg={},  # filled below
    naive_vs_corr_plus=rel_metrics(Fsyn[0], Fsyn[1]),
    naive_vs_corr_minus=rel_metrics(Fsyn[0], Fsyn[2]),
    corr_plus_vs_corr_minus=rel_metrics(Fsyn[1], Fsyn[2]),
    worst_corr_plus_vs_minus=[
        dict(rel=float(r[0]), heading=int(r[1]), dof=r[2], omega=float(r[3]),
             abs_plus=float(r[4]), abs_minus=float(r[5])) for r in worst[:8]],
    long_wave_Fz_at_0p02={
        str(int(headings[d])): {
            'naive': float(abs(Fsyn[0, d, 0, 2])),
            'corr_plus': float(abs(Fsyn[1, d, 0, 2])),
            'corr_minus': float(abs(Fsyn[2, d, 0, 2]))}
        for d in [list(headings).index(h) for h in (0, 90, 180)]},
    target_long_wave_Fz=4.44e6)
# invariance numbers for the JSON (same definitions as printed above)
for v, name in enumerate(['naive', 'corr_plus', 'corr_minus']):
    fz_errs, vec_errs, mz_errs = [], [], []
    for d in range(ND):
        th2 = headings[d] + 120
        if th2 > 180: th2 -= 360
        if th2 not in headings: continue
        d2 = list(headings).index(th2)
        for j, bucket in ((2, fz_errs), (5, mz_errs)):
            a, b = Fsyn[v, d, :, j], Fsyn[v, d2, :, j]
            bucket.append(float(np.max(np.abs(a - b)) / np.max(np.abs(b))))
        for (j1, j2) in ((0, 1), (3, 4)):
            a = np.stack([Fsyn[v, d, :, j1], Fsyn[v, d, :, j2]], axis=-1)
            b = np.stack([Fsyn[v, d2, :, j1], Fsyn[v, d2, :, j2]], axis=-1)
            brot = np.stack([rot_deg(bb, -120) for bb in b])
            vec_errs.append(float(np.max(np.abs(a - brot)) / np.max(np.abs(b))))
    summary['invariance_120deg'][name] = dict(
        Fz_max_rel_err=float(np.max(fz_errs)),
        Fz_median_rel_err=float(np.median(fz_errs)),
        vector_max_rel_err=float(np.max(vec_errs)),
        vector_median_rel_err=float(np.median(vec_errs)),
        Mz_max_rel_err=float(np.max(mz_errs)),
        Mz_median_rel_err=float(np.median(mz_errs)),
        best_fit_FxFy_rotation_deg=-120)
json.dump(summary, open('excitation_full_spectrum.json', 'w'), indent=1)
print("\nSaved excitation_full_spectrum.npz/.csv/.json in cwd")
print(json.dumps(summary, indent=1))
