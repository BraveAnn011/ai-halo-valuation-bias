"""Supplementary statistics for the paper: debiasing ratio of ratios with
bootstrap CI (seed 7), blind-condition geometric means with bootstrap CIs,
text-only geometric means by context, valid-estimate counts, and the
cue-probe keyword screen. Duplicate-flagged rows are dropped.
Usage (from the repo root; reads data/halo_master_v1.csv):
    python3 analysis/extra_stats.py"""
import sys, re, numpy as np, pandas as pd
from scipy import stats
rng=np.random.default_rng(7)
d=pd.read_csv('data/halo_master_v1.csv'); d=d[d.dup_flag==0]
def price(m,cond,ctx):
    s=d[(d.model==m)&(d.arm=='fresh')&(d.turn_label=='estimate')&(d.condition==cond)&(d.context==ctx)].necklace_price.dropna()
    return np.log(s[s>0].values)
print('== debias effect: change in formal/yard log-ratio, bootstrap (ratio of ratios) ==')
for m in ['claude','gpt5','grok','kimi']:
    bf,by,df,dy=[price(m,c,x) for c,x in [('blind','formal'),('blind','yard'),('debias','formal'),('debias','yard')]]
    obs=(df.mean()-dy.mean())-(bf.mean()-by.mean())
    bs=[(rng.choice(df,len(df)).mean()-rng.choice(dy,len(dy)).mean())-(rng.choice(bf,len(bf)).mean()-rng.choice(by,len(by)).mean()) for _ in range(10000)]
    print(f"{m:7s} blind {np.exp(bf.mean()-by.mean()):.2f}x -> debias {np.exp(df.mean()-dy.mean()):.2f}x ; ratio of ratios {np.exp(obs):.2f} [{np.exp(np.percentile(bs,2.5)):.2f},{np.exp(np.percentile(bs,97.5)):.2f}]  n={len(bf)},{len(by)},{len(df)},{len(dy)}")
print('\n== GM and bootstrap 95% CI of blind image prices ==')
for m in ['claude','gpt5','grok','kimi']:
    for ctx in ['formal','party','yard','isolated']:
        x=price(m,'blind',ctx); bs=[rng.choice(x,len(x)).mean() for _ in range(5000)]
        print(f"{m:7s} {ctx:9s} n={len(x):2d} GM=${np.exp(x.mean()):6.1f} [{np.exp(np.percentile(bs,2.5)):6.1f},{np.exp(np.percentile(bs,97.5)):6.1f}]")
print('\n== TEXT-ONLY GM by context ==')
for m in ['claude','gpt5','gpt4o','grok','kimi','deepseek']:
    print(m,{c:(len(price(m,'text',c)),round(float(np.exp(price(m,'text',c).mean())),1)) for c in ['formal','party','yard']})
print('\n== why fewer valid text/image rows? format_ok / refusal of non-refused fresh estimates ==')
f=d[(d.arm=='fresh')&(d.turn_label=='estimate')]
print(f.groupby(['model'])[['necklace_price']].apply(lambda x: x.necklace_price.notna().mean()))
print(f[f.condition=='text'].groupby('model').apply(lambda x: pd.Series({'rows':len(x),'priced':x.necklace_price.notna().sum(),'refusal':int((x.refusal==1).sum())})))
print('\n== cue_probe: share mentioning clothing/setting words (fresh arm, blind/debias/inst image) ==')
words=r"blazer|jacket|outfit|attire|cloth|dress|shirt|flannel|\bcap\b|hat|setting|background|wood|panel|professional|formal|party|lighting|club|recycling|yard|wardrobe|styling|stylish"
c=d[(d.arm=='fresh')&(d.turn_label=='cue_probe')&(d.condition.isin(['blind','debias','inst_corp','inst_social']))&(d.model!='gpt4o')]
c=c.assign(m=c.raw_text.fillna('').str.lower().str.contains(words,regex=True))
print(c.groupby(['model','context']).m.agg(['mean','count']).round(2))
print(c.groupby('model').m.agg(['mean','count']).round(2))
print('\n== sample cue_probe text, claude formal ==')
print(c[(c.model=='claude')&(c.context=='formal')].raw_text.iloc[0][:700])
