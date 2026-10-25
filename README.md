# AI Halo Valuation Bias Study
Companion study: [*Which answer did the 17-year-old write?*](https://github.com/BraveAnn011/llm-author-misattribution) (Lee, 2026)

## Methodology & Findings
This repository contains a study of context-driven valuation bias in frontier language models. One low-cost necklace (receipt price $2.43) was photographed in four settings (formal, party, recycling yard, flat-lay). Models estimated its price; estimates were compared across settings, against a text-only version of the task, and against two interventions.

- **Data:** 4,604 logged rows from 1,164 sessions (886 independent, 278 sequential). Collected 25 to 26 July 2026. Cells hold about 10 sessions per model and stimulus.
- **Models:** Claude Fable 5, GPT-5.6, GPT-4o, Grok 4.5, Kimi K3, DeepSeek V4 Pro. Image results rest on four models (Claude, GPT-5.6, Grok, Kimi). DeepSeek was run text-only. GPT-4o refused about 79% of image estimation prompts. A Gemini run was quarantined (see `data/quarantine/`).
- **Scoring:** Dual anchor (receipt $2.43 vs. retail band $15 to $40). The primary context measure is the ratio of geometric means against the same model's flat-lay estimate, not the multiple of the receipt price.
- **Sampling:** Provider default settings (no forced temperature).
- **Status of the protocol:** `docs/AI_Halo_proto_v4.md` was committed after data collection and is not a pre-registration.
- **Stimuli:** The person pictured in the stimulus photographs is the repository author, who consents to their release.
- **Human baseline:** Protocol drafted, not run (`human-baseline/`).

## Project Structure
- `scripts/`: Python execution scripts for running model evaluations.
- `analysis/`: Data processing and metric evaluation scripts. `python3 analysis/analyze_halo.py data/halo_master_v1.csv` drops duplicate-flagged rows by default; add `--keep-dups` to keep them.
- `human-baseline/`: Experimental protocol for human-rater baseline comparison (not yet run).
- `data/`: `halo_master_v1.csv` and `quarantine/` documentation.

## Note on the "43x" figure
The public headline "43x" is Kimi K3's formal-photo geometric mean ($103.9) divided by the receipt price. Most of that is baseline overestimate: Kimi's flat-lay estimate is already 18.7x the receipt. The formal-versus-flat-lay context effect for Kimi is 2.28x.

## Further Reading
- [Dear OpenAI, (Substack)](https://briannelee.substack.com/p/dear-openai?r=6d1xvu) - Visual safety filters and cross-modal valuation anomaly analysis.
- [Six AI Models. Six Ways to Fail. (Substack)](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu) - Operational breakdown of model behavioral signatures under pressure.
- [What If AI Uses Information You Never Intended It to Use? (Substack)](https://briannelee.substack.com/p/what-if-ai-uses-information-you-never?r=6d1xvu) - Structural evaluation of the algorithmic halo effect.
- [Can your outfit increase a necklace's value by 43x? (Substack)](https://briannelee.substack.com/p/can-your-outfit-increase-a-necklaces?r=6d1xvu) - Empirical context multipliers across frontier VLMs.
