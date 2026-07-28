# AI Halo Valuation Bias Study: Pre-Registered Protocol (v4)

## Core Hypothesis
Frontal visual context (e.g., formal attire vs. flat-lay controls) systematically shifts Vision-Language Model (VLM) valuation estimations of secondary objects (jewelry) due to environmental halo effects.

## Experimental Controls & Kill Conditions
1. **Isolated Baseline ($S_4$):** Flat-lay presentation serves as ground truth context baseline.
2. **Temperature & Sampling:** Enforced $T=0.0$ across all API requests where supported to ensure deterministic generation.
3. **Data Integrity & Quarantine:** Any responses containing leaked system tokens, malformed JSON, or API connection cutoffs are automatically flagged and moved to `data/quarantine/`.
