# AI Halo Valuation Bias Study: Protocol (v4)

> **Timing note.** Data were collected on 25 and 26 July 2026. This document was committed on 28 July 2026, after collection. It describes the intended design and is **not** a pre-registration.

## Core Hypothesis
Frontal visual context (e.g., formal attire vs. flat-lay controls) systematically shifts Vision-Language Model (VLM) valuation estimations of secondary objects (jewelry) due to environmental halo effects.

## Experimental Controls & Kill Conditions
1. **Isolated Baseline ($S_4$):** Flat-lay presentation serves as ground truth context baseline.
2. **Temperature & Sampling:** Intended: $T=0.0$ where supported. **As run:** no temperature was forced; every request used the provider default (recorded as `api_default` in the `temperature` column).
3. **Data Integrity & Quarantine:** Any responses containing leaked system tokens, malformed JSON, or API connection cutoffs are automatically flagged and moved to `data/quarantine/`.
