# 16-body W1 geometry v2: same derivation as v1 (ONLY the original single-body dat
# futi_lowfreq.dat + NREL Table 2), but per-body surface AREA and area centroid are now
# EXACT-CLIP values (pontoon panels clipped at the cut planes, piece areas summed per
# body) instead of v1's whole-panel centroid-rule bookkeeping. Volumes/CoB unchanged
# from v1 (already exact-clip). v1 centroid-rule areas are kept in the output as
# area_m2_v1_centroid_rule so the revision magnitude is on record.
import re, math, json
from collections import defaultdict

DAT = '/home/hatch/workspace/user/files/futi_lowfreq.dat'
lines = open(DAT, errors='ignore').read().splitlines()
nodes = {}
node_re = re.compile(r'^\s*01\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
for ln in lines:
    m = node_re.match(ln)
    if m: nodes[int(m.group(1))] = tuple(float(m.group(i)) for i in (2,3,4))
el_re = re.compile(r'^\s*02(QPPL|TPPL|PMAS)\s*(DIFF)?\s*(.*)$')
panels = []
for ln in lines:
    m = el_re.match(ln)
    if m and m.group(1) in ('QPPL', 'TPPL'):
        panels.append((bool(m.group(2)), [int(g) for g in re.findall(r'\(\s*(\d+)\)', m.group(3))]))
assert len(panels) == 6943 and sum(1 for d, _ in panels if d) == 5454

CHAINS = {'180': (-1.0, 0.0), '60': (0.5, math.sqrt(3)/2), '300': (0.5, -math.sqrt(3)/2)}
BND = [7.409, 16.91075, 26.4125, 35.91425, 45.416]
A_CROSS = 87.5

def panel_geom(groups):
    pts = [nodes[i] for i in groups[1:]]
    n = len(pts)
    c = tuple(sum(p[k] for p in pts)/n for k in range(3))
    nx = ny = nz = 0.0
    for i in range(n):
        x1, y1, z1 = pts[i]; x2, y2, z2 = pts[(i+1) % n]
        nx += (y1-y2)*(z1+z2); ny += (z1-z2)*(x1+x2); nz += (x1-x2)*(y1+y2)
    nn = math.sqrt(nx*nx+ny*ny+nz*nz)
    return pts, c, 0.5*nn, (nx/nn, ny/nn, nz/nn)

def tri_integrals(p1, p2, p3, nrm):
    ax, ay, az = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
    bx, by, bz = p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]
    A = 0.5*math.sqrt((ay*bz-az*by)**2 + (az*bx-ax*bz)**2 + (ax*by-ay*bx)**2)
    if A == 0: return 0.0, (0.0, 0.0, 0.0)
    cx, cy, cz = (p1[0]+p2[0]+p3[0])/3, (p1[1]+p2[1]+p3[1])/3, (p1[2]+p2[2]+p3[2])/3
    vol = (1/3.0)*(cx*nrm[0]+cy*nrm[1]+cz*nrm[2])*A
    mom = []
    for k in range(3):
        s1 = p1[k]+p2[k]+p3[k]; s2 = p1[k]**2+p2[k]**2+p3[k]**2
        mom.append(0.5*nrm[k]*A*(s1*s1 + s2)/12.0)
    return vol, tuple(mom)

def poly_integrals(pts, nrm):
    vol = 0.0; mom = [0.0, 0.0, 0.0]
    for i in range(1, len(pts)-1):
        v, m = tri_integrals(pts[0], pts[i], pts[i+1], nrm)
        vol += v
        for k in range(3): mom[k] += m[k]
    return vol, mom

def poly_area_centroid(pts):
    # exact area + centroid of a planar polygon via fan triangulation
    A = 0.0; C = [0.0, 0.0, 0.0]
    for i in range(1, len(pts)-1):
        p1, p2, p3 = pts[0], pts[i], pts[i+1]
        ux, uy, uz = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
        vx, vy, vz = p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]
        cx, cy, cz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        a = 0.5*math.sqrt(cx*cx+cy*cy+cz*cz)
        A += a
        for k in range(3): C[k] += a*(p1[k]+p2[k]+p3[k])/3.0
    if A == 0: return 0.0, None
    return A, tuple(C[k]/A for k in range(3))

