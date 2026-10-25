"""Inferential statistics for the paper: ratios of geometric means with 95%
percentile bootstrap CIs (10,000 resamples, seed 20261025), two-sided
Mann-Whitney U tests, and Wilson intervals for refusals and counterfactual
admissions. Supports the image, debiasing, text-only, institutional-label,
flat-lay, refusal and sequential self-report results.
Usage (from the repo root):
    python3 analysis/halo_stats.py data/halo_master_v1.csv          # all rows
    python3 analysis/halo_stats.py data/halo_master_v1.csv nodup    # drop dup_flag rows
The paper reports price statistics without duplicate-flagged rows (identical
either way) and refusal and same-object counts on all rows."""
import sys, numpy as np, pandas as pd
from scipy import stats
rng=np.random.default_rng(20261025)
d=pd.read_csv(sys.argv[1])
excl_dup = len(sys.argv)>2 and sys.argv[2]=='nodup'
if excl_dup: d=d[d.dup_flag==0]
print('rows',len(d),'exclude dup' if excl_dup else 'all rows')
def gm(x): return float(np.exp(np.mean(np.log(x))))
def ratio_ci(a,b,B=10000):
    la,lb=np.log(a),np.log(b)
    bs=[np.mean(rng.choice(la,len(la)))-np.mean(rng.choice(lb,len(lb))) for _ in range(B)]
    return np.exp(np.mean(la)-np.mean(lb)), np.exp(np.percentile(bs,2.5)), np.exp(np.percentile(bs,97.5))
def price(m,cond,ctx,arm='fresh'):
    s=d[(d.model==m)&(d.arm==arm)&(d.turn_label=='estimate')&(d.condition==cond)&(d.context==ctx)].necklace_price.dropna()
    return s[s>0].values
def cmp(m,cond,c1,c2,label=None):
    a,b=price(m,cond,c1),price(m,cond,c2)
    if len(a)<3 or len(b)<3: return None
    r,lo,hi=ratio_ci(a,b); p=stats.mannwhitneyu(a,b,alternative='two-sided').pvalue
    return f"{m:8s} {cond:11s} {c1:8s} n={len(a):2d} GM=${gm(a):6.1f} | {c2:8s} n={len(b):2d} GM=${gm(b):6.1f} | ratio {r:4.2f} [{lo:4.2f},{hi:4.2f}] MWU p={p:.4f}"
print('\n== IMAGE, fresh arm, necklace price: formal vs yard / formal vs flatlay / yard vs flatlay (blind) ==')
for m in ['claude','gpt5','grok','kimi']:
    for c1,c2 in [('formal','yard'),('formal','isolated'),('yard','isolated'),('party','yard')]:
        r=cmp(m,'blind',c1,c2); print(r)
print('\n== DEBIAS: formal vs yard ==')
for m in ['claude','gpt5','grok','kimi']:
    print(cmp(m,'debias','formal','yard'))
print('\n== TEXT-ONLY T1 formal vs T3 yard ==')
for m in ['claude','gpt5','gpt4o','grok','kimi','deepseek']:
    print(cmp(m,'text','formal','yard'))
print('\n== TEXT-ONLY n valid per cell ==')
for m in ['claude','gpt5','gpt4o','grok','kimi','deepseek']:
    print(m,{c:len(price(m,'text',c)) for c in ['formal','party','yard']})
print('\n== INST corp vs social (formal & party pooled) ==')
for m in ['claude','gpt5','gpt4o','grok','kimi']:
    a=np.concatenate([price(m,'inst_corp',c) for c in ['formal','party']]); b=np.concatenate([price(m,'inst_social',c) for c in ['formal','party']])
    if len(a)>=3 and len(b)>=3:
        r,lo,hi=ratio_ci(a,b); p=stats.mannwhitneyu(a,b).pvalue
        print(f"{m:8s} n={len(a)}/{len(b)} corp ${gm(a):.1f} social ${gm(b):.1f} ratio {r:.2f} [{lo:.2f},{hi:.2f}] p={p:.3f}")
    else: print(m,'n too small',len(a),len(b))
print('\n== FLAT-LAY vs receipt/retail ==')
for m in ['claude','gpt5','grok','kimi']:
    a=price(m,'blind','isolated'); r,lo,hi=ratio_ci(a,np.full(len(a),2.43)); r2,l2,h2=ratio_ci(a,np.full(len(a),24.5))
    print(f"{m:8s} n={len(a)} GM=${gm(a):.1f} x{r:.1f} [{lo:.1f},{hi:.1f}] vs receipt ; x{r2:.2f} [{l2:.2f},{h2:.2f}] vs retail mid; hit retail band(15-40)={np.mean((a>=15)&(a<=40)):.2f}")
print('\n== REFUSALS, fresh arm image estimates (blind/debias/inst), Wilson ==')
f=d[(d.arm=='fresh')&(d.turn_label=='estimate')&(d.stimulus.str.startswith('S'))&(d.condition!='open')]
from statsmodels.stats.proportion import proportion_confint
for m in ['claude','gpt5','gpt4o','grok','kimi']:
    x=f[f.model==m]; k=int((x.refusal==1).sum()); n=len(x); lo,hi=proportion_confint(k,n,method='wilson')
    print(f"{m:8s} {k}/{n} = {k/n:.2f} [{lo:.2f},{hi:.2f}]")
print('\n== GPT-4o refusals by context/condition ==')
x=f[f.model=='gpt4o']; print(x.groupby(['condition','context']).refusal.agg(['sum','count']))
print('\n== SEQUENTIAL arm sessions per model ==')
s=d[d.arm=='sequential']; print(s.groupby('model').session_id.nunique())
print('\n== counterfactual admission per session ==')
for m in ['claude','gpt5','gpt4o']:
    cf=s[(s.model==m)&(s.turn_label=='counterfactual')]
    yes=cf.raw_text.str.strip().str.lower().str.startswith(('yes','**yes')).sum(); n=len(cf)
    lo,hi=proportion_confint(yes,n,method='wilson'); print(f"{m:8s} yes {yes}/{n}={yes/n:.2f} [{lo:.2f},{hi:.2f}]")
print('\n== same_object (truth: same object) distribution ==')
for m in ['claude','gpt5','gpt4o']:
    so=s[(s.model==m)&(s.turn_label=='same_object')].same_object.value_counts(dropna=False).to_dict(); print(m,so)
