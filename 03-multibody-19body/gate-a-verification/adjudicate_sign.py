# -*- coding: utf-8 -*-
"""
GATE-A sign adjudication: overall single-body model (FUTI_LOWFREQ.LIS, Stage 1A)
vs 19-body synthesized excitation variants (naive / corr+ / corr-) from
excitation_full_spectrum.npz.

LIS prints Froude-Krylov and diffraction forces separately (AMP/PHASE per DOF,
w.r.t. structure CoG); total excitation = complex sum of the two.
LIS print precision: AMP 3 significant figures, PHASE 0.01 deg.
"""
import re
import numpy as np

LIS = 'FUTI_LOWFREQ.LIS'  # repo: 01-single-body-validation/output/FUTI_LOWFREQ.LIS
NPZ = 'excitation_full_spectrum.npz'  # same folder in repo: gate-a-verification/
DOF = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']

z = np.load(NPZ)
headings = z['headings']            # (25,)
freqs = z['freqs']                  # (47,)
variants = {'naive': z['Fsyn_naive'], 'corr+': z['Fsyn_corr_plus'], 'corr-': z['Fsyn_corr_minus']}

text = open(LIS, encoding='utf-8', errors='replace').read().splitlines()

row_re = re.compile(r'^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(.*)$')

def parse_blocks(kind):
    """Return dict heading -> array (47,6) complex, built from AMP/PHASE.
    Matches the EXACT stripped header line (substring matching would also
    catch the combined 'FROUDE KRYLOV + DIFFRACTION' tables)."""
    blocks = {}
    i = 0
    while i < len(text):
        if text[i].strip() == kind:
            # collect data rows after this header
            rows = []
            j = i + 1
            direction = None
            while j < len(text) and len(rows) < 47:
                m = row_re.match(text[j])
                if m:
                    toks = (m.group(3)).split()
                    if len(toks) == 13:      # direction + 12 values
                        direction = float(toks[0]); vals = toks[1:]
                    elif len(toks) == 12:    # 12 values only
                        vals = toks
                    else:
                        vals = None
                    if vals is not None and len(vals) == 12:
                        rows.append([float(v) for v in vals])
                j += 1
            if len(rows) == 47 and direction is not None:
                arr = np.array(rows)  # (47,12): amp,phase x6
                amp = arr[:, 0::2]
                pha = np.radians(arr[:, 1::2])
                blocks[int(round(direction))] = amp * np.exp(1j * pha)
            i = j
        else:
            i += 1
    return blocks

fk = parse_blocks('FROUDE KRYLOV FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
df = parse_blocks('DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
tot = parse_blocks('FROUDE KRYLOV + DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY')
print('FK blocks:', len(fk), ' DIF blocks:', len(df), ' TOTAL blocks:', len(tot))
assert len(fk) == 25 and len(df) == 25 and len(tot) == 25, 'expected 25 headings each'
assert sorted(fk) == [int(h) for h in headings] and sorted(tot) == [int(h) for h in headings]

# Cross-check: combined table must equal FK + diffraction (complex), within print rounding
chk = max(np.abs((fk[int(h)] + df[int(h)]) - tot[int(h)]).max() for h in headings)
print(f'cross-check max |FK+DIF - TOTAL| over all pts = {chk:.3e} (print-rounding scale)')

# Total excitation per LIS: use the combined table directly
F_lis = np.stack([tot[int(h)] for h in headings])  # (25,47,6)
np.save('/tmp/F_lis.npy', F_lis)

# ---- Control: long-wave (freq idx 0, w=0.02) - all variants coincide there.
# Check LIS reconstruction convention exp(+i*phase) against npz naive.
iw = 0
for ih, h in enumerate(headings):
    if h in (-180, 0, 90, 180):
        lis = F_lis[ih, iw]
        ref = variants['naive'][ih, iw]
        rel = np.abs(lis - ref) / np.maximum(np.abs(ref), 1.0)
        print(f'control w=0.02 h={h:>5}: |Fz| LIS={abs(lis[2]):.4e} npz={abs(ref[2]):.4e} '
              f'max rel cplx err over DOF={rel.max():.4f}')

# ---- Full-spectrum comparison with 5% peak mask (same masking as the note)
print()
results = {}
for name, F in variants.items():
    errs, aerrs, perrs = [], [], []
    for ih in range(25):
        for idof in range(6):
            peak = np.abs(F_lis[ih, :, idof]).max()
            mask = np.abs(F_lis[ih, :, idof]) > 0.05 * peak
            a = F_lis[ih, mask, idof]
            b = F[ih, mask, idof]
            errs.append(np.abs(b - a) / np.abs(a))
            aerrs.append(np.abs(np.abs(b) - np.abs(a)) / np.abs(a))
            perrs.append(np.degrees(np.angle(b * np.conj(a))))
    e = np.concatenate(errs); a_ = np.concatenate(aerrs); p = np.concatenate(perrs)
    results[name] = (e, a_, p)
    print(f'{name:>6}: masked pts={e.size}  cplx rel err  med={np.median(e)*100:8.3f}%  rms={np.sqrt((e**2).mean())*100:9.3f}%  max={e.max()*100:10.2f}%'
          f' | amp rel err med={np.median(a_)*100:7.3f}% max={a_.max()*100:9.2f}%'
          f' | phase err med={np.median(np.abs(p)):7.3f}deg p95={np.percentile(np.abs(p),95):8.3f}deg max={np.abs(p).max():8.2f}deg')

# ---- Decisive spot check: worst point from the note, w=1.15 (idx 27), h=180, My (dof 4)
ih = list(headings).index(180); iw = list(freqs).index(1.15); idof = 4
print()
print(f'spot w=1.15 h=180 My: LIS total = {F_lis[ih,iw,idof]:.4e}  |.|={abs(F_lis[ih,iw,idof]):.4e}')
for name, F in variants.items():
    v = F[ih, iw, idof]
    print(f'  {name:>6}: {v:.4e}  |.|={abs(v):.4e}  ratio to LIS={abs(v)/abs(F_lis[ih,iw,idof]):.3f}')

# second spot: w=1.05, h=180, My
iw2 = list(freqs).index(1.05)
print(f'spot w=1.05 h=180 My: LIS total |.|={abs(F_lis[ih,iw2,idof]):.4e}')
for name, F in variants.items():
    v = F[ih, iw2, idof]
    print(f'  {name:>6}: |.|={abs(v):.4e}  ratio to LIS={abs(v)/abs(F_lis[ih,iw2,idof]):.3f}')
