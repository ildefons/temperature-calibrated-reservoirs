from pathlib import Path
import sys
import json
import math
import pandas as pd
import nbformat

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/'results/frozen'
REPRO=ROOT/'results/reproduced'
NB=ROOT/'notebooks'

checks=[]
def check(name, condition, detail=''):
    ok=bool(condition); checks.append((name,ok,detail)); print(('PASS' if ok else 'FAIL'),name,detail)
    return ok

def close(a,b,tol=1e-6): return abs(float(a)-float(b))<=tol

# Manuscript-frozen tables: exact source-of-truth checks.
m23=pd.read_csv(FROZEN/'table_m23_robustness.csv').set_index('configuration')
check('M23 baseline containment lift',close(m23.loc['N60_K13_baseline','near_oracle_containment_lift'],2.86367,1e-5))
check('M23 K25 containment lift',close(m23.loc['N60_K25_finer_grid','near_oracle_containment_lift'],2.16005,1e-5))
check('M23 N150 continuous indicator',close(m23.loc['N150_K13_larger_reservoir','safe_dispersion_gain_correlation'],0.576738,1e-6))

shift=pd.read_csv(FROZEN/'table_srp04b_shift_family.csv').set_index('held_out_shift_family')
check('SRP04b correlated-noise gain',close(shift.loc['Strong correlated additive noise','historical_sparse_relative_gain'],0.33103,1e-5))
check('SRP04b missingness failure retained',shift.loc['Block missingness','historical_sparse_relative_gain']<0)

tasks=pd.read_csv(FROZEN/'table_srp04b_task_results.csv').set_index('task')
check('SRP04b NARMA oracle',close(tasks.loc['NARMA10','target_fitted_sparse_oracle_nrmse'],0.751775,1e-6))
check('SRP04b meta selector not hidden',tasks.loc['Lorenz-x','label_free_meta_selector_nrmse']>tasks.loc['Lorenz-x','historically_fitted_sparse_nrmse'])

# Fresh reconstruction checks: qualitative invariants, not historical point-estimate matching.
required=['m19a_replication_summary.csv','m19b_replication_summary.csv','m19c_replication_summary.csv','m19d_replication_summary.csv','m20a_replication_summary.csv','m21_replication_summary.csv']
for f in required: check(f'fresh output exists: {f}',(REPRO/f).exists())

if (REPRO/'m19a_replication_summary.csv').exists():
    d=pd.read_csv(REPRO/'m19a_replication_summary.csv').iloc[0]
    check('M19a fresh safe gain nonnegative',d.mean_safe_gain>=0,f"{d.mean_safe_gain:.6g}")
    check('M19a fresh near containment > 0.5',d.near_optimal_containment>0.5,f"{d.near_optimal_containment:.3f}")
if (REPRO/'m19b_replication_summary.csv').exists():
    d=pd.read_csv(REPRO/'m19b_replication_summary.csv').iloc[0]
    check('M19b fresh true > matched near containment',d.true_near_containment>d.matched_near_containment)
    check('M19b fresh safe-minus-matched gain positive',d.mean_safe_minus_matched_gain>0,f"{d.mean_safe_minus_matched_gain:.6g}")
if (REPRO/'m19c_replication_summary.csv').exists():
    d=pd.read_csv(REPRO/'m19c_replication_summary.csv').iloc[0]
    check('M19c fresh dispersion correlation positive',d.safe_dispersion_gain_corr>0,f"{d.safe_dispersion_gain_corr:.3f}")
    check('M19c fresh anchor correlation positive',d.anchor_spread_gain_corr>0,f"{d.anchor_spread_gain_corr:.3f}")
if (REPRO/'m19d_replication_summary.csv').exists():
    d=pd.read_csv(REPRO/'m19d_replication_summary.csv').iloc[0]
    check('M19d fresh mean safe gain positive',d.mean_safe_gain>0,f"{d.mean_safe_gain:.6g}")
if (REPRO/'m20a_replication_summary.csv').exists():
    d=pd.read_csv(REPRO/'m20a_replication_summary.csv').set_index('path')
    check('M20a fresh temperature changes effective support',d.loc['temperature','support_range']>50)
    check('M20a fresh gain leaves effective support fixed',abs(d.loc['gain','support_range'])<1e-6)
    check('M20a fresh temperature control enrichment positive',d.loc['temperature','safe_minus_matched_gain']>0)
    check('M20a fresh sparsity support is hard and broad',d.loc['sparsity','support_range']>50)

# Notebook hygiene.
for p in sorted(NB.glob('*.ipynb')):
    nb=nbformat.read(p,4)
    first=nb.cells[0].source if nb.cells else ''
    check(f'{p.name}: author header','Ildefons Magrans de Abril' in first)
    errors=[]
    for ci,c in enumerate(nb.cells):
        if c.cell_type=='code':
            for o in c.get('outputs',[]):
                if o.get('output_type')=='error': errors.append((ci,o.get('ename'),o.get('evalue')))
    check(f'{p.name}: no embedded execution errors',not errors,str(errors[:2]))

# Smoke-test artifacts for the two large original analyses.
check('M23 current-environment smoke notebook exists',(ROOT/'tests/M23_smoke_executed.ipynb').exists())
check('SRP04b current-environment smoke notebook exists',(ROOT/'tests/SRP04b_smoke_executed.ipynb').exists())

report=pd.DataFrame(checks,columns=['check','passed','detail'])
report.to_csv(ROOT/'tests/verification_results.csv',index=False)
print('\nSummary:',int(report.passed.sum()),'/',len(report),'passed')
if not report.passed.all():
    sys.exit(1)
