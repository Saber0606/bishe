# -*- coding: utf-8 -*-
"""
GATE-B check for W6 BEMIO output (run 2026-11-15; results: gate-b-results.json,
record: gate-b-verification-record.md, same folder).

Inputs (paths below are the as-run local paths; repo/release sources):
  AH1  futi_19body.AH1            -> repo 03-multibody-19body/gate-a-verification/output/
  NPZ  excitation_full_spectrum.npz (anchor Fsyn_corr_plus)
                                  -> repo 03-multibody-19body/gate-a-verification/excitation_full_spectrum.npz
  H5   futi_19body.h5             -> Release W6-output, inside futi_19body.zip
  MAT  futi_19body_hydro.mat      -> Release W6-output, inside futi_19body.zip
Checks: (1) per-body excitation, BEMIO convention inverted, vs AH1 FORCERAO;
(2) corr+ synthesis vs the GATE-A corr+ anchor (criteria: amp <1%, phase <1 deg),
full spectrum and the w<=0.15 subset; (3) A/B matrices vs AH1 blocks;
(4) Ainf: h5 vs hydro.mat, symmetry residual, rigid synthesis vs NREL Table 4.
Structural items (cg exactness, K33 sum, disp-vol sum, dof map) were verified
in the companion run whose outputs are merged into gate-b-results.json.
"""
import h5py, numpy as np, json
AH1='/home/hatch/workspace/graduation-design/stage_multibody_check/futi_19body.AH1'
H5='/home/hatch/workspace/w6-gateb/futi_19body.h5'; MAT='/home/hatch/workspace/w6-gateb/futi_19body_hydro.mat'
NPZ='/home/hatch/workspace/graduation-design/stage_multibody_check/excitation_full_spectrum.npz'
NB,NF,ND=19,47,25
freqs=np.array([0.02,0.04,0.07,0.10,0.15,0.2094,0.23,0.25,0.27,0.30,0.33,0.36,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00,1.05,1.10,1.15,1.20,1.25,1.30,1.35,1.40,1.45,1.50,1.55,1.60,1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.00,2.05,2.10])
headings=np.arange(-180,181,15)
lines=open(AH1,encoding='latin1').read().splitlines()
def sec(name):
    hits=[i for i,l in enumerate(lines) if l.strip()==name]; assert len(hits)==1; return hits[0]
i0=sec('COG'); COG=np.zeros((19,3))
for b in range(19):
    t=lines[i0+1+b].split(); COG[b]=[float(x) for x in t[1:4]]
i0f=sec('FORCERAO')
Fraw=np.zeros((NB,ND,NF,6),dtype=complex)
for b in range(NB):
    for d in range(ND):
        for k in range(NF):
            n=(b*ND+d)*NF+k; base=i0f+1+n*2
            amps=np.array([float(x) for x in lines[base].split()[3:]])
            ph=np.array([float(x) for x in lines[base+1].split()])
            Fraw[b,d,k,:]=amps*np.exp(1j*np.deg2rad(ph))
SEC_OFF={'ADDEDMASS':sec('ADDEDMASS'),'DAMPING':sec('DAMPING')}
def block(name,i,j,k):  # 1-based bodies, 1-based freq
    i0=SEC_OFF[name]; n=((i-1)*NB+(j-1))*NF+(k-1); base=i0+1+n*6; rows=[]
    for r in range(6):
        toks=lines[base+r].split()
        if r==0: toks=toks[3:]
        rows.append([float(x) for x in toks])
    return np.array(rows)
z=np.load(NPZ); Fref=z['Fsyn_corr_plus']; CGtot=z['CGtot']
f=h5py.File(H5,'r'); m=h5py.File(MAT,'r'); h=m['hydro']
rho=float(f['simulation_parameters/rho'][0,0]); g=float(f['simulation_parameters/g'][0,0]); RG=rho*g
out={}
# ---------- 1. excitation: invert BEMIO convention, per-body fidelity ----------
Fh5=np.zeros_like(Fraw)
for b in range(NB):
    re=f[f'body{b+1}/hydro_coeffs/excitation/re'][:]; im=f[f'body{b+1}/hydro_coeffs/excitation/im'][:]
    Fh5[b]=(re+1j*im).transpose(1,2,0)*RG
