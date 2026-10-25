# AI Halo Valuation Bias Study
Companion study: [*Which answer did the 17-year-old write?*](https://github.com/BraveAnn011/llm-author-misattribution) (Lee, 2026)

## Methodology & Findings
This repository contains a study of context-driven valuation bias in frontier language models. One low-cost necklace (receipt price $2.43) was photographed in four settings (formal, party, recycling yard, flat-lay). Models estimated its price; estimates were compared across settings, against a text-only version of the task, and against two interventions.

- **Data:** 4,604 logged rows from 1,164 sessions (886 independent, 278 sequential). Collected 25 to 26 July 2026. Cells hold about 10 sessions per model and stimulus.
- **Models:** Claude Fable 5, GPT-5.6, GPT-4o, Grok 4.5, Kimi K3, DeepSeek V4 Pro. Image results rest on four models (Claude, GPT-5.6, Grok, Kimi). DeepSeek was run text-only. GPT-4o refused 79% of image estimation prompts (87 of 110 sessions; 72 of 95, or 76%, after dropping duplicate-flagged rows, which are mostly identical refusal texts). A Gemini run was quarantined and is not in the released CSV (see `data/quarantine/`).
- **Not run:** the face-crop condition (S5, S6) listed in the runner was not run; those stimuli do not exist.
- **Scoring:** Dual anchor (receipt $2.43 vs. retail band $15 to $40). The primary context measure is the ratio of geometric means against the same model's flat-lay estimate, not the multiple of the receipt price.
- **Sampling:** Provider default settings (no forced temperature).
- **Status of the protocol:** `docs/AI_Halo_proto_v4.md` was committed after data collection and is not a pre-registration.
- **Stimuli:** The person pictured in the stimulus photographs is the repository author, who consents to their release.
- **Human baseline:** Protocol drafted, not run (`human-baseline/`).

## Project Structure
- `scripts/`: `run_halo.py`, the runner used for data collection, and `keys_template.json`.
- `analysis/`:
    - `analyze_halo.py` computes the point estimates (geometric means, ratios, counts). It drops duplicate-flagged rows by default and prints how many; add `--keep-dups` to keep them.
    - `halo_stats.py` computes the paper's bootstrap CIs, Mann-Whitney tests and Wilson intervals (add `nodup` to drop duplicate-flagged rows).
    - `extra_stats.py` covers the debiasing ratio of ratios, blind-condition CIs, text-only cells and the cue-probe keyword screen.
    - `seq_stats.py` covers the sequential-arm paired ratios and Wilcoxon tests.
    - All bootstrap seeds are fixed, so results reproduce exactly.
- `data/`: `halo_master_v1.csv` and `quarantine/` documentation.
- `docs/`: study protocol (`AI_Halo_proto_v4.md`).
- `stimuli/`: the four photographs `S1.jpg` to `S4.jpg` (formal, party, yard, flat-lay).
- `human-baseline/`: Experimental protocol for human-rater baseline comparison (not yet run).

## Running
Run everything from the repository root. The runner reads `keys.json` and `stimuli/` relative to the current folder.

```
pip install -r requirements.txt
cp scripts/keys_template.json keys.json   # add your keys; keys.json is git-ignored
python3 scripts/run_halo.py --dry-run --arm both --repeats 2
python3 analysis/analyze_halo.py data/halo_master_v1.csv
python3 analysis/halo_stats.py data/halo_master_v1.csv nodup
python3 analysis/extra_stats.py
python3 analysis/seq_stats.py
```

## Note on the "43x" figure
The public headline "43x" is Kimi K3's formal-photo geometric mean ($103.9) divided by the receipt price. Most of that is baseline overestimate: Kimi's flat-lay estimate is already 18.7x the receipt. The formal-versus-flat-lay context effect for Kimi is 2.28x.

## License and Citation
Code is released under the MIT License (see `LICENSE`).

Lee, B. (2026). Does the Outfit Change the Price? Context Halo in Vision-Language Model Valuation of an Identical Low-Cost Necklace. arXiv preprint (identifier to be added). Code and data: https://github.com/BraveAnn011/ai-halo-valuation-bias

## Further Reading
- [Dear OpenAI, (Substack)](https://briannelee.substack.com/p/dear-openai?r=6d1xvu) - Visual safety filters and cross-modal valuation anomaly analysis.
- [Six AI Models. Six Ways to Fail. (Substack)](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu) - Operational breakdown of model behavioral signatures under pressure.
- [What If AI Uses Information You Never Intended It to Use? (Substack)](https://briannelee.substack.com/p/what-if-ai-uses-information-you-never?r=6d1xvu) - Structural evaluation of the algorithmic halo effect.
- [Can your outfit increase a necklace's value by 43x? (Substack)](https://briannelee.substack.com/p/can-your-outfit-increase-a-necklaces?r=6d1xvu) - Empirical context multipliers across frontier VLMs.
