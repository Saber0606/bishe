#!/usr/bin/env python3
"""GATE-style synthesis verification for FUTI 19-body AQWA output.
Parses futi_19body.AH1, transforms all sub-body coefficients to the
overall CoG, sums, and compares with the validated single-body baseline
(from technical route V2.5 / GATE 1A / GATE 2 level-1 target values).
"""
import numpy as np, json, sys
np.set_printoptions(suppress=True, linewidth=200)

AH1='futi_19body.AH1'
lines=open(AH1,encoding='latin1').read().splitlines()
NB=19; NF=47; ND=25
freqs=np.array([0.02,0.04,0.07,0.10,0.15,0.2094,0.23,0.25,0.27,0.30,0.33,0.36,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00,1.05,1.10,1.15,1.20,1.25,1.30,1.35,1.40,1.45,1.50,1.55,1.60,1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.00,2.05,2.10])

def sec(name):
    return [i for i,l in enumerate(lines) if l.strip()==name][0]

def parse_simple(name, ncols):
    i0=sec(name); out={}
    for b in range(1,NB+1):
        toks=lines[i0+b].split(); assert int(toks[0])==b, (name,toks)
        out[b]=np.array([float(x) for x in toks[1:1+ncols]])
    return out

cog_d=parse_simple('COG',3); cob_d=parse_simple('COB',3); disp_d=parse_simple('DISPLACEMENT',1)
COG=np.array([cog_d[b] for b in range(1,NB+1)])
COB=np.array([cob_d[b] for b in range(1,NB+1)])
DISP=np.array([disp_d[b][0] for b in range(1,NB+1)])

def parse_mat(name):
    i0=sec(name); mats={}
    pos=i0+1
    for b in range(1,NB+1):
        rows=[]
        for r in range(6):
            toks=lines[pos].split()
            if r==0:
                assert int(toks[0])==b; toks=toks[1:]
            rows.append([float(x) for x in toks]); pos+=1
        mats[b]=np.array(rows)
    return mats, pos

MASS,_=parse_mat('MASS')
HYD,_=parse_mat('HYDSTIFFNESS')
mass=np.array([MASS[b][0,0] for b in range(1,NB+1)])

def skew(r):
    return np.array([[0,-r[2],r[1]],[r[2],0,-r[0]],[-r[1],r[0],0.]])
def S_mat(r):
    S=np.zeros((6,6)); S[:3,:3]=np.eye(3); S[3:,3:]=np.eye(3); S[3:,:3]=skew(r); return S
def T_mat(r):
    return S_mat(r).T

# ---------- 1. static synthesis ----------
Mtot=mass.sum()
CGtot=(mass[:,None]*COG).sum(0)/Mtot
Vtot=DISP.sum()
CBtot=(DISP[:,None]*COB).sum(0)/Vtot
# inertia about combined CoG: I = sum( I_i + m_i * ((r.r)I - r r^T) ), r = COG_i - CGtot ; rotational block of MASS is inertia about own CoG
Itot=np.zeros((3,3))
for b in range(NB):
    r=COG[b]-CGtot; m=mass[b]
    Itot += MASS[b+1][3:,3:] + m*((r@r)*np.eye(3)-np.outer(r,r))
print(f"Total mass = {Mtot:.4e} kg = {Mtot/1000:.1f} t   (target 17854 t)")
print(f"Total mesh displacement = {Vtot:.2f} m3  (target 20158 m3, paper 20206)")
print(f"Combined CoG = {CGtot}  (target (0,0,-14.94))")
print(f"Combined CoB (disp-weighted) = {CBtot}  (target ~(0,0,-13.64))")
print(f"Combined inertia about combined CoG diag = {np.diag(Itot)}  (target 1.251e10,1.251e10,2.367e10)")
print(f"Inertia offdiag = {Itot[0,1]:.3e} {Itot[0,2]:.3e} {Itot[1,2]:.3e}")
print(f"Mass-based displacement total = {Mtot/1025:.2f} m3")
print("\nPer-body table:")
print("body      mass(t)    disp(m3)  mass/disp%    CoG")
for b in range(NB):
    print(f"{b+1:4d} {mass[b]/1000:10.1f} {DISP[b]:10.1f} {100*(mass[b]/1025-DISP[b])/DISP[b]:+9.1f}   {COG[b]}")

