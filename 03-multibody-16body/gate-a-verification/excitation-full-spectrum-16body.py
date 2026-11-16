#!/usr/bin/env python3
"""W5 / GATE-A, 16-body: full-spectrum excitation synthesis + adjudication.

Part 1 (AH1, full print precision): parse futi_16body.AH1 FORCERAO for
16 bodies, synthesise to the combined CoG in three variants
  naive  - direct complex sum + moment transfer, no phase correction
  corr+  - per-body factor exp(+i*k*(x_G cos th + y_G sin th)) first
  corr-  - per-body factor exp(-i*k*(x_G cos th + y_G sin th)) first
then moment transfer M = sum(M_b + r_b x F_b), r_b = CoG_b - CGtot.
Saves excitation-full-spectrum-16body.npz / .csv (the corr+ array is
the GATE-B anchor, same role as the 19-body npz).

Part 2 (adjudication): compare the three variants against the overall
single-body benchmark FUTI_LOWFREQ.LIS (Stage 1A) combined
FK+DIFFRACTION tables (print precision: amp 3 sig figs, phase 0.01 deg),
25 headings x 47 freqs x 6 DOF, 5% peak mask per (heading, DOF) --
exactly the 19-body GATE-A adjudication protocol
(03-multibody-19body/gate-a-verification/adjudicate_sign.py).
Also: per-DOF and per-band breakdowns for corr+, spot checks, and the
omega <= 0.15 low-frequency moment residual band re-measured in the
16-body case.
"""
import re, json
import numpy as np

AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
LIS1 = '/home/hatch/workspace/bishe-sync/01-single-body-validation/output/FUTI_LOWFREQ.LIS'
OUTD = '/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work'
NB, NF, ND = 16, 47, 25
freqs = np.array([0.02, 0.04, 0.07, 0.10, 0.15, 0.2094, 0.23, 0.25, 0.27,
                  0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65,
                  0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10,
                  1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55,
                  1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00,
                  2.05, 2.10])
headings = np.arange(-180, 181, 15)
DOF = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
G = 9.81

lines = open(AH1, encoding='latin1').read().splitlines()
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

COG = np.array([parse_simple('COG', 3)[b] for b in range(1, NB + 1)])
pos = sec('MASS') + 1; mass = np.zeros(NB)
for b in range(NB):
    for r in range(6):
        toks = lines[pos].split()
        if r == 0:
            mass[b] = float(toks[1]); toks = toks[1:]
        pos += 1
Mtot = mass.sum(); CGtot = (mass[:, None] * COG).sum(0) / Mtot
print(f"Mtot={Mtot/1000:.2f} t  CGtot={CGtot}")

# ---- FORCERAO -> Fraw[body, heading, freq, dof] ----
i0f = sec('FORCERAO')
Fraw = np.zeros((NB, ND, NF, 6), dtype=complex)
for b in range(NB):
    for d in range(ND):
        for k in range(NF):
            n = (b * ND + d) * NF + k; base = i0f + 1 + n * 2
            amps = np.array([float(x) for x in lines[base].split()[3:]])
            ph = np.array([float(x) for x in lines[base + 1].split()])
            assert len(amps) == 6 and len(ph) == 6, (b, d, k)
            Fraw[b, d, k, :] = amps * np.exp(1j * np.deg2rad(ph))
n_entries = NB * ND * NF
print(f"FORCERAO parsed: {n_entries} entries; section ends at line "
      f"{i0f + 1 + 2 * n_entries} of {len(lines)} (file lines, 0-based sec start {i0f})")

