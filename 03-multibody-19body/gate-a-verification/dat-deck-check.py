#!/usr/bin/env python3
"""Deck-level check of futi_19body.dat (stage 3, W3) against the AH1-derived
W2 restored ledger (w2-mass-accounting-19body.md) and W1 segmentation table.

Parses Deck 01 (PMAS node coordinates), Deck 02 (ELM blocks: element counts,
DIFF counts, PMAS assignment), Deck 03 (MATE masses, fixed-column format),
Deck 04 (PMAS inertia tensors), Deck 05/06 (depth/density, freq/heading).
Outputs dat-deck-check-results.json next to this script.
"""
import json, re, sys
from pathlib import Path

DAT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "workspace/user/files/futi_19body.dat"
lines = DAT.read_text().splitlines()

# ---- W2 restored ledger (from AH1, full precision values as published, t / m / kg*m^2)
W2 = [
    # body, mass_t, cog(x,y,z), Ixx, Iyy, Izz, Ixy
    (1, 2262.70, (0.001, 0.003, -12.247), 2.401e8, 2.401e8, 6.817e7, -1.58e4),
    (2, 658.33, (-11.194, -0.001, -16.501), 1.275e7, 6.409e6, 1.269e7, 1.94e3),
    (3, 656.45, (-18.803, 0.000, -16.498), 1.272e7, 6.358e6, 1.265e7, 4.46e2),
    (4, 656.73, (-26.401, 0.000, -16.500), 1.273e7, 6.365e6, 1.266e7, -3.95e2),
    (5, 656.92, (-34.003, -0.001, -16.498), 1.273e7, 6.370e6, 1.266e7, -3.08e3),
    (6, 656.88, (-41.606, 0.002, -16.502), 1.271e7, 6.374e6, 1.265e7, -1.82e3),
    (7, 1911.80, (-50.998, 0.000, -13.322), 1.892e8, 1.875e8, 5.074e7, 2.31e3),
    (8, 657.60, (5.599, 9.697, -16.501), 7.974e6, 1.116e7, 1.267e7, 2.75e6),
    (9, 656.63, (9.400, 16.284, -16.499), 7.952e6, 1.113e7, 1.265e7, 2.75e6),
    (10, 656.73, (13.201, 22.865, -16.500), 7.957e6, 1.114e7, 1.266e7, 2.76e6),
    (11, 656.90, (17.001, 29.448, -16.499), 7.962e6, 1.114e7, 1.266e7, 2.76e6),
    (12, 657.06, (20.804, 36.032, -16.502), 7.965e6, 1.113e7, 1.265e7, 2.75e6),
    (13, 1911.80, (25.499, 44.166, -13.321), 1.880e8, 1.888e8, 5.075e7, 7.35e5),
    (14, 658.48, (5.596, -9.692, -16.499), 8.002e6, 1.117e7, 1.269e7, -2.75e6),
    (15, 656.75, (9.402, -16.284, -16.500), 7.958e6, 1.114e7, 1.266e7, -2.76e6),
    (16, 656.72, (13.202, -22.866, -16.500), 7.957e6, 1.113e7, 1.266e7, -2.76e6),
    (17, 656.43, (17.001, -29.446, -16.499), 7.950e6, 1.113e7, 1.265e7, -2.76e6),
    (18, 657.25, (20.802, -36.030, -16.502), 7.970e6, 1.114e7, 1.266e7, -2.75e6),
    (19, 1911.90, (25.499, -44.166, -13.322), 1.880e8, 1.888e8, 5.075e7, -7.32e5),
]
W1_DIFF = [670, 192, 190, 192, 192, 192, 616, 201, 196, 198, 197, 188, 629, 196, 198, 198, 196, 196, 615]

res = {}

# ---- Deck 01: node count + PMAS node coordinates
i01 = next(i for i, l in enumerate(lines) if l.strip() == "01    COOR" or "01    COOR" in l)
e01 = next(i for i, l in enumerate(lines) if l.strip() == "END01")
deck01 = lines[i01:e01]
node_lines = [l for l in deck01 if re.match(r"\s+01", l) and "COOR" not in l and "NOD5" not in l]
res["deck01_node_count"] = len(node_lines)

def parse_node_line(l):
    toks = l.split()
    if toks[0] == "01":
        nid = int(toks[1]); xyz = [float(t) for t in toks[2:5]]
    else:  # '01' fused with node number, e.g. '0120584'
        nid = int(toks[0][2:]); xyz = [float(t) for t in toks[1:4]]
    return nid, xyz

nodes = {}
for l in node_lines:
    nid, xyz = parse_node_line(l)
    nodes[nid] = xyz
pmas_nodes = {n: nodes[99980 + n] for n in range(1, 20)}
res["pmas_node_ids_ok"] = sorted(pmas_nodes) == list(range(1, 20))
res["max_node_id"] = max(nodes)

