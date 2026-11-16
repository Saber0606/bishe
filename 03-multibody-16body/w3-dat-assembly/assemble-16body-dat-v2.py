# W3 v2 (16-body correction): assemble futi_16body.dat by cutting the ORIGINAL
# single-body dat (futi_lowfreq.dat, Stage 1A) into 16 structures, WITH panel
# splitting at the I-1 / I-3 cut planes (r = 16.91075 / 35.91425, the two planes
# that fall mid-bay between mesh rings; I-0 / I-2 / I-4 already lie on mesh
# rings and are NOT split). Differences vs v1 (whole-panel):
#   - panels straddling I-1/I-3 are subdivided exactly at the plane; new nodes
#     are inserted at edge-plane intersections (shared per mesh edge);
#   - ELM block headers mirror the as-run 19-body file: ELM1..ELM9, EL10..EL16;
#   - masses/CoGs/inertias from the W2 v2 design table (exact-clip areas).
# Surface geometry is unchanged: split pieces tile their original panels.
# Anchors: single-body dat + W1/W2 v2 (geometry/allocation JSONs). No 19-body
# VALUES are used; only its file-format precedent (EL headers, HYDI placement).
import re, math, json, hashlib
from collections import Counter, defaultdict

SRC = '/home/hatch/workspace/user/files/futi_lowfreq.dat'
GEO = '/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_from_singlebody_geometry_v2.json'
ALLO = '/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_w2_allocation_results_v2.json'
OUT = '/home/hatch/workspace/graduation-design/stage3-correction-16body/futi_16body.dat'
MANIFEST = '/home/hatch/workspace/graduation-design/stage3-correction-16body/assemble_16body_dat_v2_manifest.json'

lines = open(SRC, errors='ignore').read().splitlines()

