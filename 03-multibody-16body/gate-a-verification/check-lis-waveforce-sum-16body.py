# -*- coding: utf-8 -*-
"""
Independent print-precision cross-check (16-body version of the
19-body check-lis-waveforce-sum.py):
  sum over 16 bodies of the complex FK+DIFFRACTION wave-force tables
  printed in futi_16body.LIS vs the single-body model's combined table
  in FUTI_LOWFREQ.LIS, at the same (omega, heading).
Methods: plain / transfer (moment transport only) / corr+ (per-body
exp(+i k (x_b cos th + y_b sin th)) first, then transfer).
COG_b and CG_total from the 16-body AH1 (full print precision there).
All values here are LIS print precision (amp 3 sig figs, phase 0.01 deg),
so the corr+ median is expected at the ~0.1-0.2% level (19-body: 0.168%).
"""
import re, numpy as np, json

LIS16 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.LIS'
LIS1 = '/home/hatch/workspace/bishe-sync/01-single-body-validation/output/FUTI_LOWFREQ.LIS'
AH1 = '/home/hatch/workspace/graduation-design/stage3-correction-16body/run-products-20261116/futi_16body.AH1'
OUT = '/home/hatch/workspace/graduation-design/stage3-correction-16body/gate-a-work/check-lis-waveforce-sum-16body-results.json'
NB = 16
FREQS = [0.02, 0.04, 0.07, 0.10, 0.15, 0.2094, 0.23, 0.25, 0.27, 0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.05, 2.10]
HEADINGS = list(range(-180, 181, 15))
DOF = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']

lines = open(AH1, encoding='latin1').read().splitlines()
i0 = [i for i, l in enumerate(lines) if l.strip() == 'COG'][0]
COG = []
for b in range(NB):
    t = lines[i0 + 1 + b].split(); assert int(t[0]) == b + 1
    COG.append([float(x) for x in t[1:4]])
COG = np.array(COG)
i0m = [i for i, l in enumerate(lines) if l.strip() == 'MASS'][0]
mass = np.zeros(NB); pos = i0m + 1
for b in range(NB):
    for r in range(6):
        t = lines[pos].split()
        if r == 0: mass[b] = float(t[1])
        pos += 1
CGtot = (mass[:, None] * COG).sum(0) / mass.sum()
print(f"COG parsed; CGtot={CGtot}, Mtot={mass.sum()/1000:.2f} t")

struct_re = re.compile(r'S\s*T\s*R\s*U\s*C\s*T\s*U\s*R\s*E\s+(\d+)')
row_re = re.compile(r'^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(.*)$')
KIND = 'FROUDE KRYLOV + DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY'

def parse_lis(path, expect_structs):
    text = open(path, encoding='utf-8', errors='replace').read().splitlines()
    blocks = {}; cur_struct = None; i = 0; n = 0
    while i < len(text):
        m = struct_re.search(text[i])
        if m: cur_struct = int(m.group(1))
        if text[i].strip() == KIND:
            rows = []; heading = None; j = i + 1
            while j < len(text) and len(rows) < 47:
                mm = row_re.match(text[j])
                if mm:
                    toks = mm.group(3).split()
                    if len(toks) == 13: heading = float(toks[0]); vals = toks[1:]
                    elif len(toks) == 12: vals = toks
                    else: vals = None
                    if vals is not None and len(vals) == 12:
                        rows.append([float(v) for v in vals])
                j += 1
            if len(rows) == 47 and heading is not None:
                arr = np.array(rows); amp = arr[:, 0::2]; pha = np.radians(arr[:, 1::2])
                key = (cur_struct, int(round(heading)))
                assert key not in blocks, f"dup {key}"
                blocks[key] = amp * np.exp(1j * pha); n += 1
            i = j
        else:
            i += 1
    print(f"{path.split('/')[-1]}: FK+DIFF freq-blocks parsed = {n} (expect {expect_structs*25})")
    assert n == expect_structs * 25
    return blocks

b16 = parse_lis(LIS16, 16)
b1 = parse_lis(LIS1, 1)

def synth(heading, method):
    th = np.radians(heading); u = np.array([np.cos(th), np.sin(th)])
    out = np.zeros((47, 6), dtype=complex)
    for k, w in enumerate(FREQS):
        kk = w * w / 9.81; Ftot = np.zeros(6, dtype=complex)
        for b in range(NB):
            F = b16[(b + 1, heading)][k].copy()
            if method == 'corr+':
                F = F * np.exp(+1j * kk * (COG[b, 0] * u[0] + COG[b, 1] * u[1]))
            if method == 'plain':
                Ftot += F
            else:
                r = COG[b] - CGtot
                Mt = F[3:] + np.cross(r, F[:3])
                Ftot[:3] += F[:3]; Ftot[3:] += Mt
        out[k] = Ftot
    return out

results = {}
print("\nFull spectrum (25 headings x 47 freqs x 6 dof, 5% peak mask per heading/dof):")
for method in ['plain', 'transfer', 'corr+']:
    errs = []
    for h in HEADINGS:
        S = synth(h, method); R = b1[(1, h)]
        for dof in range(6):
            peak = np.abs(R[:, dof]).max(); mask = np.abs(R[:, dof]) > 0.05 * peak
            errs.append(np.abs(S[mask, dof] - R[mask, dof]) / np.abs(R[mask, dof]))
    e = np.concatenate(errs)
    print(f"  [{method:>8}] masked pts={e.size}  median={np.median(e)*100:.3f}%  p95={np.percentile(e,95)*100:.2f}%  max={e.max()*100:.1f}%")
    results[f"fullspec {method}"] = {"median_pct": float(np.median(e) * 100),
                                     "p95_pct": float(np.percentile(e, 95) * 100),
                                     "max_pct": float(e.max() * 100), "n": int(e.size)}
json.dump(results, open(OUT, 'w'), indent=1)
print(f"\nsaved {OUT}")
