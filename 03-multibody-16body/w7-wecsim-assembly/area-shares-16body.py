# W7 Option A prep (16-body): per-body projected-area shares and translational
# quadratic-damping split of NREL Table 5, by the SAME method as the 19-body
# pending record (bishe-sync 03-multibody-19body/w7-wecsim-assembly/
# w7-damping-split-options-pending.md S3.1-3.3):
#   box segment faces (3 orientations): radial cap W*H, tangential side L*H,
#   vertical L*W; projected area along d = sum |n.d| * A_face.
#   column (cylinder D=12.5, draft 20): horizontal 250 m2 (azimuth-free),
#   vertical pi*6.25^2.
# Shares are formed per direction over the SUM of per-body projections (the
# record's convention), then Bq_body = share * Table 5 diagonal.
# The script first REPRODUCES the 19-body record numbers (L=7.6014, 5 segs)
# as a method validation, then computes the 16-body case (L=9.50175, 4 segs).
import numpy as np, json

W, H = 12.5, 7.0
COL_H, COL_V = 250.0, np.pi * 6.25**2
TABLE5 = dict(surge=9.225e5, sway=9.225e5, heave=2.296e6)
CHAINS = [180.0, 60.0, 300.0]  # azimuths of the three pontoon chains

def seg_proj(L, phi_deg):
    phi = np.deg2rad(phi_deg)
    radial = np.array([np.cos(phi), np.sin(phi), 0.0])
    tang = np.array([-np.sin(phi), np.cos(phi), 0.0])
    vert = np.array([0.0, 0.0, 1.0])
    faces = [(radial, W * H), (tang, L * H), (vert, L * W)]
    out = {}
    for dname, d in [('surge', np.array([1., 0, 0])), ('sway', np.array([0., 1, 0])),
                     ('heave', np.array([0., 0, 1.]))]:
        out[dname] = sum(abs(n @ d) * A for n, A in faces)
    return out

def compute(L, nseg):
    bodies = []  # (label, proj dict)
    bodies.append(('CEN column', dict(surge=COL_H, sway=COL_H, heave=COL_V)))
    for phi in CHAINS:
        p = seg_proj(L, phi)
        for s in range(nseg):
            bodies.append((f'{int(phi)}deg seg{s+1}', p))
        bodies.append((f'{int(phi)}deg column', dict(surge=COL_H, sway=COL_H, heave=COL_V)))
    totals = {d: sum(b[1][d] for b in bodies) for d in TABLE5}
    pon = {d: sum(b[1][d] for b in bodies if 'seg' in b[0]) for d in TABLE5}
    col = {d: sum(b[1][d] for b in bodies if 'column' in b[0]) for d in TABLE5}
    rows = []
    for lab, p in bodies:
        rows.append(dict(body=lab, **{f'Bq_{d}': p[d] / totals[d] * TABLE5[d] for d in TABLE5},
                         **{f'area_{d}': p[d] for d in TABLE5}))
    sums = {d: sum(r[f'Bq_{d}'] for r in rows) for d in TABLE5}
    return bodies, totals, pon, col, rows, sums

# ---- validation against the 19-body record ----
b19, t19, p19, c19, r19, s19 = compute(7.6014, 5)
print("19-body validation vs record S3.2/S3.3:")
print(f"  pontoon totals surge/sway/heave = {p19['surge']:.2f}/{p19['sway']:.2f}/{p19['heave']:.2f}"
      f"  (record 1335.81/1289.87/1425.26)")
print(f"  grand totals = {t19['surge']:.2f}/{t19['sway']:.2f}/{t19['heave']:.2f}"
      f"  (record 2335.81/2289.87/1916.13)")
colrow = [r for r in r19 if r['body'] == 'CEN column'][0]
seg180 = [r for r in r19 if r['body'] == '180deg seg1'][0]
seg60 = [r for r in r19 if r['body'] == '60deg seg1'][0]
print(f"  column Bq = {colrow['Bq_surge']:.4e}/{colrow['Bq_sway']:.4e}/{colrow['Bq_heave']:.4e}"
      f"  (record 9.873e4/1.007e5/1.47e5)")
print(f"  180 seg Bq = {seg180['Bq_surge']:.4e}/{seg180['Bq_sway']:.4e}/{seg180['Bq_heave']:.4e}"
      f"  (record 3.456e4/2.144e4/1.139e5)")
print(f"  60 seg Bq  = {seg60['Bq_surge']:.4e}/{seg60['Bq_sway']:.4e}  (record 3.548e4/4.125e4)")
print(f"  Bq sums    = {s19['surge']:.6e}/{s19['sway']:.6e}/{s19['heave']:.6e} (Table 5 exact)")

# ---- 16-body case ----
b16, t16, p16, c16, r16, s16 = compute(9.50175, 4)
print("\n16-body (L=9.50175, 4 segs/chain, 12 segs + 4 columns):")
print(f"  pontoon totals = {p16['surge']:.2f}/{p16['sway']:.2f}/{p16['heave']:.2f}")
print(f"  column totals  = {c16['surge']:.2f}/{c16['sway']:.2f}/{c16['heave']:.2f}")
print(f"  grand totals   = {t16['surge']:.2f}/{t16['sway']:.2f}/{t16['heave']:.2f}")
print(f"  pontoon shares = {p16['surge']/t16['surge']*100:.2f}%/{p16['sway']/t16['sway']*100:.2f}%/"
      f"{p16['heave']/t16['heave']*100:.2f}%  (19-body: 57.19/56.33/74.38)")
print(f"  Bq sums        = {s16['surge']:.6e}/{s16['sway']:.6e}/{s16['heave']:.6e} (Table 5 exact)")
NAMES16 = ['1 CEN', '2 180 S1', '3 180 S2', '4 180 S3', '5 180 S4', '6 180 COL',
           '7 60 S1', '8 60 S2', '9 60 S3', '10 60 S4', '11 60 COL',
           '12 300 S1', '13 300 S2', '14 300 S3', '15 300 S4', '16 300 COL']
out = dict(method='per-body projected area, per-direction normalisation (19-body record S3 method)',
           segment_length_m=9.50175, totals=t16, pontoon_totals=p16, column_totals=c16,
           pontoon_shares={d: p16[d] / t16[d] for d in TABLE5},
           Bq_sums=s16, table5_diag=TABLE5,
           bodies=[dict(body=NAMES16[i], Bq_surge=r['Bq_surge'], Bq_sway=r['Bq_sway'],
                        Bq_heave=r['Bq_heave'], area_surge=r['area_surge'],
                        area_sway=r['area_sway'], area_heave=r['area_heave'])
                   for i, r in enumerate(r16)])
for b in out['bodies']:
    print(f"  {b['body']:9s} Bq surge/sway/heave = {b['Bq_surge']:.4e} / {b['Bq_sway']:.4e} / {b['Bq_heave']:.4e}")
json.dump(out, open('/home/hatch/workspace/graduation-design/stage3-correction-16body/w7-prep/area-shares-16body.json', 'w'), indent=1)
print("saved area-shares-16body.json")
