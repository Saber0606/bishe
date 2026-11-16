# 16-body W2 allocation solver.
# Inputs ONLY: single-body dat geometry (geometry json), dat Deck 03/04 totals,
# NREL Table 2 components. Placement/shape RULES are fixed a priori (see doc);
# the three accounts (mass / CoG-z / Izz, from dat Deck 03/04) close the system:
# steel shares are the solution nearest to surface-area proportionality that
# satisfies the accounts exactly; Ixx/Iyy are left as independent checks.
import json, math
import numpy as np
from scipy.optimize import minimize

GEO = json.load(open('/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_from_singlebody_geometry.json'))
P = GEO['parts']
CHAINS = ['180', '60', '300']
RHO = 1.025  # t/m3

# targets from the single-body dat itself
M_TOT = 17854.0            # t, Deck 03
ZG_TOT = -14.940           # m, node 99999
IXX_T, IZZ_T = 1.251e10, 2.367e10   # kg m2, Deck 04 (about total CoG)

# components (NREL Table 2)
STEEL, FIXED, FLUID, TOWER = 3914.0, 2540.0, 11300.0, 100.0
FIXED_PER_COL = FIXED/3.0
A_CS_COL = math.pi*6.25**2          # outer column cross-section, m2
RHO_FIX = 3.5                        # t/m3, iron-ore concrete (design assumption)
V_FIX = FIXED_PER_COL/RHO_FIX        # m3 per column
H_FIX = V_FIX/A_CS_COL               # block height at column bottom
Z_FIX = -20.0 + H_FIX/2.0            # its centroid z
Z_TOWER = 15.0

segV = P['180_S1']['volume_m3']      # all segments equal: 831.40
seg_area = {b: P[b]['area_m2'] for b in P}
A_TOT = sum(seg_area.values())
area_share = {b: STEEL*seg_area[b]/A_TOT for b in P}

def build(phi):
    """Return per-body (mass, cog, inertia-about-own-cog in chain frame) given steel dict and phi."""
    raise NotImplementedError

def assemble(steel, phi):
    # fluid: pontoons bottom-up fill fraction phi of interior (= displaced vol, thin-shell)
    f_seg = RHO*phi*segV                       # t per segment
    z_f_seg = -20.0 + 3.5*phi                  # fluid centroid z in segment (bottom-up, 7 m tall)
    f_col_tot = FLUID - 12*f_seg
    f_col = f_col_tot/3.0                      # t per outer column
    h_f = f_col/(RHO*A_CS_COL)
    z_f_col = (-20.0 + H_FIX) + h_f/2.0        # stacked above fixed block
    bodies = {}
    # segments
    for c in CHAINS:
        ux, uy = {'180': (-1,0), '60': (0.5, math.sqrt(3)/2), '300': (0.5, -math.sqrt(3)/2)}[c]
        for i in range(1, 5):
            b = f'{c}_S{i}'
            ms = steel[b]; mf = f_seg
            ac = P[b]['area_centroid']; vc = P[b]['cob']
            m = ms + mf
            cog = tuple((ms*ac[k] + mf*(vc[k] if k != 2 else z_f_seg))/m for k in range(3))
            # solid box L x 12.5 x 7 in chain frame (s,t,z), about own CoG
            L = 9.50175
            Iss = m*(12.5**2 + 7.0**2)/12*1000; Itt = m*(L**2 + 7.0**2)/12*1000; Izz = m*(L**2 + 12.5**2)/12*1000
            # rotate (s,t) -> (x,y): I in global: R diag(Iss,Itt) R^T ; Ixy etc.
            Ixx = Iss*ux*ux + Itt*uy*uy; Iyy = Iss*uy*uy + Itt*ux*ux; Ixy = (Iss-Itt)*ux*uy
            bodies[b] = (m, cog, (Ixx, Iyy, Izz, Ixy, 0.0, 0.0))
    # outer columns: steel shell + fixed block + fluid block, chain frame s = radial
    for c in CHAINS:
        ux, uy = {'180': (-1,0), '60': (0.5, math.sqrt(3)/2), '300': (0.5, -math.sqrt(3)/2)}[c]
        b = f'{c}_COL'
        ms = steel[b]
        ac = P[b]['area_centroid']
        # component centroids in global: steel at area centroid; fixed/fluid on axis at s=51.75
        comp = [(ms, tuple(ac), 'shell', 6.25, 35.0),
                (FIXED_PER_COL, (51.75*ux, 51.75*uy, Z_FIX), 'solid', 6.25, H_FIX),
                (f_col, (51.75*ux, 51.75*uy, z_f_col), 'solid', 6.25, h_f)]
        m = sum(x[0] for x in comp)
        cog = tuple(sum(x[0]*x[1][k] for x in comp)/m for k in range(3))
        # inertia about body CoG: cylinder pieces about own centroidal axes (axis = z)
        Ixx = Iyy = Izz = 0.0
        for (mm, cc, kind, R, h) in comp:
            if kind == 'shell': izz_o = mm*R*R*1000; ixx_o = mm*(R*R/2 + h*h/12)*1000
            else: izz_o = mm*R*R/2*1000; ixx_o = mm*(3*R*R + h*h)/12*1000
            d2 = [(cc[k]-cog[k])**2 for k in range(3)]
            Izz += izz_o + mm*1000*(d2[0]+d2[1])
            Ixx += ixx_o + mm*1000*(d2[1]+d2[2])
            Iyy += ixx_o + mm*1000*(d2[0]+d2[2])
        bodies[b] = (m, cog, (Ixx, Iyy, Izz, 0.0, 0.0, 0.0))
    # central column: steel shell R=5 h=35 + tower point mass at z=15
    b = 'CEN'
    ms = steel[b]; ac = P[b]['area_centroid']
    comp = [(ms, tuple(ac)), (TOWER, (0.0, 0.0, Z_TOWER))]
    m = ms + TOWER
    cog = tuple(sum(x[0]*x[1][k] for x in comp)/m for k in range(3))
    izz_o = ms*25.0*1000; ixx_o = ms*(25.0/2 + 35.0**2/12)*1000
    d2s = [(ac[k]-cog[k])**2 for k in range(3)]; d2t = [(comp[1][1][k]-cog[k])**2 for k in range(3)]
    Izz = izz_o + ms*1000*(d2s[0]+d2s[1]) + TOWER*1000*(d2t[0]+d2t[1])
    Ixx = ixx_o + ms*1000*(d2s[1]+d2s[2]) + TOWER*1000*(d2t[1]+d2t[2])
    Iyy = ixx_o + ms*1000*(d2s[0]+d2s[2]) + TOWER*1000*(d2t[0]+d2t[2])
    bodies[b] = (m, cog, (Ixx, Iyy, Izz, 0.0, 0.0, 0.0))
    # totals
    M = sum(v[0] for v in bodies.values())
    G = tuple(sum(v[0]*v[1][k] for v in bodies.values())/M for k in range(3))
    It = [0.0]*6
    for (m, cog, (Ixx, Iyy, Izz, Ixy, Ixz, Iyz)) in bodies.values():
        d = [cog[k]-G[k] for k in range(3)]
        It[0] += Ixx + m*1000*(d[1]**2+d[2]**2); It[1] += Iyy + m*1000*(d[0]**2+d[2]**2)
        It[2] += Izz + m*1000*(d[0]**2+d[1]**2); It[3] += Ixy - m*1000*d[0]*d[1]
    return bodies, M, G, It, f_seg, f_col

