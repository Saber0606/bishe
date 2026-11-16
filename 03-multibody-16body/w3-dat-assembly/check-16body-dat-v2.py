# Independent checker for futi_16body.dat v2 (split version). Re-parses the
# WRITTEN file from scratch and verifies it against the W1/W2 v2 design JSONs
# and the builder manifest. Nothing is taken from the builder's internals.
import re, math, json, hashlib
from collections import defaultdict

DAT = '/home/hatch/workspace/graduation-design/stage3-correction-16body/futi_16body.dat'
GEO = json.load(open('/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_from_singlebody_geometry_v2.json'))['parts']
ALLO = json.load(open('/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_w2_allocation_results_v2.json'))['bodies']
MAN = json.load(open('/home/hatch/workspace/graduation-design/stage3-correction-16body/assemble_16body_dat_v2_manifest.json'))

raw = open(DAT, 'rb').read()
md5 = hashlib.md5(raw).hexdigest()
L = raw.decode(errors='ignore').splitlines()
checks = []
def ck(name, ok, detail=''):
    checks.append((name, bool(ok), detail))

ck('md5 matches manifest', md5 == MAN['dat_md5'], md5)
ck('OPTIONS has AHD1, no LHFR', any('OPTIONS REST GOON AHD1 END' in ln for ln in L))

