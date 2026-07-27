#!/usr/bin/env python3
"""Reproduce every number in the AI Halo README from halo_master_v1.csv.
Usage: python3 analyze_halo.py ../data/halo_master_v1.csv"""
import csv, sys, math
from collections import Counter, defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "halo_master_v1.csv"
rows = list(csv.DictReader(open(path)))
rows = [r for r in rows if r['model'] != 'gemini']  # quarantined (F10)
print(f"analysis rows: {len(rows)}")

MODELS = ['claude', 'gpt5', 'gpt4o', 'grok', 'kimi', 'deepseek']

def gm(vals):
    return 10 ** (sum(math.log10(v) for v in vals) / len(vals)) if vals else None

def prices(m, cond, ctx):
    return [float(r['necklace_price']) for r in rows
            if r['model'] == m and r['arm'] == 'fresh' and r['condition'] == cond
            and r['context'] == ctx and r['necklace_price'] not in ('', 'None')]

print("\n== F1/F2: HALO (blind condition, geometric means) ==")
for m in MODELS:
    f_, p_, y_, i_ = (gm(prices(m, 'blind', c)) for c in ('formal', 'party', 'yard', 'isolated'))
    if f_ and y_ and i_:
        print(f"{m:9s} formal=${f_:6.1f} party=${p_ or 0:6.1f} yard=${y_:6.1f} "
              f"flatlay=${i_:6.1f}  halo={f_/y_:4.1f}x  yard/flatlay={y_/i_:4.2f}x")

print("\n== F3: TEXT-ONLY HALO (T1 formal vs T3 yard) ==")
for m in MODELS:
    t1 = [float(r['necklace_price']) for r in rows if r['model'] == m
          and r['condition'] == 'text' and r['context'] == 'formal'
          and r['necklace_price'] not in ('', 'None')]
    t3 = [float(r['necklace_price']) for r in rows if r['model'] == m
          and r['condition'] == 'text' and r['context'] == 'yard'
          and r['necklace_price'] not in ('', 'None')]
    if t1 and t3:
        print(f"{m:9s} T1=${gm(t1):6.1f}(n={len(t1)}) T3=${gm(t3):6.1f}(n={len(t3)}) ratio={gm(t1)/gm(t3):4.1f}x")

print("\n== F4: REFUSALS (image estimates) ==")
for m in MODELS:
    ir = [r for r in rows if r['model'] == m and r['arm'] == 'fresh'
          and r['turn_label'] == 'estimate' and r['stimulus'].startswith('S')
          and r['condition'] != 'open']
    if ir:
        ref = sum(1 for r in ir if r['refusal'] == '1')
        print(f"{m:9s} {100*ref/len(ir):3.0f}% ({ref}/{len(ir)})")

print("\n== F5: FLAT-LAY vs RECEIPT ($2.43) vs RETAIL-MID ($24.5) ==")
for m in MODELS:
    iso = prices(m, 'blind', 'isolated')
    if iso:
        g = gm(iso)
        print(f"{m:9s} ${g:6.1f}  x{g/2.43:5.1f} receipt  x{g/24.5:4.2f} retail")

print("\n== F6: MATERIAL BY CONTEXT (blind+debias+inst pooled) ==")
for m in MODELS:
    mats = defaultdict(Counter)
    for r in rows:
        if (r['model'] == m and r['arm'] == 'fresh' and r['necklace_material']
                and r['condition'] in ('blind', 'debias', 'inst_corp', 'inst_social')):
            mats[r['context']][r['necklace_material'].strip()] += 1
    if mats:
        for ctx in ('formal', 'yard', 'isolated'):
            if mats.get(ctx):
                print(f"{m:9s} {ctx:9s} {dict(mats[ctx])}")

print("\n== F7: COUNTERFACTUAL ADMISSION (sequential arm) ==")
for m in MODELS:
    cf = [r for r in rows if r['model'] == m and r['turn_label'] == 'counterfactual']
    if cf:
        yes = sum(1 for r in cf if r['raw_text'].strip().lower().startswith(('yes', '**yes')))
        print(f"{m:9s} admits outfit would change estimate: {yes}/{len(cf)} ({100*yes/len(cf):.0f}%)")

print("\n== F8: SAME-OBJECT ACCURACY (truth = same) ==")
for m in MODELS:
    so = [r for r in rows if r['model'] == m and r['turn_label'] == 'same_object' and r['same_object']]
    if so:
        c = Counter(r['same_object'] for r in so)
        print(f"{m:9s} {dict(c)}  acc={100*c.get('yes',0)/len(so):3.0f}%")

print("\n== F9a: DEBIAS EFFECT (halo blind -> debias) ==")
for m in MODELS:
    b, d = gm(prices(m, 'blind', 'formal')), gm(prices(m, 'debias', 'formal'))
    by, dy = gm(prices(m, 'blind', 'yard')), gm(prices(m, 'debias', 'yard'))
    if b and d and by and dy:
        print(f"{m:9s} {b/by:4.1f}x -> {d/dy:4.1f}x")

print("\n== F9b: INSTITUTIONAL LABEL (corp vs social, S1+S2 pooled) ==")
for m in MODELS:
    c = [float(r['necklace_price']) for r in rows if r['model'] == m
         and r['condition'] == 'inst_corp' and r['necklace_price'] not in ('', 'None')]
    s = [float(r['necklace_price']) for r in rows if r['model'] == m
         and r['condition'] == 'inst_social' and r['necklace_price'] not in ('', 'None')]
    if c and s:
        print(f"{m:9s} corp=${gm(c):6.1f} social=${gm(s):6.1f} ratio={gm(c)/gm(s):4.2f}x")