# unknowns: steel for CEN, COL (x3 sym), SEG (x12 sym), phi  -> parametrize by type
def unpack(x):
    s_cen, s_col, s_seg, phi = x
    steel = {'CEN': s_cen}
    for c in CHAINS:
        steel[f'{c}_COL'] = s_col
        for i in range(1, 5): steel[f'{c}_S{i}'] = s_seg
    return steel, phi

def residuals(x):
    steel, phi = unpack(x)
    bodies, M, G, It, f_seg, f_col = assemble(steel, phi)
    return np.array([sum(steel.values()) - STEEL,
                     G[2] - ZG_TOT,
                     (It[2] - IZZ_T)/1e8])

cons = [{'type': 'eq', 'fun': lambda x: residuals(x)[0]},
        {'type': 'eq', 'fun': lambda x: residuals(x)[1]},
        {'type': 'eq', 'fun': lambda x: residuals(x)[2]}]
x0 = np.array([area_share['CEN'], area_share['180_COL'], area_share['180_S1'], 0.93])
def objective(x):
    steel, phi = unpack(x)
    dev = [(steel[b]-area_share[b])/50.0 for b in steel]
    return sum(d*d for d in dev) + (phi-0.93)**2*100
sol = minimize(objective, x0, method='SLSQP', constraints=cons,
               bounds=[(50, 2500), (50, 2500), (20, 800), (0.3, 1.0)])
print("solver success:", sol.success, sol.message)
steel, phi = unpack(sol.x)
bodies, M, G, It, f_seg, f_col = assemble(steel, phi)
print(f"phi (pontoon fill) = {phi:.4f}; fluid per segment = {f_seg:.1f} t; fluid per column = {f_col:.1f} t")
print(f"steel: CEN {steel['CEN']:.1f} t (area share {area_share['CEN']:.1f}), COL {steel['180_COL']:.1f} t (share {area_share['180_COL']:.1f}), SEG {steel['180_S1']:.1f} t (share {area_share['180_S1']:.1f})")
print(f"TOTAL mass = {M:.2f} t (target {M_TOT})")
print(f"TOTAL CoG = ({G[0]:.4f}, {G[1]:.4f}, {G[2]:.4f}) (target 0,0,{ZG_TOT})")
print(f"Ixx = {It[0]:.4e} (target {IXX_T:.4e}, dev {(It[0]/IXX_T-1)*100:+.2f}%)  <-- independent check")
print(f"Iyy = {It[1]:.4e} (dev {(It[1]/IXX_T-1)*100:+.2f}%)")
print(f"Izz = {It[2]:.4e} (target {IZZ_T:.4e}, dev {(It[2]/IZZ_T-1)*100:+.2f}%)")
print(f"Ixy total = {It[3]:.3e}")
print("\nper-body table:")
for b in ['CEN'] + [f'{c}_S{i}' for c in CHAINS for i in range(1,5)] + [f'{c}_COL' for c in CHAINS]:
    m, cog, I = bodies[b]
    print(f"  {b:8s} m={m:8.1f} t  CoG=({cog[0]:8.3f},{cog[1]:8.3f},{cog[2]:8.3f})  Ixx={I[0]:.4e} Iyy={I[1]:.4e} Izz={I[2]:.4e} Ixy={I[3]:+.3e}")
json.dump({'phi': phi, 'fluid_per_segment_t': f_seg, 'fluid_per_column_t': f_col,
           'steel': {b: steel[b] for b in steel},
           'bodies': {b: {'mass_t': bodies[b][0], 'cog': list(bodies[b][1]), 'inertia': list(bodies[b][2])} for b in bodies},
           'totals': {'mass_t': M, 'cog': list(G), 'inertia': It}},
          open('/home/hatch/workspace/graduation-design/stage3-correction-16body/design_16body_w2_allocation_results.json', 'w'), indent=1)
print("saved allocation results json")