# ---------- 2. hydrostatic stiffness synthesis about combined CoG ----------
Ktot=np.zeros((6,6))
for b in range(NB):
    r=COG[b]-CGtot
    Ktot += S_mat(r) @ HYD[b+1] @ T_mat(r)
print("\nSynthesised hydrostatic stiffness about combined CoG (6x6):")
print(Ktot)
print(f"K33 synth = {Ktot[2,2]:.4e}  (target 4.460e6)")
print(f"K44 synth = {Ktot[3,3]:.4e} ; K55 synth = {Ktot[4,4]:.4e}  (overall TOTAL about CoG target 5.229e9; hydro-only component 2.201e9)")
# also naive sum (no transform)
Kn=sum(HYD[b] for b in range(1,NB+1))
print(f"K33 naive sum = {Kn[2,2]:.4e}, K44 naive={Kn[3,3]:.4e}, K55 naive={Kn[4,4]:.4e}")

# ---------- 3. added mass synthesis ----------
i0=sec('ADDEDMASS')
# entries: ((i-1)*NB+(j-1))*NF + (k-1), each 6 lines
def added_block(i,j,k):
    n=((i-1)*NB+(j-1))*NF+(k-1); base=i0+1+n*6; rows=[]
    for r in range(6):
        toks=lines[base+r].split()
        if r==0: toks=toks[3:]
        rows.append([float(x) for x in toks])
    return np.array(rows)

def synth_added(k):
    Aeq=np.zeros((6,6))
    for i in range(1,NB+1):
        Si=S_mat(COG[i-1]-CGtot)
        for j in range(1,NB+1):
            Aeq += Si @ added_block(i,j,k) @ T_mat(COG[j-1]-CGtot)
    return Aeq

# damping synthesis (same transform)
i0d=sec('DAMPING')
def damp_block(i,j,k):
    n=((i-1)*NB+(j-1))*NF+(k-1); base=i0d+1+n*6; rows=[]
    for r in range(6):
        toks=lines[base+r].split()
        if r==0: toks=toks[3:]
        rows.append([float(x) for x in toks])
    return np.array(rows)
def synth_damp(k):
    Beq=np.zeros((6,6))
    for i in range(1,NB+1):
        Si=S_mat(COG[i-1]-CGtot)
        for j in range(1,NB+1):
            Beq += Si @ damp_block(i,j,k) @ T_mat(COG[j-1]-CGtot)
    return Beq

print("\nAdded-mass synthesis (about combined CoG):")
A_by_k={}
for k in [1,6,10,14,47]:
    A=synth_added(k); A_by_k[k]=A
    print(f" w={freqs[k-1]:.4f} rad/s : A11={A[0,0]:.4e} A22={A[1,1]:.4e} A33={A[2,2]:.4e} A44={A[3,3]:.4e} A55={A[4,4]:.4e} A66={A[5,5]:.4e} A15={A[0,4]:.4e} A24={A[1,3]:.4e}")
print(" target @2.10: A33 = 2.43e7 ; paper Ainf: A11=9.64e6 A33=2.48e7 A44/A55=1.16e10 A66=2.01e10 A15=-1.01e8 (about SWL origin, not CoG)")

# ---------- 4. natural frequencies from synth K, M, A ----------
# heave: solve w = sqrt(K33/(M+A33(w))) by interpolation over all freqs
A33s=[]; A55s=[]; A44s=[]
for k in range(1,NF+1):
    A=synth_added(k); A33s.append(A[2,2]); A55s.append(A[4,4]); A44s.append(A[3,3])
A33s=np.array(A33s); A55s=np.array(A55s); A44s=np.array(A44s)
def natfreq(K, M_or_I, Aarr):
    w=np.sqrt(K/(M_or_I+Aarr))  # implied w at each tabulated A(w)
    # find crossing w_tab vs implied
    diff=freqs-w
    for idx in range(NF-1):
        if diff[idx]==0: return freqs[idx]
        if diff[idx]*diff[idx+1]<0:
            t=diff[idx]/(diff[idx]-diff[idx+1]); return freqs[idx]+t*(freqs[idx+1]-freqs[idx])
    return None
w_heave=natfreq(Ktot[2,2], Mtot, A33s)
w_pitch=natfreq(Ktot[4,4], Itot[1,1], A55s)
w_roll=natfreq(Ktot[3,3], Itot[0,0], A44s)
print(f"\nSynthesised natural freq: heave = {w_heave} rad/s (target 0.315, GATE2 synth 0.3143)")
print(f"Synthesised natural freq: pitch = {w_pitch} rad/s (target 0.466, GATE2 synth 0.4633)")
print(f"Synthesised natural freq: roll  = {w_roll} rad/s (expect ~ pitch by symmetry)")