# nodes added relative to the overall single-body dat (same ANSYS export base)
_cands = [Path(__file__).resolve().parents[2] / "01-single-body-validation/output/futi_lowfreq.dat",
          Path.home() / "workspace/bishe-sync/01-single-body-validation/output/futi_lowfreq.dat"]
SINGLE = next(p for p in _cands if p.exists())
slines = SINGLE.read_text().splitlines()
si01 = next(i for i, l in enumerate(slines) if "01    COOR" in l)
se01 = next(i for i, l in enumerate(slines) if l.strip() == "END01")
snodes = {}
for l in slines[si01:se01]:
    if re.match(r"\s+01", l) and "COOR" not in l and "NOD5" not in l:
        nid, xyz = parse_node_line(l)
        snodes[nid] = xyz
added = sorted(set(nodes) - set(snodes))
removed = sorted(set(snodes) - set(nodes))
res["single_dat_node_count"] = len(snodes)
res["nodes_added_vs_single"] = len(added)
res["nodes_added_non_pmas"] = [n for n in added if n < 99981]
res["nodes_removed_vs_single"] = removed
common = set(nodes) & set(snodes)
res["common_node_coords_identical"] = all(nodes[n] == snodes[n] for n in common)

# ---- Deck 02: ELM blocks
blocks = []
cur = None
for l in lines:
    m = re.match(r"\s+02\s+ELM?(\d+)\s*$", l)  # ELM1..ELM9, then EL10..EL19 (fixed-width name)
    if m:
        cur = {"elm": int(m.group(1)), "qppl": 0, "tppl": 0, "diff": 0, "pmas": None, "elem_ids": []}
        blocks.append(cur); continue
    if cur is not None:
        if "02QPPL" in l:
            cur["qppl"] += 1
            if "DIFF" in l: cur["diff"] += 1
            cur["elem_ids"].append(int(l.split()[-1]))
        elif "02TPPL" in l:
            cur["tppl"] += 1
            if "DIFF" in l: cur["diff"] += 1
            cur["elem_ids"].append(int(l.split()[-1]))
        elif "02PMAS" in l:
            g = re.findall(r"\(\s*(\d+)\)", l)
            cur["pmas"] = {"groups": [int(x) for x in g], "elem_no": int(l.split()[-1])}
        elif l.strip() == "END02":
            cur = None
res["elm_blocks"] = len(blocks)
res["total_elements"] = sum(b["qppl"] + b["tppl"] for b in blocks)
res["total_diff"] = sum(b["diff"] for b in blocks)
all_ids = [i for b in blocks for i in b["elem_ids"]]
res["elem_ids_unique"] = len(all_ids) == len(set(all_ids))
res["per_block"] = [
    {"elm": b["elm"], "total": b["qppl"] + b["tppl"], "diff": b["diff"],
     "diff_vs_w1": b["diff"] - W1_DIFF[b["elm"] - 1],
     "pmas_node": b["pmas"]["groups"][1] if b["pmas"] else None,
     "pmas_mat": b["pmas"]["groups"][2] if b["pmas"] else None}
    for b in blocks
]

# ---- Deck 03: MATE masses (fixed-column: material no. fused with value)
i03 = next(i for i, l in enumerate(lines) if "03    MATE" in l)
e03 = next(i for i in range(i03, len(lines)) if lines[i].strip() == "END03")
masses = {}
for l in lines[i03 + 1:e03]:
    tok = l.split()[-1]
    m = re.match(r"^(\d{1,2})(\d\.\d+E[+-]\d+)$", tok)
    masses[int(m.group(1))] = float(m.group(2))
res["deck03_count"] = len(masses)
res["deck03_total_t"] = sum(masses.values()) / 1000.0

# ---- Deck 04: PMAS inertia (regex float extraction; order Ixx Ixy Ixz Iyy Iyz Izz)
inertia = {}
for l in lines:
    if "04PMAS" in l:
        rest = l.split("04PMAS", 1)[1]
        body = int(rest.split()[0])
        nums = [float(x) for x in re.findall(r"[-+]?(?:\d+\.\d*(?:E[-+]\d+)?|\d+(?:E[-+]\d+)?|\.\d+(?:E[-+]\d+)?)", rest.split(None, 1)[1])]
        assert len(nums) == 6, (body, nums)
        inertia[body] = nums  # Ixx Ixy Ixz Iyy Iyz Izz
res["deck04_count"] = len(inertia)

# ---- Deck 05/06
res["deck05"] = [l.strip() for l in lines if "05DPTH" in l or "05DENS" in l or "ACCG" in l]
freq_blocks = [l for l in lines if re.match(r"\s+06\s+F", l)]
res["deck06_blocks"] = len(freq_blocks)
freq_vals = []
for l in lines:
    if "06FREQ" in l:
        freq_vals += [float(x) for x in re.findall(r"\d+\.\d+", l.split("FREQ", 1)[1].split("    ", 1)[-1]) if float(x) < 10]