# ---------- parse Deck 01 ----------
node_re = re.compile(r'^\s*01\s*(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
nodes, node_line = {}, {}
for ln in lines:
    m = node_re.match(ln)
    if m:
        nid = int(m.group(1))
        nodes[nid] = tuple(float(m.group(i)) for i in (2, 3, 4))
        node_line[nid] = ln
assert len(nodes) == 6983 and 99999 in nodes
assert max(n for n in nodes if n != 99999) == 6982

# ---------- parse Deck 02 panels ----------
el_re = re.compile(r'^\s*02(QPPL|TPPL)\s*(DIFF)?\s*(.*?)\s*(\d+)\s*$')
panels = []  # (elem_no, type, diff, [node ids])
for ln in lines:
    m = el_re.match(ln)
    if m:
        ids = [int(g) for g in re.findall(r'\(\s*(\d+)\)', m.group(3))]
        panels.append((int(m.group(4)), m.group(1), bool(m.group(2)), ids[1:]))
assert len(panels) == 6943 and sorted(p[0] for p in panels) == list(range(1, 6944))
assert sum(1 for p in panels if p[2]) == 5454
zlwl_line = next(ln for ln in lines if 'ZLWL' in ln)

# ---------- verbatim tail (Deck 05..EOF) ----------
i05 = next(i for i, ln in enumerate(lines) if ln.startswith('    05'))
tail = lines[i05:]
header = lines[:10]
assert header[9].strip() == '*'
header = [ln.replace('OPTIONS REST GOON END', 'OPTIONS REST GOON AHD1 END') for ln in header]

CHAINS = {'180': (-1.0, 0.0), '60': (0.5, math.sqrt(3) / 2), '300': (0.5, -math.sqrt(3) / 2)}
BND = [7.409, 16.91075, 26.4125, 35.91425, 45.416]
SPLIT_PLANES = [16.91075, 35.91425]   # I-1, I-3

def node_text(nid, x, y, z):
    return '    01' + f'{nid:5d}' + ' ' * 9 + f'{x:10.3f}{y:10.3f}{z:10.3f}'

def panel_area(ids):
    pts = [nodes[i] for i in ids]
    n = len(pts); A = 0.0
    for i in range(1, n - 1):
        ux, uy, uz = (pts[i][k] - pts[0][k] for k in range(3))
        vx, vy, vz = (pts[i + 1][k] - pts[0][k] for k in range(3))
        A += 0.5 * math.sqrt((uy * vz - uz * vy) ** 2 + (uz * vx - ux * vz) ** 2 + (ux * vy - uy * vx) ** 2)
    return A

def chain_frame(chain, p):
    ux, uy = CHAINS[chain]
    return (p[0] * ux + p[1] * uy, -p[0] * uy + p[1] * ux, p[2])

def best_chain(centroid):
    x, y, z = centroid
    best = None
    for name in CHAINS:
        s, t, _ = chain_frame(name, (x, y, z))
        if best is None or s > best[1]:
            best = (name, s, t)
    return best

# ---------- splitting ----------
next_node = 6983
edge_node = {}    # (frozenset({a,b}), chain, plane) -> new node id
split_stats = Counter()
min_piece_area = [1e18]

def get_edge_node(a, b, chain, plane, pa, pb):
    global next_node
    key = (frozenset((a, b)), chain, plane)
    if key in edge_node:
        return edge_node[key]
    sa = chain_frame(chain, pa)[0]; sb = chain_frame(chain, pb)[0]
    f = (plane - sa) / (sb - sa)
    p = tuple(pa[k] + f * (pb[k] - pa[k]) for k in range(3))
    nid = next_node; next_node += 1
    nodes[nid] = p
    node_line[nid] = node_text(nid, *p)
    edge_node[key] = nid
    split_stats['split_nodes'] += 1
    return nid

def clip_side(verts, chain, plane, keep_le):
    # verts: list of node ids (global coords via nodes{}); clip in chain frame by s<=plane or s>=plane
    if not verts: return verts
    sv = [chain_frame(chain, nodes[v])[0] for v in verts]
    out = []
    n = len(verts)
    for i in range(n):
        cur, prv = verts[i], verts[i - 1]
        sc, sp = sv[i], sv[i - 1]
        cin = sc <= plane if keep_le else sc >= plane
        pin = sp <= plane if keep_le else sp >= plane
        if cin != pin:
            out.append(get_edge_node(prv, cur, chain, plane, nodes[prv], nodes[cur]))
        if cin:
            out.append(cur)
    # drop consecutive duplicates (same id)
    ded = []
    for v in out:
        if not ded or ded[-1] != v:
            ded.append(v)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded

def decompose(poly):
    # polygon (3..5 verts, orientation preserved) -> list of node-id lists (tri/quad)
    if len(poly) <= 4:
        return [poly]
    if len(poly) == 5:
        return [poly[0:3], [poly[0], poly[2], poly[3], poly[4]]]
    raise ValueError(f'polygon with {len(poly)} vertices')

def split_panel(ids, chain, plane):
    lo = clip_side(ids, chain, plane, True)
    hi = clip_side(ids, chain, plane, False)
    pieces = []
    for poly in (lo, hi):
        if len(poly) >= 3:
            pieces += decompose(poly)
    return pieces

pieces_all = []   # (diff, [node ids]) in processing order; element numbers assigned below
split_report = []
for elem_no, typ, diff, ids in panels:
    pts = [nodes[i] for i in ids]
    cen = tuple(sum(p[k] for p in pts) / len(pts) for k in range(3))
    chain, s_c, t_c = best_chain(cen)
    target_plane = None
    if -20.01 <= cen[2] <= -12.99 and abs(t_c) <= 7.5:
        sv = [chain_frame(chain, p)[0] for p in pts]
        for P in SPLIT_PLANES:
            if min(sv) < P - 1e-9 and max(sv) > P + 1e-9:
                target_plane = P
                break
    if target_plane is None:
        pieces_all.append((elem_no, diff, ids))
        continue
    a0 = panel_area(ids)
    pieces = split_panel(ids, chain, target_plane)
    a1 = sum(panel_area(pc) for pc in pieces)
    assert abs(a1 - a0) / a0 < 1e-9, (elem_no, a0, a1)
    for pc in pieces:
        min_piece_area[0] = min(min_piece_area[0], panel_area(pc))
    split_stats['split_panels'] += 1
    split_stats[f'plane_{target_plane}'] += 1
    split_report.append((elem_no, target_plane, len(pieces)))
    for j, pc in enumerate(pieces):
        pieces_all.append((elem_no if j == 0 else None, diff, pc))

n_extra = sum(1 for e, _, _ in pieces_all if e is None)
next_extra = 6944
final_panels = []  # (elem_no, type, diff, [ids])
for e, diff, ids in pieces_all:
    if e is None:
        e = next_extra; next_extra += 1
    final_panels.append((e, 'QPPL' if len(ids) == 4 else 'TPPL', diff, ids))
TOTAL_PANELS = len(final_panels)
assert TOTAL_PANELS == 6943 + n_extra
print(f'split panels: {split_stats["split_panels"]} (I-1: {split_stats["plane_16.91075"]}, I-3: {split_stats["plane_35.91425"]}); '
      f'split nodes: {split_stats["split_nodes"]}; extra elements: {n_extra}; total panels: {TOTAL_PANELS}; min piece area: {min_piece_area[0]:.4f} m2')

# ---------- classify pieces to bodies (centroid rule, same as W1) ----------
BODY_NO = {'CEN': 1}
for ci, c in enumerate(['180', '60', '300']):
    for i in range(1, 5):
        BODY_NO[f'{c}_S{i}'] = 2 + ci * 5 + (i - 1)
    BODY_NO[f'{c}_COL'] = 6 + ci * 5
NAME_OF = {v: k for k, v in BODY_NO.items()}

def classify(node_ids):
    pts = [nodes[i] for i in node_ids]
    n = len(pts)
    x = sum(p[0] for p in pts) / n; y = sum(p[1] for p in pts) / n; z = sum(p[2] for p in pts) / n
    rho = math.hypot(x, y)
    name, s, t = best_chain((x, y, z))
    ux, uy = CHAINS[name]
    d_out = math.hypot(x - 51.75 * ux, y - 51.75 * uy)
    in_band = -20.01 <= z <= -12.99
    is_pontoon = in_band and abs(t) <= 6.55 and 4.0 <= s <= 52.0 and rho > 5.35 and d_out > 6.35
    if is_pontoon:
        if s <= BND[0]:
            return 'CEN'
        if s > BND[4]:
            return f'{name}_COL'
        return f'{name}_S{1 + sum(1 for b in BND[1:4] if s > b)}'
    if d_out <= 6.55:
        return f'{name}_COL'
    if rho <= 7.45:
        return 'CEN'
    raise ValueError(f'unclassified piece centroid {(x, y, z)}')

panel_body = {}
for elem_no, typ, diff, ids in final_panels:
    panel_body[elem_no] = BODY_NO[classify(ids)]
cnt = Counter(panel_body.values()); dif = Counter()
for elem_no, typ, diff, ids in final_panels:
    if diff:
        dif[panel_body[elem_no]] += 1
print('piece counts per body:', {NAME_OF[k]: (cnt[k], dif[k]) for k in range(1, 17)})

# ---------- node ownership and duplicates ----------
node_bodies = defaultdict(set)
for elem_no, typ, diff, ids in final_panels:
    for nid in ids:
        node_bodies[nid].add(panel_body[elem_no])
dup_of = {}
next_dup = 20001
for body_no in range(1, 17):
    for nid in sorted(node_bodies):
        users = node_bodies[nid]
        if body_no in users and body_no != min(users):
            dup_of[(body_no, nid)] = next_dup
            next_dup += 1
print(f'interface duplicate nodes: {next_dup - 20001} (20001..{next_dup - 1})')

def node_for(body_no, nid):
    if body_no == min(node_bodies[nid]):
        return nid
    return dup_of[(body_no, nid)]

# ---------- W2 v2 design values ----------
allo = json.load(open(ALLO))['bodies']
def w2(name):
    b = allo[name]
    Ixx, Iyy, Izz, Ixy, Ixz, Iyz = b['inertia']
    return b['mass_t'] * 1000.0, b['cog'], (Ixx, Ixy, Ixz, Iyy, Iyz, Izz)

PMAS_NODE = {k: 99983 + k for k in range(1, 17)}

out = []
out += header
out += ['* 16-body assembly v2 (stage 3 correction W3): cut from the original single-body',
        '* dat futi_lowfreq.dat; panels straddling the I-1/I-3 cut planes are split at the',
        '* plane (interface nodes inserted on the planes); ELM1-ELM9 + EL10-EL16 blocks,',
        '* HYDI in EL16 (structure 1); masses/inertias per body from the 16-body W2 v2',
        '* design table (PMAS nodes 99984-99999 at COGs); interface nodes duplicated',
        '* from 20001. AHD1 on, LHFR off.']
out += ['    01    COOR', '    01NOD5']
for nid in sorted(n for n in nodes if n != 99999):
    out.append(node_line[nid])
for k in range(1, 17):
    _, cog, _ = w2(NAME_OF[k])
    out.append(node_text(PMAS_NODE[k], *cog))
for (body_no, nid), new_id in sorted(dup_of.items(), key=lambda kv: kv[1]):
    out.append('    01' + f'{new_id:5d}' + node_line[nid][11:])
out += [' END01', '*']

panels_of = defaultdict(list)
for elem_no, typ, diff, ids in final_panels:
    panels_of[panel_body[elem_no]].append((elem_no, typ, diff, ids))
for k in range(1, 17):
    out.append(f'    02    ELM{k}' if k < 10 else f'    02    EL{k}')
    out.append(zlwl_line)
    for elem_no, typ, diff, ids in sorted(panels_of[k]):
        kw = (typ + (' DIFF' if diff else '')).ljust(15)
        base = '    02' + kw + '(1)' + ''.join(f'({node_for(k, n):5d})' for n in ids)
        out.append(base + str(elem_no).rjust(81 - len(base)))
    base = '    02' + 'PMAS'.ljust(15) + '(1)' + f'({PMAS_NODE[k]:5d})({k:5d})({k:5d})'
    out.append(base + str(TOTAL_PANELS + k).rjust(81 - len(base)))
    if k == 16:
        out.append('    02HYDI         1')
    out.append(' END02')
out += ['    02    FINI', '*']

out.append('    03    MATE * PMAS point mass (kg) per body, from 16-body W2 v2 design table')
for k in range(1, 17):
    mass, _, _ = w2(NAME_OF[k])
    out.append('    03' + (str(k) + f'{mass:.4E}').rjust(24))
out += [' END03', '*']
out.append('    04    GEOM * PMAS inertia tensor about own PMAS node (= body COG), 16-body W2 v2')
for k in range(1, 17):
    _, _, tensor = w2(NAME_OF[k])
    out.append('    04PMAS' + f'{k:10d}' + ''.join(f'{v:10.4G}' for v in tensor))
out += [' END04', '*']
out += tail

text = '\n'.join(out) + '\n'
with open(OUT, 'w') as f:
    f.write(text)
md5 = hashlib.md5(text.encode()).hexdigest()
print(f'wrote {OUT}: {len(out)} lines, md5 {md5}')

manifest = {'dat_md5': md5, 'total_panels': TOTAL_PANELS, 'total_diff_pieces': int(sum(dif.values())),
            'split_panels': split_stats['split_panels'], 'split_nodes': split_stats['split_nodes'],
            'extra_elements': n_extra, 'duplicates': next_dup - 20001,
            'min_piece_area_m2': min_piece_area[0],
            'counts': {NAME_OF[k]: {'panels': int(cnt[k]), 'diff': int(dif[k])} for k in range(1, 17)}}
json.dump(manifest, open(MANIFEST, 'w'), indent=1)
print('saved manifest')