Frec=np.zeros_like(Fraw)
for b in range(NB):
    for d in range(ND):
        th=np.deg2rad(headings[d]); s=(freqs**2/9.81)*(COG[b,0]*np.cos(th)+COG[b,1]*np.sin(th))
        Frec[b,d]=np.conj(Fh5[b,d])*np.exp(-1j*s)[:,None]
mask=np.zeros_like(Fraw,dtype=bool)
for b in range(NB):
    for j in range(6):
        mask[b,:,:,j]=np.abs(Fraw[b,:,:,j])>0.05*np.abs(Fraw[b,:,:,j]).max()
crel=(np.abs(Frec-Fraw)/np.abs(Fraw))[mask]
arel=(np.abs(np.abs(Frec)-np.abs(Fraw))/np.abs(Fraw))[mask]
perr=np.abs(np.angle(Frec/Fraw,deg=True))[mask]
out['exc_perbody']=dict(n=int(mask.sum()),complex_med=float(np.median(crel)),complex_max=float(crel.max()),amp_med=float(np.median(arel)),amp_max=float(arel.max()),phase_med_deg=float(np.median(perr)),phase_max_deg=float(perr.max()))
print('1 per-body excitation (de-conventionalised):', out['exc_perbody'])
# ---------- 2. corr+ synthesis vs GATE-A reference ----------
Fsyn=np.zeros((ND,NF,6),dtype=complex)
for d in range(ND):
    th=np.deg2rad(headings[d]); u=np.array([np.cos(th),np.sin(th)])
    for k in range(NF):
        w=freqs[k]; kk=w*w/9.81; Ftot=np.zeros(6,dtype=complex)
        for b in range(NB):
            F=Frec[b,d,k,:]*np.exp(+1j*kk*(COG[b,0]*u[0]+COG[b,1]*u[1]))
            r=COG[b]-CGtot; Ftot[:3]+=F[:3]; Ftot[3:]+=F[3:]+np.cross(r,F[:3])
        Fsyn[d,k,:]=Ftot
def stats(A,B,kidx=None):
    idx=np.arange(NF) if kidx is None else np.array(kidx); cr,ar,pr=[],[],[]
    for d in range(ND):
        for j in range(6):
            a,bb=A[d,idx,j],B[d,idx,j]; mk=np.abs(bb)>0.05*np.abs(bb).max()
            cr+=list(np.abs(a[mk]-bb[mk])/np.abs(bb[mk])); ar+=list(np.abs(np.abs(a[mk])-np.abs(bb[mk]))/np.abs(bb[mk])); pr+=list(np.abs(np.angle(a[mk]/bb[mk],deg=True)))
    return dict(n=len(cr),complex_med=float(np.median(cr)),complex_max=float(np.max(cr)),amp_med=float(np.median(ar)),amp_max=float(np.max(ar)),phase_med_deg=float(np.median(pr)),phase_max_deg=float(np.max(pr)))
out['synth_full']=stats(Fsyn,Fref); out['synth_low']=stats(Fsyn,Fref,kidx=[0,1,2,3,4])
print('2 synthesis FULL:', out['synth_full']); print('2 synthesis w<=0.15:', out['synth_low'])
# ---------- 3. A / B matrices vs AH1 blocks ----------
def assemble(kind,k):  # k 0-based; returns (114,114) normalized as stored in h5
    M=np.zeros((114,114))
    for b in range(NB): M[b*6:(b+1)*6,:]=f[f'body{b+1}/hydro_coeffs/{kind}'][:,:,k]
    return M
