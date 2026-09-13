from pathlib import Path
import math, re, sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'results'/'reproduced'
T=ROOT/'manuscript'/'tables'
MAIN=(ROOT/'manuscript'/'main.tex').read_text()
checks=[]
def check(name,cond,detail=''):
    ok=bool(cond); checks.append(ok); print(('PASS' if ok else 'FAIL'),name,detail)
def close(a,b,tol=5e-6): return abs(float(a)-float(b))<=tol

# Fresh executable source values.
a=pd.read_csv(R/'m19a_replication_summary.csv').iloc[0]
b=pd.read_csv(R/'m19b_replication_summary.csv').iloc[0]
c=pd.read_csv(R/'m19c_replication_summary.csv').iloc[0]
d=pd.read_csv(R/'m19d_replication_summary.csv').iloc[0]
p=pd.read_csv(R/'m20a_replication_summary.csv').set_index('path')
ap=pd.read_csv(R/'m20b_replication_summary.csv').set_index('path')
aq=pd.read_csv(R/'m20c2_replication_summary.csv').set_index('path')
m21=pd.read_csv(R/'m21_replication_summary.csv').set_index('study')

check('M19a submission gain',close(a.mean_safe_gain,0.0013128394))
check('M19b control advantage',close(b.mean_safe_minus_matched_gain,0.0296645957))
check('M19c dispersion correlation',close(c.safe_dispersion_gain_corr,0.3229285116))
check('M19d submission gain',close(d.mean_safe_gain,0.0015846215))
check('M20a temperature support',close(p.loc['temperature','support_range'],55.1645098))
check('M20a temperature safe-control',close(p.loc['temperature','safe_minus_matched_gain'],0.0275082732))
check('Appliances safe-control null',close(ap.loc['temperature','mean_safe_minus_matched_gain'],-0.0093469071))
check('Air Quality safe-control positive',close(aq.loc['temperature','mean_safe_minus_matched_gain'],0.0392515975))
check('Air Quality temperature not operationally dominant',aq.loc['gain','mean_safe_gain']>aq.loc['temperature','mean_safe_gain'])
check('M21 synthetic ratio',close(m21.loc['Synthetic path comparison','near_containment_ratio'],2.363111951))
check('M21 Appliances counterexample',m21.loc['Appliances Energy','near_containment_ratio']<1)
check('M21 Air enrichment',m21.loc['Air Quality','near_containment_ratio']>1)

# Publication CSVs must carry the executable values at reported precision.
real=pd.read_csv(T/'table_real_world.csv').set_index('Dataset')
check('Table real Appliances gain',close(real.loc['Appliances Energy','Temperature mean best-safe gain'],0.00685,1e-8))
check('Table real Air gain',close(real.loc['Air Quality','Temperature mean best-safe gain'],0.00856,1e-8))
pa=pd.read_csv(T/'table_path_ablation.csv').set_index('Path')
check('Table path temperature gain',close(pa.loc['temperature','Mean best-safe gain'],0.00253,1e-8))
check('Table path gain spectral radius',close(pa.loc['gain','Spectral-radius range'],1.570,1e-8))
mt=pd.read_csv(T/'table_m21_safe_width.csv').set_index('Study')
check('Table M21 synthetic ratio',str(mt.loc['Synthetic path comparison','Near-optimal containment ratio'])=='2.36x')
check('Table M21 Appliances ratio',str(mt.loc['Appliances Energy','Near-optimal containment ratio'])=='0.69x')
check('Table M21 Air ratio',str(mt.loc['Air Quality','Near-optimal containment ratio'])=='1.39x')

# No superseded v18.4 submission framing in current manuscript.
banned=['retained historical','could not be recovered','do not numerically recover','supporting historical evidence','publication reconstructions','publication-reconstruction']
for phrase in banned:
    check(f'no superseded framing: {phrase}',phrase.lower() not in MAIN.lower())

# Fresh figures expected by manuscript.
for n in range(2,8):
    matches=list((ROOT/'figures').glob(f'fig{n}_*.png'))
    check(f'Figure {n} exists',len(matches)==1,str(matches[0].name if matches else 'missing'))

print(f'\nSubmission-layer summary: {sum(checks)} / {len(checks)} passed')
if not all(checks): sys.exit(1)