# ---- synthesise: Fsyn[variant, heading, freq, dof] ----
Fsyn = np.zeros((3, ND, NF, 6), dtype=complex)
for d in range(ND):
    th = np.deg2rad(headings[d]); u = np.array([np.cos(th), np.sin(th)])
    for k in range(NF):
        kk = freqs[k] ** 2 / G
        for v in range(3):
            Ftot = np.zeros(6, dtype=complex)
            for b in range(NB):
                F = Fraw[b, d, k, :].copy()
                if v == 1: F = F * np.exp(+1j * kk * (COG[b, 0] * u[0] + COG[b, 1] * u[1]))
                elif v == 2: F = F * np.exp(-1j * kk * (COG[b, 0] * u[0] + COG[b, 1] * u[1]))
                r = COG[b] - CGtot
                Ftot[:3] += F[:3]; Ftot[3:] += F[3:] + np.cross(r, F[:3])
            Fsyn[v, d, k, :] = Ftot

np.savez(f'{OUTD}/excitation-full-spectrum-16body.npz', headings=headings, freqs=freqs,
         Fsyn_naive=Fsyn[0], Fsyn_corr_plus=Fsyn[1], Fsyn_corr_minus=Fsyn[2], CGtot=CGtot)
with open(f'{OUTD}/excitation-full-spectrum-16body.csv', 'w') as fh:
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
print("saved npz + csv")

# ---- long-wave control ----
print("\nLong-wave w=0.02 |Fz| (target ~4.44e6):")
for h in (0, 90, 180):
    d = list(headings).index(h)
    print(f"  h={h:+4d}: naive={abs(Fsyn[0,d,0,2]):.4e} corr+={abs(Fsyn[1,d,0,2]):.4e} corr-={abs(Fsyn[2,d,0,2]):.4e}")

# ================= Part 2: adjudication vs single-body LIS =================
text = open(LIS1, encoding='utf-8', errors='replace').read().splitlines()
row_re = re.compile(r'^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(.*)$')
def parse_blocks(kind):
    blocks = {}; i = 0
    while i < len(text):
        if text[i].strip() == kind:
            rows = []; j = i + 1; direction = None
            while j < len(text) and len(rows) < 47:
                m = row_re.match(text[j])
                if m:
                    toks = m.group(3).split()
                    if len(toks) == 13: direction = float(toks[0]); vals = toks[1:]
                    elif len(toks) == 12: vals = toks
                    else: vals = None
                    if vals is not None and len(vals) == 12:
                        rows.append([float(v) for v in vals])
                j += 1
            if len(rows) == 47 and direction is not None:
                arr = np.array(rows); amp = arr[:, 0::2]; pha = np.radians(arr[:, 1::2])
                blocks[int(round(direction))] = amp * np.exp(1j * pha)
            i = j
        else:
            i += 1
    return blocks