worstA=worstB=0.0; worstAk=worstBk=-1
for k in range(NF):
    Aref=np.zeros((114,114)); Bref=np.zeros((114,114))
    for i in range(1,NB+1):
        for j in range(1,NB+1):
            Aref[(i-1)*6:i*6,(j-1)*6:j*6]=block('ADDEDMASS',i,j,k+1)
            Bref[(i-1)*6:i*6,(j-1)*6:j*6]=block('DAMPING',i,j,k+1)
    Ah=assemble('added_mass/all',k)*rho
    Bh=assemble('radiation_damping/all',k)*rho*freqs[k]
    ra=np.abs(Ah-Aref).max()/np.abs(Aref).max(); rb=np.abs(Bh-Bref).max()/np.abs(Bref).max()
    if ra>worstA: worstA,worstAk=ra,k
    if rb>worstB: worstB,worstBk=rb,k
out['AB_vs_AH1']=dict(A_worst_rel=float(worstA),A_worst_w=float(freqs[worstAk]),B_worst_rel=float(worstB),B_worst_w=float(freqs[worstBk]))
print('3 A/B vs AH1 (max-abs rel to per-freq peak):', out['AB_vs_AH1'])
# ---------- 4. Ainf ----------
Ainf=np.zeros((114,114))
for b in range(NB): Ainf[b*6:(b+1)*6,:]=f[f'body{b+1}/hydro_coeffs/added_mass/inf_freq'][:]
out['Ainf_h5_vs_mat']=float(np.abs(Ainf-h['Ainf'][:].T).max())
Ainf_dim=Ainf*rho
out['Ainf_sym_resid']=float(np.abs(Ainf_dim-Ainf_dim.T).max()/np.abs(Ainf_dim).max())
def skew(r): return np.array([[0,-r[2],r[1]],[r[2],0,-r[0]],[-r[1],r[0],0]])
def rigid_syn(M6,P):
    S=np.zeros((6,6))
    for b in range(NB):
        L=np.zeros((6,6)); L[:3,:3]=np.eye(3); L[3:,3:]=np.eye(3); L[:3,3:]=-skew(COG[b]-P)
        for c in range(NB):
            Lc=np.zeros((6,6)); Lc[:3,:3]=np.eye(3); Lc[3:,3:]=np.eye(3); Lc[:3,3:]=-skew(COG[c]-P)
            S+=L.T@M6[b*6:(b+1)*6,c*6:(c+1)*6]@Lc
    return S
Ainf_cg=rigid_syn(Ainf_dim,CGtot); Ainf_or=rigid_syn(Ainf_dim,np.zeros(3))
paper={'A11':9.64e6,'A33':2.48e7,'A44':1.16e10,'A55':1.16e10,'A66':2.01e10,'A15':-1.01e8}
mine={'A11':Ainf_or[0,0],'A33':Ainf_or[2,2],'A44':Ainf_or[3,3],'A55':Ainf_or[4,4],'A66':Ainf_or[5,5],'A15':Ainf_or[0,4]}
out['Ainf_origin']=dict(mine={k:float(v) for k,v in mine.items()},paper=paper,dev_pct={k:float((mine[k]/paper[k]-1)*100) for k in paper})
out['Ainf_cg_diag']=[float(Ainf_cg[i,i]) for i in range(6)]
print('4 Ainf: h5-vs-mat diff', out['Ainf_h5_vs_mat'], '| sym resid', out['Ainf_sym_resid'])
print('4 Ainf about SWL origin vs paper Table 4 dev %:', out['Ainf_origin']['dev_pct'])
json.dump(out, open('/home/hatch/workspace/w6-gateb/gateb_final.json','w'), indent=1)
np.savez('/home/hatch/workspace/w6-gateb/gateb_final.npz', Fsyn_h5=Fsyn, Frec=Frec)
print('saved gateb_final.json/.npz')