# simpler: collect from first FDR block only
first = []
started = False
for l in lines:
    if re.match(r"\s+06\s+FDR1", l): started = True; continue
    if started and "06FREQ" in l:
        first += [float(t) for t in l.split()[3:]]
    if started and "06DIRN" in l:
        res["dirn_line"] = l.strip(); break
res["freq_count_first_block"] = len(first)
res["freq_first_last"] = [first[0], first[-1]] if first else None

# ---- Comparisons vs W2
comp = []
for (b, m_t, cog, Ixx, Iyy, Izz, Ixy) in W2:
    dm = masses[b] / 1000.0 - m_t
    dcog = [pmas_nodes[b][k] - cog[k] for k in range(3)]
    Iv = inertia[b]
    comp.append({
        "body": b, "mass_dat_t": masses[b] / 1000.0, "mass_w2_t": m_t, "dmass_t": round(dm, 4),
        "cog_dat": pmas_nodes[b], "dcog": [round(x, 4) for x in dcog],
        "I_dat": Iv,
        "dIxx_rel": (Iv[0] - Ixx) / Ixx, "dIyy_rel": (Iv[3] - Iyy) / Iyy,
        "dIzz_rel": (Iv[5] - Izz) / Izz, "dIxy_abs": Iv[1] - Ixy,
    })
res["comparison"] = comp
res["max_abs_dmass_t"] = max(abs(c["dmass_t"]) for c in comp)
res["max_abs_dcog_m"] = max(abs(x) for c in comp for x in c["dcog"])
res["max_abs_dI_diag_rel"] = max(abs(c[k]) for c in comp for k in ("dIxx_rel", "dIyy_rel", "dIzz_rel"))

# ---- Three accounts recomputed from dat alone
M = sum(masses.values())
cg = [sum(masses[b] * pmas_nodes[b][k] for b in masses) / M for k in range(3)]
res["dat_total_mass_t"] = M / 1000.0
res["dat_total_cog"] = cg
# inertia about total CoG via parallel-axis
import itertools
Itot = [[0.0] * 3 for _ in range(3)]
for b in masses:
    d = [pmas_nodes[b][k] - cg[k] for k in range(3)]
    Iv = inertia[b]
    Ii = [[Iv[0], Iv[1], Iv[2]], [Iv[1], Iv[3], Iv[4]], [Iv[2], Iv[4], Iv[5]]]
    dd = sum(x * x for x in d)
    for a, c in itertools.product(range(3), range(3)):
        Itot[a][c] += Ii[a][c] + masses[b] * ((dd if a == c else 0.0) - d[a] * d[c])
res["dat_total_inertia"] = {"Ixx": Itot[0][0], "Iyy": Itot[1][1], "Izz": Itot[2][2],
                            "dIxx_rel_vs_paper": (Itot[0][0] - 1.251e10) / 1.251e10,
                            "dIzz_rel_vs_paper": (Itot[2][2] - 2.367e10) / 2.367e10}

# ---- LIS per-structure diffracting element counts (solver's own count, for cross-check)
LIS = Path.home() / "workspace/graduation-design/stage_multibody_check/FUTI_19BODY.LIS"
if LIS.exists():
    import re as _re
    vals = [int(x) for x in _re.findall(r"NUMBER OF DIFFRACTING ELEMENTS[. ]+(\d+)", LIS.read_text(errors="ignore"))]
    res["lis_diff_per_structure"] = vals[:19]
    res["lis_diff_total"] = sum(vals[:19])
    res["lis_diff_vs_dat_per_body"] = [vals[i] - res["per_block"][i]["diff"] for i in range(19)]

out = Path(__file__).with_name("dat-deck-check-results.json")
out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in res.items() if k not in ("comparison", "per_block")}, indent=1, ensure_ascii=False))
print("per_block diff_vs_w1:", [b["diff_vs_w1"] for b in res["per_block"]])
print("per_block totals:", [b["total"] for b in res["per_block"]])
print("pmas nodes/mats:", [(b["pmas_node"], b["pmas_mat"]) for b in res["per_block"]])
print("max|dmass| t:", res["max_abs_dmass_t"], " max|dcog| m:", res["max_abs_dcog_m"], " max|dI diag| rel:", res["max_abs_dI_diag_rel"])
for c in comp:
    print(c["body"], c["mass_dat_t"], "dm", c["dmass_t"], "dcog", c["dcog"], "dI%", [round(100 * c[k], 3) for k in ("dIxx_rel", "dIyy_rel", "dIzz_rel")], "dIxy", c["dIxy_abs"])
