#!/usr/bin/env python3
"""W4 quick check: parse 16-body LIS hydrostatic blocks + diffracting counts,
compare against W1/W2 v2 design table and W3 v2 manifest counts."""
import re, json, sys

LIS = sys.argv[1] if len(sys.argv) > 1 else "FUTI_16BODY.LIS"
text = open(LIS, encoding="utf-8", errors="replace").read()

# --- diffracting elements per structure (SECONDARY DIFFRACTION MODELLING CHECK blocks, in order)
diff = [int(x) for x in re.findall(r"NUMBER OF DIFFRACTING ELEMENTS[\s.]*?(\d+)\s*\n", text)]
diff_ignored = [int(x) for x in re.findall(r"NUMBER OF DIFFRACTING ELEMENTS IGNORED[\s.]*?(\d+)\s*\n", text)]

# --- hydrostatic blocks in order
mesh_disp = [float(x) for x in re.findall(r"MESH BASED DISPLACEMENT[\s.]*=\s*([-\d.E+]+)", text)]
mass_disp = [float(x) for x in re.findall(r"MASS BASED DISPLACEMENT[\s.]*=\s*([-\d.E+]+)", text)]
cog = [(float(a), float(b), float(c)) for a, b, c in
       re.findall(r"STRUCTURE C\.O\.G\.\s+GX=\s*([-\d.]+)\s+GY=\s*([-\d.]+)\s+GZ=\s*([-\d.]+)", text)]
cob = [(float(a), float(b), float(c)) for a, b, c in
       re.findall(r"POSITION OF THE CENTRE OF BUOYANCY\s+BX =\s*([-\d.]+)\s+BY =\s*([-\d.]+)\s+BZ =\s*([-\d.]+)", text)]
awp = [float(x) for x in re.findall(r"CUT WATER PLANE AREA[\s.]*=\s*([-\d.E+]+)", text)]
k33 = [float(x) for x in re.findall(r"HEAVE\( Z\) =\s*([-\d.E+]+)", text)]

names = ["CEN", "180_S1", "180_S2", "180_S3", "180_S4", "180_COL",
         "60_S1", "60_S2", "60_S3", "60_S4", "60_COL",
         "300_S1", "300_S2", "300_S3", "300_S4", "300_COL"]
design_vol = [2482.60, 831.40, 831.40, 831.40, 831.40, 2566.09,
              831.39, 831.43, 831.41, 831.41, 2566.40,
              831.39, 831.43, 831.41, 831.41, 2565.87]
design_diff = [670, 255, 257, 256, 256, 616, 265, 263, 264, 253, 629, 262, 264, 264, 262, 615]
design_mass = [1120.1] + [961.5]*4 + [1731.9] + [961.5]*4 + [1731.9] + [961.5]*4 + [1731.9]
RHO, G = 1025.0, 9.81

print(f"blocks found: diff={len(diff)} mesh={len(mesh_disp)} mass={len(mass_disp)} cog={len(cog)} cob={len(cob)} awp={len(awp)} k33={len(k33)}")
print(f"{'body':8s} {'DIFF':>5s} {'ok':>3s} {'meshVol':>9s} {'design':>8s} {'dev%':>7s} {'massVol':>8s} {'mass_t':>8s} {'des_t':>7s} {'CoBz':>8s} {'Awp':>8s} {'K33':>11s}")
sv = sm = sa = sk = 0.0
wbx = wby = wbz = 0.0
for i in range(16):
    mass_t = mass_disp[i] * RHO / 1000.0
    dev = (mesh_disp[i] - design_vol[i]) / design_vol[i] * 100
    ok = "OK" if diff[i] == design_diff[i] else "XX"
    print(f"{names[i]:8s} {diff[i]:5d} {ok:>3s} {mesh_disp[i]:9.2f} {design_vol[i]:8.2f} {dev:+7.2f} {mass_disp[i]:8.2f} {mass_t:8.2f} {design_mass[i]:7.1f} {cob[i][2]:8.4f} {awp[i]:8.3f} {k33[i]:11.4E}")
    sv += mesh_disp[i]; sm += mass_t; sa += awp[i]; sk += k33[i]
    wbx += mesh_disp[i]*cob[i][0]; wby += mesh_disp[i]*cob[i][1]; wbz += mesh_disp[i]*cob[i][2]
print(f"\nSUM mesh disp  = {sv:.2f} m3   (single-body LIS 20157.80, dev {(sv-20157.80)/20157.80*100:+.3f}%)")
print(f"SUM mass       = {sm:.2f} t    (design 17854.0, dev {(sm-17854.0)/17854.0*100:+.4f}%)")
print(f"SUM Awp        = {sa:.3f} m2   (single-body LIS 443.576, dev {(sa-443.576)/443.576*100:+.3f}%)")
print(f"SUM K33        = {sk:.5E}  (single-body LIS 4.46027E6, dev {(sk-4.46027e6)/4.46027e6*100:+.3f}%)")
print(f"rho*g*SUM Awp  = {RHO*G*sa:.5E}  (vs SUM K33 dev {(RHO*G*sa-sk)/sk*100:+.3f}%)")
print(f"Vol-weighted CoB = ({wbx/sv:.4f}, {wby/sv:.4f}, {wbz/sv:.4f})  (single-body LIS (0,0,-13.6393))")
print(f"SUM DIFF = {sum(diff)} (design 5651), ignored total = {sum(diff_ignored)}")
print(f"CoG z list = {[c[2] for c in cog]}")