# ---------- 5. excitation synthesis, heading 180 and 0, with/without CoG phase correction ----------
i0f=sec('FORCERAO')
headings=np.arange(-180,181,15)
def force_block(body, d_idx, k):
    # entries: ((body-1)*ND + (d-1))*NF + (k-1), each 2 lines (amps, phases deg)
    n=((body-1)*ND+(d_idx-1))*NF+(k-1); base=i0f+1+n*2
    t1=lines[base].split()[3:]; amps=np.array([float(x) for x in t1])
    ph=np.array([float(x) for x in lines[base+1].split()])
    return amps*np.exp(1j*np.deg2rad(ph))
def synth_force(d_idx, k, correct_phase, wave_from_deg):
    # wave travelling direction: AQWA heading = direction wave comes FROM? test both conventions via sign param passed in wave_from_deg handling outside
    Ftot=np.zeros(6, dtype=complex)
    theta=np.deg2rad(headings[d_idx-1])
    # wave number
    w=freqs[k-1]; kk=w*w/9.81
    # propagation unit vector: if heading is direction wave travels TOWARDS measured from +x: u=(cos,sin)
    # phase at point r relative to origin for a plane wave exp(i(wt - k u.r)) -> spatial factor exp(-i k u.r) depending convention; caller flips sign by using corrected with + or -
    for b in range(1,NB+1):
        F=force_block(b,d_idx,k)
        if correct_phase:
            r=COG[b-1]
            # AQWA phases are referenced to each body's own CoG (per V2.5 memo): to refer all to global origin,
            # multiply by exp(-i * k * (r . u)) where u = propagation direction. We test u=(cos theta, sin theta) with sign in exponent as -; result stored, alternative sign tested separately by caller using theta+pi equivalence.
            phase_corr=np.exp(-1j*kk*(r[0]*np.cos(theta)+r[1]*np.sin(theta)))
            F=F*phase_corr
        r=COG[b-1]-CGtot
        Ft=F[:3]; Mt=F[3:]+np.cross(r,Ft)
        Ftot[:3]+=Ft; Ftot[3:]+=Mt
    return Ftot

print("\nExcitation synthesis |Fz| (N/m) etc:")
for dval in [180,0,-180]:
    didx=list(headings).index(dval)+1
    for k in [1,14,26]:
        Fn=synth_force(didx,k,False,None); Fc=synth_force(didx,k,True,None)
        print(f" heading {dval:5d} w={freqs[k-1]:.3f}: naive |Fx|={abs(Fn[0]):.4e} |Fz|={abs(Fn[2]):.4e} |My|={abs(Fn[4]):.4e} || phase-corr |Fx|={abs(Fc[0]):.4e} |Fz|={abs(Fc[2]):.4e} |My|={abs(Fc[4]):.4e}")
print(" target long-wave: |Fz| -> 4.44e6 N/m as w->0")

# symmetry check of added mass full matrix at k=47 (should be symmetric)
k=47; full=np.zeros((NB*6,NB*6))
for i in range(1,NB+1):
    for j in range(1,NB+1):
        full[(i-1)*6:i*6,(j-1)*6:j*6]=added_block(i,j,k)
asym=np.max(np.abs(full-full.T))/np.max(np.abs(full))
print(f"\nAdded mass full-matrix asymmetry at w=2.10: max|A-A^T|/max|A| = {asym:.3e}")
Btot=synth_damp(47)
print(f"Damping synth @2.10 diag: {np.diag(Btot)}")

json_out=dict(Mtot_t=float(Mtot/1000), Vtot=float(Vtot), CG=CGtot.tolist(), CB=CBtot.tolist(),
  Idiag=np.diag(Itot).tolist(), K33=float(Ktot[2,2]), K44=float(Ktot[3,3]), K55=float(Ktot[4,4]),
  A33_210=float(A_by_k[47][2,2]), A55_210=float(A_by_k[47][4,4]), A11_210=float(A_by_k[47][0,0]),
  w_heave=w_heave, w_pitch=w_pitch, w_roll=w_roll)
open('synthesis_results.json','w').write(json.dumps(json_out,indent=1))
print("\nJSON:", json.dumps(json_out,indent=1))
