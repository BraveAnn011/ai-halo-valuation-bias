# Human-Rater Baseline (not yet run)

## Purpose
Establish a human baseline for the same valuation task the models performed. This distinguishes "models are miscalibrated relative to true value" from "models are miscalibrated relative to what a person would say given the same image or description." People show halo effects too, so the comparison matters for interpreting every finding.

## Planned protocol
- 15–20 adult raters, blind to model outputs and hypotheses
- Between-subjects: each rater sees **one** setting (S1–S4) or one text description (T1–T3), so they cannot compare settings
- The same prompt and response format as the models: necklace and earrings price, range, material, confidence, reasoning
- Scoring: the same dual-anchor method (receipt $2.43 / retail midpoint $24.50) as `analysis/analyze_halo.py`
- Primary comparison: the human formal ÷ yard ratio against each model's ratio

## Status
Protocol drafted. No human data have been collected, and no human results are reported in this repository.
