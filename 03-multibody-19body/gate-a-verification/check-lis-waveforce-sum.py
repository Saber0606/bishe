# -*- coding: utf-8 -*-
"""
Verify (from the LIS files themselves, print precision):
  sum over 19 bodies of the complex FK+DIFFRACTION wave-force RAO
  vs the single-body model's FK+DIFFRACTION table, at the same (omega, heading).
Three summation methods:
  plain    : F = sum F_b ;  M = sum M_b            (exactly what "just add them" says)
  transfer : F = sum F_b ;  M = sum (M_b + r_b x F_b), r_b = COG_b - CG_total
  corr+    : per-body factor exp(+i k (x_b cos th + y_b sin th)) applied first,
             then transfer (the GATE-A adjudicated synthesis, from AH1 work)
COG_b and CG_total are taken from the 19-body AH1 COG block (full precision).
"""
import re, numpy as np, json

LIS19 = '/home/hatch/workspace/graduation-design/stage_multibody_check/FUTI_19BODY.LIS'
LIS1  = '/home/hatch/workspace/bishe-sync/01-single-body-validation/output/FUTI_LOWFREQ.LIS'
AH1   = '/home/hatch/workspace/graduation-design/stage_multibody_check/futi_19body.AH1'

FREQS = [0.02,0.04,0.07,0.10,0.15,0.2094,0.23,0.25,0.27,0.30,0.33,0.36,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00,1.05,1.10,1.15,1.20,1.25,1.30,1.35,1.40,1.45,1.50,1.55,1.60,1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.00,2.05,2.10]
HEADINGS = list(range(-180,181,15))
DOF = ['Fx','Fy','Fz','Mx','My','Mz']

# ---- COGs from AH1 ----
lines = open(AH1, encoding='latin1').read().splitlines()
i0 = [i for i,l in enumerate(lines) if l.strip()=='COG'][0]
COG=[]
for b in range(19):
    t=lines[i0+1+b].split(); assert int(t[0])==b+1
    COG.append([float(x) for x in t[1:4]])
COG=np.array(COG)
i0m=[i for i,l in enumerate(lines) if l.strip()=='MASS'][0]
mass=np.zeros(19); pos=i0m+1
for b in range(19):
    rows=[]
    for r in range(6):
        t=lines[pos].split()
        if r==0: t=t[1:]
        rows.append([float(x) for x in t]); pos+=1
    mass[b]=rows[0][0]
CGtot=(mass[:,None]*COG).sum(0)/mass.sum()
print(f"COG parsed; CGtot={CGtot}, Mtot={mass.sum()/1000:.1f} t")

struct_re = re.compile(r'S\s*T\s*R\s*U\s*C\s*T\s*U\s*R\s*E\s+(\d+)')
row_re = re.compile(r'^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(.*)$')
KIND='FROUDE KRYLOV + DIFFRACTION FORCES-VARIATION WITH WAVE PERIOD/FREQUENCY'

def parse_lis(path, expect_structs):
    """Return dict[(struct,heading)] -> (47,6) complex for FK+DIFF, freq-variation tables only."""
    text=open(path,encoding='utf-8',errors='replace').read().splitlines()
    blocks={}; cur_struct=None; i=0; n=0
    while i < len(text):
        m=struct_re.search(text[i])
        if m: cur_struct=int(m.group(1))
        if text[i].strip()==KIND:
            rows=[]; heading=None; j=i+1
            while j < len(text) and len(rows)<47:
                mm=row_re.match(text[j])
                if mm:
                    toks=mm.group(3).split()
                    if len(toks)==13: heading=float(toks[0]); vals=toks[1:]
                    elif len(toks)==12: vals=toks
                    else: vals=None
                    if vals is not None and len(vals)==12:
                        rows.append([float(v) for v in vals])
                j+=1
            if len(rows)==47 and heading is not None:
                arr=np.array(rows); amp=arr[:,0::2]; pha=np.radians(arr[:,1::2])
                key=(cur_struct,int(round(heading)))
                assert key not in blocks, f"dup {key}"
                blocks[key]=amp*np.exp(1j*pha); n+=1
            i=j
        else:
            i+=1
    print(f"{path.split('/')[-1]}: FK+DIFF freq-blocks parsed = {n} (expect {expect_structs*25})")
    assert n==expect_structs*25
    return blocks

b19=parse_lis(LIS19,19)
b1=parse_lis(LIS1,1)

def synth(heading, method):
    """Return (47,6) complex synthesised total for one heading."""
    th=np.radians(heading); u=np.array([np.cos(th),np.sin(th)])
    out=np.zeros((47,6),dtype=complex)
    for k,w in enumerate(FREQS):
        kk=w*w/9.81; Ftot=np.zeros(6,dtype=complex)
        for b in range(19):
            F=b19[(b+1,heading)][k].copy()
            if method=='corr+':
                F=F*np.exp(+1j*kk*(COG[b,0]*u[0]+COG[b,1]*u[1]))
            if method=='plain':
                Ftot+=F
            else:
                r=COG[b]-CGtot
                Mt=F[3:]+np.cross(r,F[:3])
                Ftot[:3]+=F[:3]; Ftot[3:]+=Mt
        out[k]=Ftot
    return out

spots=[(0.02,0),(0.02,180),(0.50,0),(0.50,180),(1.00,0),(1.00,180),(1.15,180)]
print("\nSpot checks: complex relative error |calc-ref|/|ref| (%) and |calc| vs |ref|")
results={}
for (w,h) in spots:
    k=FREQS.index(w); ref=b1[(1,h)][k]
    line=f"\nw={w} heading={h}: "
    print(line)
    for dof in range(6):
        print(f"  {DOF[dof]:>2} ref |F|={abs(ref[dof]):.4e}  phase={np.degrees(np.angle(ref[dof])):8.2f} deg")
    for method in ['plain','transfer','corr+']:
        S=synth(h,method)[k]
        errs=np.abs(S-ref)/np.abs(ref)*100
        results[f"{method} w={w} h={h}"]={DOF[d]:float(errs[d]) for d in range(6)}
        print(f"  [{method:>8}] cplx rel err %: "+"  ".join(f"{DOF[d]}={errs[d]:9.3f}" for d in range(6)))

# Full-spectrum masked medians for the three methods (LIS print precision)
print("\nFull spectrum (25 headings x 47 freqs x 6 dof, 5% peak mask per heading/dof):")
for method in ['plain','transfer','corr+']:
    errs=[]
    for h in HEADINGS:
        S=synth(h,method); R=np.stack([b1[(1,h)]]*1)[0]
        for dof in range(6):
            peak=np.abs(R[:,dof]).max(); mask=np.abs(R[:,dof])>0.05*peak
            errs.append(np.abs(S[mask,dof]-R[mask,dof])/np.abs(R[mask,dof]))
    e=np.concatenate(errs)
    print(f"  [{method:>8}] masked pts={e.size}  median={np.median(e)*100:.3f}%  p95={np.percentile(e,95)*100:.2f}%  max={e.max()*100:.1f}%")
    results[f"fullspec {method}"]={"median_pct":float(np.median(e)*100),"p95_pct":float(np.percentile(e,95)*100),"max_pct":float(e.max()*100),"n":int(e.size)}

json.dump(results, open('/home/hatch/workspace/graduation-design/stage3-correction-16body/check_lis_waveforce_sum_results.json','w'), indent=1)
print("\nsaved results json")