fk = parse_blocks('FROUDE KRYLOV FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
df = parse_blocks('DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
tot = parse_blocks('FROUDE KRYLOV + DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
print(f"\nLIS blocks: FK={len(fk)} DIF={len(df)} TOTAL={len(tot)}")
assert len(fk) == len(df) == len(tot) == 25
chk = max(np.abs((fk[int(h)] + df[int(h)]) - tot[int(h)]).max() for h in headings)
print(f"cross-check max |FK+DIF - TOTAL| = {chk:.3e} (print-rounding scale)")
F_lis = np.stack([tot[int(h)] for h in headings])  # (25,47,6)

def masked_stats(F, Flo=None, Fhi=None, dofs=range(6)):
    """5% peak mask per (heading,dof) over the FULL freq range (19-body
    protocol); optional freq sub-band restriction of the points counted."""
    errs, aerrs, perrs = [], [], []
    for ih in range(ND):
        for j in dofs:
            peak = np.abs(F_lis[ih, :, j]).max()
            mask = np.abs(F_lis[ih, :, j]) > 0.05 * peak
            if Flo is not None:
                mask &= (freqs >= Flo) & (freqs <= Fhi)
            a = F_lis[ih, mask, j]; b = F[ih, mask, j]
            errs.append(np.abs(b - a) / np.abs(a))
            aerrs.append(np.abs(np.abs(b) - np.abs(a)) / np.abs(a))
            perrs.append(np.degrees(np.angle(b * np.conj(a))))
    e = np.concatenate(errs); a_ = np.concatenate(aerrs); p = np.concatenate(perrs)
    return dict(n=int(e.size), cplx_med_pct=float(np.median(e) * 100),
                cplx_rms_pct=float(np.sqrt((e ** 2).mean()) * 100),
                cplx_p95_pct=float(np.percentile(e, 95) * 100),
                cplx_max_pct=float(e.max() * 100),
                amp_med_pct=float(np.median(a_) * 100), amp_max_pct=float(a_.max() * 100),
                phase_med_deg=float(np.median(np.abs(p))),
                phase_p95_deg=float(np.percentile(np.abs(p), 95)),
                phase_max_deg=float(np.abs(p).max()))

results = {}
print("\nFull-spectrum adjudication (5% mask):")
for v, name in enumerate(['naive', 'corr+', 'corr-']):
    s = masked_stats(Fsyn[v]); results[name] = s
    print(f"  {name:6s}: n={s['n']} cplx med={s['cplx_med_pct']:.3f}% rms={s['cplx_rms_pct']:.3f}% "
          f"p95={s['cplx_p95_pct']:.2f}% max={s['cplx_max_pct']:.1f}% | amp med={s['amp_med_pct']:.3f}% "
          f"| phase med={s['phase_med_deg']:.3f}deg p95={s['phase_p95_deg']:.2f}deg")

print("\ncorr+ per-DOF (full spectrum):")
per_dof = {}
for j in range(6):
    s = masked_stats(Fsyn[1], dofs=[j]); per_dof[DOF[j]] = s
    print(f"  {DOF[j]}: n={s['n']} cplx med={s['cplx_med_pct']:.3f}% p95={s['cplx_p95_pct']:.2f}% max={s['cplx_max_pct']:.2f}% phase med={s['phase_med_deg']:.3f}deg")

print("\ncorr+ per-band cplx median:")
bands = {}
for lo, hi in [(0.02, 0.15), (0.15, 0.30), (0.30, 0.36), (0.36, 2.10), (0.40, 2.10)]:
    s = masked_stats(Fsyn[1], Flo=lo, Fhi=hi); bands[f'{lo}-{hi}'] = s
    print(f"  w in [{lo},{hi}]: n={s['n']} med={s['cplx_med_pct']:.3f}% p95={s['cplx_p95_pct']:.2f}% max={s['cplx_max_pct']:.1f}%")
# Mx/My only, high band (19-body record: <=0.56% for w>=0.36, <=0.15% for w>=0.40)
for lo in (0.36, 0.40):
    s = masked_stats(Fsyn[1], Flo=lo, Fhi=2.10, dofs=[3, 4])
    print(f"  Mx/My w>={lo}: med={s['cplx_med_pct']:.3f}% max={s['cplx_max_pct']:.2f}%")
    bands[f'MxMy>={lo}'] = s

# worst corr+ point overall (masked)
worst = []
for ih in range(ND):
    for j in range(6):
        peak = np.abs(F_lis[ih, :, j]).max(); mask = np.abs(F_lis[ih, :, j]) > 0.05 * peak
        rel = np.abs(Fsyn[1, ih, mask, j] - F_lis[ih, mask, j]) / np.abs(F_lis[ih, mask, j])
        i = int(np.argmax(rel))
        worst.append((float(rel[i]), int(headings[ih]), DOF[j], float(freqs[mask][i])))
worst.sort(reverse=True)
print("\nTop 8 worst corr+ masked points:")
for r in worst[:8]: print(f"  {r[0]*100:7.2f}%  heading {r[1]:+4d}  {r[2]}  w={r[3]:.2f}")

# spot checks (19-body decisive points)
spots = {}
for (w, h, j) in [(1.15, 180, 4), (1.05, 180, 4)]:
    ih = list(headings).index(h); iw = list(freqs).index(w)
    ref = F_lis[ih, iw, j]
    spots[f'w{w}_h{h}_{DOF[j]}'] = dict(ref_abs=float(abs(ref)),
        **{name: float(abs(Fsyn[v, ih, iw, j])) for v, name in enumerate(['naive', 'corr+', 'corr-'])},
        corr_plus_ratio=float(abs(Fsyn[1, ih, iw, j]) / abs(ref)))
    print(f"spot w={w} h={h} {DOF[j]}: LIS={abs(ref):.4e} corr+={abs(Fsyn[1,ih,iw,j]):.4e} "
          f"(ratio {spots[f'w{w}_h{h}_{DOF[j]}']['corr_plus_ratio']:.3f}) corr-={abs(Fsyn[2,ih,iw,j]):.4e} naive={abs(Fsyn[0,ih,iw,j]):.4e}")

# ---- low-frequency band omega <= 0.15 (indices 0..4), corr+ ----
print("\nLow-freq band w<=0.15, corr+ vs LIS:")
low = {}
idx = [k for k in range(NF) if freqs[k] <= 0.15 + 1e-9]
for j in range(6):
    absdiffs, ratios, rels = [], [], []
    for ih in range(ND):
        peak = np.abs(F_lis[ih, :, j]).max()
        for k in idx:
            d = abs(Fsyn[1, ih, k, j] - F_lis[ih, k, j])
            absdiffs.append(d); ratios.append(d / peak)
            if abs(F_lis[ih, k, j]) > 0.05 * peak:
                rels.append(d / abs(F_lis[ih, k, j]))
    low[DOF[j]] = dict(max_abs=float(np.max(absdiffs)),
                       max_abs_over_peak_pct=float(np.max(ratios) * 100),
                       masked_rel_max_pct=float(np.max(rels) * 100) if rels else None,
                       masked_rel_med_pct=float(np.median(rels) * 100) if rels else None)
    print(f"  {DOF[j]}: max|diff|={low[DOF[j]]['max_abs']:.4e}  = {low[DOF[j]]['max_abs_over_peak_pct']:.2f}% of channel peak; "
          f"masked rel med={low[DOF[j]]['masked_rel_med_pct']:.2f}% max={low[DOF[j]]['masked_rel_max_pct']:.1f}%")
# where is the max moment diff?
best = (0, None)
for j in (3, 4, 5):
    for ih in range(ND):
        for k in idx:
            d = abs(Fsyn[1, ih, k, j] - F_lis[ih, k, j])
            if d > best[0]: best = (d, (DOF[j], int(headings[ih]), float(freqs[k]),
                                        float(d / np.abs(F_lis[ih, :, j]).max() * 100)))
print(f"  max moment |diff| in band: {best[0]:.4e} at {best[1]}")

summary = dict(method='AH1 FORCERAO, 16 bodies, corr+/corr-/naive synthesis to combined CoG, '
                      'vs single-body LIS FK+DIFF combined tables, 5% peak mask',
               CGtot=CGtot.tolist(), Mtot_t=float(Mtot / 1000),
               fk_dif_total_crosscheck_max=float(chk),
               variants=results, per_dof_corr_plus=per_dof, bands=bands,
               worst_corr_plus=[dict(rel_pct=r[0] * 100, heading=r[1], dof=r[2], omega=r[3]) for r in worst[:8]],
               spots=spots, low_freq_band=low,
               low_freq_max_moment=dict(abs=float(best[0]), dof=best[1][0], heading=best[1][1],
                                        omega=best[1][2], over_peak_pct=best[1][3]),
               long_wave_Fz_002={str(h): float(abs(Fsyn[1, list(headings).index(h), 0, 2])) for h in (0, 90, 180)})
json.dump(summary, open(f'{OUTD}/gate-a-adjudication-results.json', 'w'), indent=1)
print(f"\nSaved gate-a-adjudication-results.json")
print(json.dumps(summary, indent=1)[:2000])