def clip_s(poly_stz, lo, hi):
    def clip_one(poly, bound, keep_le):
        if not poly: return poly
        out = []
        for i in range(len(poly)):
            cur = poly[i]; prv = poly[i-1]
            cin = cur[0] <= bound if keep_le else cur[0] >= bound
            pin = prv[0] <= bound if keep_le else prv[0] >= bound
            if cin != pin:
                f = (bound - prv[0])/(cur[0] - prv[0])
                out.append((bound, prv[1] + f*(cur[1]-prv[1]), prv[2] + f*(cur[2]-prv[2])))
            if cin: out.append(cur)
        return out
    return clip_one(clip_one(poly_stz, lo, False), hi, True)

bodies = ['CEN'] + [f'{c}_S{i}' for c in CHAINS for i in range(1, 5)] + [f'{c}_COL' for c in CHAINS]
cnt = defaultdict(int); dif = defaultdict(int)
area1 = defaultdict(float); area1_c = defaultdict(lambda: [0.0, 0.0, 0.0])   # v1 centroid rule
area2 = defaultdict(float); area2_c = defaultdict(lambda: [0.0, 0.0, 0.0])   # v2 exact clip
vol = defaultdict(float); mom = defaultdict(lambda: [0.0, 0.0, 0.0])
seg_of_slab = {}
for c in CHAINS:
    seg_of_slab[(c, 0)] = 'CEN'; seg_of_slab[(c, 5)] = f'{c}_COL'
    for i in range(4): seg_of_slab[(c, i+1)] = f'{c}_S{i+1}'

unclassified = 0
total_panel_area = 0.0
for diff, groups in panels:
    pts, c, a, nrm = panel_geom(groups)
    total_panel_area += a
    x, y, z = c; rho = math.hypot(x, y)
    best = None
    for name, (ux, uy) in CHAINS.items():
        s = x*ux + y*uy; t = -x*uy + y*ux
        if best is None or s > best[1]: best = (name, s, t)
    name, s, t = best; ux, uy = CHAINS[name]
    d_out = math.hypot(x - 51.75*ux, y - 51.75*uy)
    in_band = -20.01 <= z <= -12.99
    is_pontoon = in_band and abs(t) <= 6.55 and 4.0 <= s <= 52.0 and rho > 5.35 and d_out > 6.35
    if is_pontoon:
        poly = []
        for (px, py, pz) in pts:
            poly.append((px*ux + py*uy, -px*uy + py*ux, pz))
        edges = [-1e9] + BND + [1e9]
        for slab in range(6):
            piece = clip_s(poly, edges[slab], edges[slab+1])
            if len(piece) < 3: continue
            body = seg_of_slab[(name, slab)]
            gpts = [(ss*ux - tt*uy, ss*uy + tt*ux, zz) for (ss, tt, zz) in piece]
            pa, pc = poly_area_centroid(gpts)
            area2[body] += pa
            if pc is not None:
                for k in range(3): area2_c[body][k] += pa*pc[k]
            if diff:
                v, m = poly_integrals(gpts, nrm)
                vol[body] += v
                for k in range(3): mom[body][k] += m[k]
        body_c = seg_of_slab[(name, 0 if s <= BND[0] else 5 if s > BND[4] else 1 + sum(1 for b in BND[1:4] if s > b))]
        cnt[body_c] += 1; area1[body_c] += a
        if diff: dif[body_c] += 1
        for k in range(3): area1_c[body_c][k] += a*c[k]
    elif d_out <= 6.55:
        body = f'{name}_COL'
        cnt[body] += 1; area1[body] += a; area2[body] += a
        for k in range(3):
            area1_c[body][k] += a*c[k]; area2_c[body][k] += a*c[k]
        if diff:
            dif[body] += 1
            v, m = poly_integrals(pts, nrm); vol[body] += v
            for k in range(3): mom[body][k] += m[k]
    elif rho <= 7.45:
        body = 'CEN'
        cnt[body] += 1; area1[body] += a; area2[body] += a
        for k in range(3):
            area1_c[body][k] += a*c[k]; area2_c[body][k] += a*c[k]
        if diff:
            dif[body] += 1
            v, m = poly_integrals(pts, nrm); vol[body] += v
            for k in range(3): mom[body][k] += m[k]
    else:
        unclassified += 1