node_re = re.compile(r'^\s*01\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
nodes = {}
bad_node_len = 0
for ln in L:
    m = node_re.match(ln)
    if m:
        nodes[int(m.group(1))] = tuple(float(m.group(i)) for i in (2, 3, 4))
        if len(ln) != 50: bad_node_len += 1
ck('all node lines 50 chars', bad_node_len == 0, f'{bad_node_len} bad')
ck('node count = originals + split + PMAS + duplicates',
   len(nodes) == 6982 + MAN['split_nodes'] + 16 + MAN['duplicates'], f'{len(nodes)}')

hdr_re = re.compile(r'^\s*02\s+ELM?(\d+)\s*$')
el_re = re.compile(r'^\s*02(QPPL|TPPL|PMAS)\s*(DIFF)?\s*(.*?)\s*(\d+)\s*$')
blocks = {}; order = []; cur = None; hydi = []
bad_el_len = 0
for ln in L:
    em = hdr_re.match(ln)
    if em:
        cur = int(em.group(1)); blocks[cur] = []; order.append(cur); continue
    if 'HYDI' in ln and cur: hydi.append(cur)
    m = el_re.match(ln)
    if m and cur:
        if len(ln) != 81: bad_el_len += 1
        ids = [int(g) for g in re.findall(r'\(\s*(\d+)\)', m.group(3))]
        blocks[cur].append((m.group(1), bool(m.group(2)), ids, int(m.group(4))))
ck('16 ELM blocks in order 1..16 (ELM#/EL##)', order == list(range(1, 17)), str(order))
ck('HYDI exactly once, in EL16', hydi == [16], str(hydi))
ck('all element lines 81 chars', bad_el_len == 0, f'{bad_el_len} bad')
elem_nos = [e[3] for b in blocks.values() for e in b]
ck('element numbers unique', len(elem_nos) == len(set(elem_nos)), f'{len(elem_nos)} elements')
ck('total panels == manifest', sum(len([e for e in v if e[0] != "PMAS"]) for v in blocks.values()) == MAN['total_panels'])
ck('one PMAS element per block', all(len([e for e in v if e[0] == 'PMAS']) == 1 for v in blocks.values()))

BODY_NO = {'CEN': 1}
for ci, c in enumerate(['180', '60', '300']):
    for i in range(1, 5): BODY_NO[f'{c}_S{i}'] = 2 + ci * 5 + (i - 1)
    BODY_NO[f'{c}_COL'] = 6 + ci * 5
NAME_OF = {v: k for k, v in BODY_NO.items()}

cnt_ok = True; dif_ok = True
for k in range(1, 17):
    ps = [e for e in blocks[k] if e[0] != 'PMAS']
    if len(ps) != MAN['counts'][NAME_OF[k]]['panels']: cnt_ok = False
    if len([e for e in ps if e[1]]) != MAN['counts'][NAME_OF[k]]['diff']: dif_ok = False
ck('per-body panel counts == manifest', cnt_ok)
ck('per-body DIFF counts == manifest', dif_ok)

# node usage / duplicates consistency
used = defaultdict(set)
for k, v in blocks.items():
    for typ, diff, ids, no in v:
        if typ != 'PMAS':
            for nid in ids[1:]: used[nid].add(k)
coord_groups = defaultdict(set)
for nid, p in nodes.items(): coord_groups[p].add(nid)
multi = 0
for p, idset in coord_groups.items():
    bodies_at = set()
    for nid in idset: bodies_at |= used.get(nid, set())
    if len(idset) > 1: multi += 1
ck('every panel node exists in Deck 01', all(nid in nodes for v in blocks.values() for e in v if e[0] != 'PMAS' for nid in e[2][1:]))

# split nodes: ids 6983..6982+split_nodes lie on I-1/I-3 planes, each shared by exactly 2 bodies
CHAINS = {'180': (-1.0, 0.0), '60': (0.5, math.sqrt(3)/2), '300': (0.5, -math.sqrt(3)/2)}
PLANES = [16.91075, 35.91425]
split_ids = [n for n in nodes if 6983 <= n <= 6982 + MAN['split_nodes']]
on_plane = 0; shared2 = 0
pos_bodies = defaultdict(set)
for nid, p in nodes.items():
    for k in used.get(nid, set()): pos_bodies[p].add(k)
for nid in split_ids:
    p = nodes[nid]
    best = None
    for cn, (ux, uy) in CHAINS.items():
        s = p[0]*ux + p[1]*uy
        for P in PLANES:
            if best is None or abs(s - P) < best[0]: best = (abs(s - P), cn, P)
    if best[0] <= 0.002: on_plane += 1
    if len(pos_bodies[p]) == 2: shared2 += 1
ck('all split nodes lie on I-1/I-3 planes (<=2 mm)', on_plane == len(split_ids), f'{on_plane}/{len(split_ids)}')
ck('every split-node position shared by exactly 2 bodies', shared2 == len(split_ids), f'{shared2}/{len(split_ids)}')

# no piece straddles I-1/I-3
straddle = 0
for k, v in blocks.items():
    for typ, diff, ids, no in v:
        if typ == 'PMAS': continue
        pts = [nodes[n] for n in ids[1:]]
        cen = tuple(sum(p[i] for p in pts)/len(pts) for i in range(3))
        bc = max(CHAINS, key=lambda cn: cen[0]*CHAINS[cn][0] + cen[1]*CHAINS[cn][1])
        ux, uy = CHAINS[bc]
        sv = [p[0]*ux + p[1]*uy for p in pts]
        for P in PLANES:
            if min(sv) < P - 0.002 and max(sv) > P + 0.002: straddle += 1
ck('no panel piece straddles I-1/I-3', straddle == 0, f'{straddle} straddlers')

# geometry integrals per body
def panel_int(ids):
    pts = [nodes[i] for i in ids]; n = len(pts)
    cx = sum(p[0] for p in pts)/n; cy = sum(p[1] for p in pts)/n; cz = sum(p[2] for p in pts)/n
    nx = ny = nz = 0.0
    for i in range(n):
        x1, y1, z1 = pts[i]; x2, y2, z2 = pts[(i+1) % n]
        nx += (y1-y2)*(z1+z2); ny += (z1-z2)*(x1+x2); nz += (x1-x2)*(y1+y2)
    nn = math.sqrt(nx*nx+ny*ny+nz*nz)
    return (1/3.0)*(cx*nx+cy*ny+cz*nz)*0.5, 0.5*nn
vol = defaultdict(float); area = defaultdict(float)
for k, v in blocks.items():
    for typ, diff, ids, no in v:
        if typ == 'PMAS': continue
        vi, ai = panel_int(ids[1:])
        area[NAME_OF[k]] += ai
        if diff: vol[NAME_OF[k]] += vi
BND = [7.409, 16.91075, 26.4125, 35.91425, 45.416]; A = 87.5
def cap(s, sign): return sign*(1/3.0)*s*A
for c in ['180', '60', '300']:
    vol['CEN'] += cap(BND[0], +1)
    for i in range(4):
        vol[f'{c}_S{i+1}'] += cap(BND[i+1], +1) + cap(BND[i], -1)
    vol[f'{c}_COL'] += cap(BND[4], -1)
worst_v = 0.0; worst_seg = 0.0; worst_a = 0.0
print('\nper-body volume/area vs W1 v2 exact:')
for k in range(1, 17):
    nm = NAME_OF[k]; g = GEO[nm]
    dv = (vol[nm]-g['volume_m3'])/g['volume_m3']*100
    da = (area[nm]-g['area_m2'])/g['area_m2']*100
    worst_v = max(worst_v, abs(dv)); worst_a = max(worst_a, abs(da))
    if '_S' in nm: worst_seg = max(worst_seg, abs(dv))
    print(f'  {nm:8s} vol {vol[nm]:9.2f} vs {g["volume_m3"]:9.2f} ({dv:+.2f}%)   area {area[nm]:8.1f} vs {g["area_m2"]:8.1f} ({da:+.2f}%)')
ck('total displaced volume conserved (20157.84)', abs(sum(vol.values()) - 20157.84) < 0.05, f'{sum(vol.values()):.2f}')
ck('worst segment volume deviation <= 0.75% (ring-residue level; was 8.3% in v1)', worst_seg <= 0.75, f'{worst_seg:.2f}%')
ck('worst body volume deviation <= 0.75%', worst_v <= 0.75, f'{worst_v:.2f}%')
ck('total surface area conserved (10272.61)', abs(sum(area.values()) - 10272.61) < 0.05, f'{sum(area.values()):.2f}')

# Deck 03 / 04 vs W2 v2 (fixed-column parse)
d3 = {}
for ln in L:
    m = re.match(r'^\s*03(.{24})\s*$', ln)
    if m and 'MATE' not in ln:
        f = m.group(1).strip()
        # fixed-column format: str(body) + sci-notation (always 10 chars: d.ddddE+dd)
        cands = [k for k in range(1, 17) if len(f) == len(str(k)) + 10 and f.startswith(str(k))]
        assert len(cands) == 1, f
        d3[cands[0]] = float(f[len(str(cands[0])):])
ck('Deck 03 has 16 masses', len(d3) == 16, f'{len(d3)}')
mdev = max(abs(d3[k]/1000.0 - ALLO[NAME_OF[k]]['mass_t'])/ALLO[NAME_OF[k]]['mass_t'] for k in range(1, 17))
ck('Deck 03 masses == W2 v2 (print precision)', mdev < 1e-4, f'max rel dev {mdev:.2e}')
ck('Deck 03 printed total within %.4E print-rounding bound (0.85 t)', abs(sum(d3.values())/1000.0 - 17854.0) < 0.85, f'{sum(d3.values())/1000.0:.2f} t (print rounding of 16 values, quantum 0.1 t each)')
d4 = {}
for ln in L:
    if ln.startswith('    04PMAS'):
        g = int(ln[10:20]); vals = [float(ln[20+i*10:30+i*10]) for i in range(6)]
        d4[g] = vals
ck('Deck 04 has 16 tensors', len(d4) == 16)
idev = 0.0
for k in range(1, 17):
    Ixx, Iyy, Izz, Ixy, Ixz, Iyz = ALLO[NAME_OF[k]]['inertia']
    want = [Ixx, Ixy, Ixz, Iyy, Iyz, Izz]
    for a, b in zip(d4[k], want):
        if abs(b) > 1: idev = max(idev, abs(a-b)/abs(b))
ck('Deck 04 tensors == W2 v2 (print precision)', idev < 5e-4, f'max rel dev {idev:.2e}')
# three-account synthesis from printed decks
M = sum(d3.values())/1000.0
G = [0.0]*3; It = [0.0]*6
for k in range(1, 17):
    b = ALLO[NAME_OF[k]]; cog = b['cog']; m = d3[k]/1000.0
    # use printed tensor (about own cog) + printed mass + design cog (PMAS node printed at 3dp)
    pn = nodes[99983 + k]
    Ixx, Ixy, Ixz, Iyy, Iyz, Izz = d4[k]
    for i in range(3): G[i] += m*pn[i]
G = [g/M for g in G]
for k in range(1, 17):
    m = d3[k]/1000.0; pn = nodes[99983 + k]
    Ixx, Ixy, Ixz, Iyy, Iyz, Izz = d4[k]
    d = [pn[i]-G[i] for i in range(3)]
    It[0] += Ixx + m*1000*(d[1]**2+d[2]**2); It[1] += Iyy + m*1000*(d[0]**2+d[2]**2)
    It[2] += Izz + m*1000*(d[0]**2+d[1]**2)
ck('synthesis CoG z = -14.940 +/- 0.002', abs(G[2] + 14.940) < 0.002, f'{G[2]:.4f}')
ck('synthesis Izz dev < 0.01%', abs(It[2]/2.367e10 - 1) < 1e-4, f'{(It[2]/2.367e10-1)*100:+.4f}%')
ck('synthesis Ixx/Iyy dev within +0.5..+0.9% (design check values)', 0.4 < (It[0]/1.251e10-1)*100 < 0.9 and 0.4 < (It[1]/1.251e10-1)*100 < 0.9,
   f'Ixx {(It[0]/1.251e10-1)*100:+.2f}%, Iyy {(It[1]/1.251e10-1)*100:+.2f}%')
# PMAS nodes at design CoGs (3dp print)
pdev = 0.0
for k in range(1, 17):
    pn = nodes[99983 + k]; cg = ALLO[NAME_OF[k]]['cog']
    pdev = max(pdev, max(abs(pn[i]-cg[i]) for i in range(3)))
ck('PMAS nodes at W2 v2 CoGs (<=1 mm print rounding)', pdev <= 0.001, f'{pdev*1000:.2f} mm')

print()
fails = 0
for name, ok, detail in checks:
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail else ''))
    fails += (not ok)
print(f'\n{len(checks)-fails}/{len(checks)} checks passed')
