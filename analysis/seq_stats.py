"""Sequential-arm statistics for the paper: within-session formal/yard and
formal/party price ratios (paired geometric mean ratio, bootstrap CI with
seed 3, Wilcoxon signed-rank test), split by which photograph was shown
first. Duplicate-flagged rows are dropped.
Usage (from the repo root; reads data/halo_master_v1.csv):
    python3 analysis/seq_stats.py"""
import pandas as pd, numpy as np
from scipy import stats
rng=np.random.default_rng(3)
d=pd.read_csv('data/halo_master_v1.csv'); d=d[d.dup_flag==0]
s=d[(d.arm=='sequential')&d.turn_label.isin(['estimate_1','estimate_2'])&(d.necklace_price>0)]
rows=[]
for sid,g in s.groupby('session_id'):
    if len(g)<2: continue
    p=dict(zip(g.context,g.necklace_price)); first=g.sort_values('order_seen').context.iloc[0]
    rows.append(dict(model=g.model.iloc[0],sid=sid,first=first,**p))
w=pd.DataFrame(rows)
for m in ['claude','gpt5','gpt4o']:
    x=w[w.model==m]
    for other in ['yard','party']:
        y=x.dropna(subset=['formal',other]); 
        if len(y)<3: print(m,other,'n',len(y)); continue
        lr=np.log(y.formal/y[other]); bs=[rng.choice(lr,len(lr)).mean() for _ in range(5000)]
        try: p=stats.wilcoxon(lr).pvalue
        except Exception: p=float('nan')
        print(f"{m:6s} formal/{other:5s} n={len(y):3d} GMratio={np.exp(lr.mean()):.2f} [{np.exp(np.percentile(bs,2.5)):.2f},{np.exp(np.percentile(bs,97.5)):.2f}] wilcoxon p={p:.4f}; formal-first mean logratio {lr[y['first']=='formal'].mean():.2f} (n={(y['first']=='formal').sum()}) other-first {lr[y['first']!='formal'].mean():.2f} (n={(y['first']!='formal').sum()})")
print(w.groupby('model').size())