print(f"unclassified: {unclassified}; panels counted: {sum(cnt.values())}; DIFF counted: {sum(dif.values())}")
print(f"total panel area {total_panel_area:.2f}; sum exact areas {sum(area2.values()):.2f}; sum v1 areas {sum(area1.values()):.2f}")

def cap_vol(chain, s, sign):
    return sign*(1/3.0)*s*A_CROSS
def cap_mom(chain, s, sign):
    ux, uy = CHAINS[chain]; W2 = 12.5**2/12.0
    ix = A_CROSS*((s*ux)**2 + W2*uy*uy); iy = A_CROSS*((s*uy)**2 + W2*ux*ux)
    return (sign*0.5*ux*ix, sign*0.5*uy*iy, 0.0)
for cname in CHAINS:
    vol['CEN'] += cap_vol(cname, BND[0], +1)
    cm = cap_mom(cname, BND[0], +1)
    for k in range(3): mom['CEN'][k] += cm[k]
    for i in range(4):
        b = f'{cname}_S{i+1}'
        vol[b] += cap_vol(cname, BND[i+1], +1) + cap_vol(cname, BND[i], -1)
        cm1 = cap_mom(cname, BND[i], -1); cm2 = cap_mom(cname, BND[i+1], +1)
        for k in range(3): mom[b][k] += cm1[k] + cm2[k]
    vol[f'{cname}_COL'] += cap_vol(cname, BND[4], -1)
    cm = cap_mom(cname, BND[4], -1)
    for k in range(3): mom[f'{cname}_COL'][k] += cm[k]

V = {b: vol[b] for b in bodies}
CoB = {b: tuple(mom[b][k]/V[b] for k in range(3)) for b in bodies}
print("\nbody | area v1 | area v2 exact | d% | volume | CoB")
for b in bodies:
    d = (area2[b]-area1[b])/area1[b]*100
    print(f"{b:8s} {area1[b]:9.1f} {area2[b]:9.1f} {d:+6.2f}  {V[b]:10.2f}  ({CoB[b][0]:8.3f},{CoB[b][1]:8.3f},{CoB[b][2]:8.3f})")
Vt = sum(V.values())
tc = tuple(sum(V[b]*CoB[b][k] for b in bodies)/Vt for k in range(3))
print(f"TOTAL V = {Vt:.2f}; total CoB = ({tc[0]:.4f},{tc[1]:.4f},{tc[2]:.4f})")

out = {'source': 'futi_lowfreq.dat only (Deck 01/02) + NREL Table 2 for W2',
       'revision': 'v2: area_m2 and area_centroid are exact-clip values; v1 centroid-rule areas kept as area_m2_v1_centroid_rule',
       'diff_total': int(sum(dif.values())), 'volume_total': Vt, 'total_cob': list(tc),
       'area_total': sum(area2.values()),
       'parts': {b: {'panels': int(cnt[b]), 'diff': int(dif[b]),
                     'area_m2': area2[b],
                     'area_centroid': [area2_c[b][k]/area2[b] for k in range(3)],
                     'area_m2_v1_centroid_rule': area1[b],
                     'volume_m3': V[b], 'cob': list(CoB[b])} for b in bodies}}
with open('/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_from_singlebody_geometry_v2.json', 'w') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("saved geometry v2 json")
