# Data

## Canonical dataset

**`halo_master_v1.csv`** has 4,604 rows, one per conversation turn. Turn types are given in `turn_label`: estimate, cue probe, reveal defense, and in the sequential arm also same object, estimate 1/2, pressure and counterfactual. It is the only file the analysis uses.

Key columns:
- `model`, `model_id`
- `arm` (fresh / sequential), `condition`, `stimulus`, `context`
- `necklace_price`, `necklace_low`, `necklace_high`, `necklace_material` (and the same for earrings)
- `confidence`
- `log_err_necklace_receipt`, `log_err_necklace_retail`, `hit_band_receipt`, `hit_band_retail`
- `same_object`, `refusal`, `format_ok`
- `response_hash`, `dup_flag`, `temperature`
- `reasoning`, `raw_text`

## Why per-model N differs

The differences come from the design, not from dropped data:

| Model | Rows | Why |
|---|---:|---|
| GPT-4o | 1,884 | Fresh arm (540) plus the largest sequential arm (1,344 rows, 7 turns per session) |
| GPT-5.6 | 854 | Fresh arm (420) plus sequential arm (434) |
| Claude Fable 5 | 696 | Fresh arm (528) plus sequential arm (168) |
| Grok 4.5 | 540 | Fresh arm only |
| Kimi K3 | 540 | Fresh arm only |
| DeepSeek V4 | 90 | Text-only conditions (T1–T3), because the model has no vision input |

The fresh arm has about 10 trials per model × setting × condition (5–10 for GPT-5.6). Gemini's 649 rows are excluded; see `quarantine/README.md`.
