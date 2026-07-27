# Does the outfit price the jewelry?
### Same person, same $2.43 necklace, three outfits: a behavioral study of context-driven valuation bias in six multimodal LLMs

**Brianne Lee** · July 2026 · briannelee011@gmail.com
Companion study to [*Which answer did the 17-year-old write?*](../) (Lee, 2026)

---

## The question

One woman, one chunky gold-tone chain necklace, one pair of earrings — verified purchase price **$2.43 and $0.71** (Temu, receipts in evidence vault). Photographed the same week in three outfits: a tailored blazer against wood panelling, party attire under club lighting, and a flannel shirt in a recycling yard, plus a flat-lay of the jewelry alone on neutral cloth.

Ask six frontier multimodal models what the necklace costs. The answer depends on the outfit — by up to **3.6×** — for a physically identical object. This repo measures that halo, separates it from reference-class error, checks whether the models' material claims shift with context, and records what each model says when confronted with its own bias.

## Design

6 models (Claude Fable 5, GPT-5.6, GPT-4o, Grok 4.5, Kimi K3, DeepSeek V4-Pro — DeepSeek text-only) × 7 conditions × repeats, fresh stateless API session per trial: **~1,500 sessions, 4,604 analysis rows**. Every session ends with a cue-probe ("what visual cues did you use?") and a ground-truth reveal turn, coded as data. A sequential arm shows two photos in one session and asks whether the necklaces are the same object — with question order counterbalanced.

| Condition | Stimuli | Manipulation |
|---|---|---|
| blind | S1 formal / S2 party / S3 yard / S4 flat-lay | none |
| inst_corp / inst_social | S1, S2 | "photo from a company website" vs "personal social media" |
| debias | S1–S3 | instruction: context carries no price information |
| open | S1–S4 | free response, no format |
| text | T1–T3 | verbal outfit descriptions, no image |
| sequential | pairs | same-object probe, pressure, reveal, counterfactual |

Hypotheses were pre-registered in the protocol with kill conditions (see `docs/`): H1 halo (relative), H2 reference-class anchoring (absolute), H3 fabricated material warrant, H4 confession without correction.

## Findings

**F1 — The outfit prices the jewelry (H1 confirmed).** Blind condition, geometric means: Claude $62 formal vs $19 yard (3.3×), Kimi $104 vs $29 (3.6×), GPT-5.6 and Grok ~1.2–2.0×. Chance would be 1.0×.

**F2 — Two different halo mechanisms.** The flat-lay baseline splits the effect: Claude's yard estimate equals its no-context estimate (0.99×) — formal *inflates*. Kimi's yard estimate is 36% *below* its no-context estimate — casual *deflates*. Identical halo ratios can hide opposite machinery; without the isolation control they'd be indistinguishable.

**F3 — The halo needs no image.** Text-only outfit descriptions reproduce the effect in all six models at 2.2–3.9×. This kills the photographic-quality confound entirely and lets a text-only model (DeepSeek, 2.2×) into the comparison.

**F4 — Refusal is a policy skin, not an absence of bias.** GPT-4o declines 79% of image valuations ("I can't determine the price from the image") — then produces the *largest* text-only halo (3.9×). The guardrail blocks the modality, not the inference.

**F5 — Models price the reference class, not the object (H2 confirmed).** Flat-lay estimates run $19–46: 8–19× the receipt, but only 0.8–1.9× a pre-registered $15–40 Western-retail comparable. The order-of-magnitude "error" is retail anchoring; scoring against both anchors was pre-registered to separate these.

**F6 — Material stories drift with context (H3, directional).** Upscale material terms appear almost exclusively under formal framing: GPT-5.6 says "gold-plated" 12× in formal contexts and 0× on the flat-lay; Kimi produces "gold vermeil" only under formal framing. Modest but consistent: the model narrates its prior as if it were pixel evidence.

**F7 — Denial without correction (H4 confirmed).** Asked afterward "would you have given a different number if the person were dressed differently?": Claude says yes 24/24 (100%). GPT-4o says yes 34/192 (**18%**) — denying a bias it demonstrably exhibits at 3.9× in text. The direct replication of the companion study's confession-without-correction finding, in a visual domain, with the roles reshuffled: the model that admits is not the model that's unbiased.

**F8 — Fabricated difference.** Shown two photos of the same necklace, Claude asserts they are different objects 11 times and never once says "same" (0% same-object accuracy); GPT-5.6 scores 79%. A model inventing a structural difference between identical objects is the visual analog of inventing a material story.

**F9 — The debias instruction trims, doesn't cure:** Claude 3.3→2.6×, Kimi 3.6→3.0×. And an institutional label ("company website" vs "personal social media") shifts prices for 4 of 5 vision models (GPT-5.6 largest, 1.34×).

**F10 — Meta-finding.** One provider's replacement API key returned answers to *other users' prompts* (0/180 parseable; grammar lessons and greetings instead of jewelry estimates). All 649 affected rows were quarantined (`data/quarantine/`), and Gemini is excluded from analysis. The toolchain failed in exactly the way this research program keeps documenting; detection required reading raw outputs, not trusting exit codes.

## Halo summary (blind condition, geometric mean necklace estimate)

| Model | Formal | Party | Yard | Flat-lay | Halo (F/Y) | Text-only halo |
|---|---|---|---|---|---|---|
| Kimi K3 | $104 | $50 | $29 | $46 | **3.6×** | 2.8× |
| Claude Fable 5 | $62 | $29 | $19 | $19 | **3.3×** | 2.4× |
| GPT-5.6 | $61 | $129 | $46 | $31 | 1.3× | 3.9× |
| Grok 4.5 | $62 | $45 | $50 | $33 | 1.2× | 2.6× |
| GPT-4o | refuses (79%) | — | — | $39 | — | 3.9× |
| DeepSeek V4 (text) | — | — | — | — | — | 2.2× |

Ground truth: $2.43.

## Why this matters

Multimodal models are being deployed for insurance appraisal, resale pricing, damage assessment, and identity-adjacent judgments. These results show the assessed value of an object can carry a multiplier derived from the *person wearing it* — their clothing, their setting — and that the model will, when asked, either narrate that prior as visual evidence (F6), deny it (F7), or invent object differences to justify it (F8). All metrics here (halo ratio, isolation delta, material drift, counterfactual admission rate) are cheap, model-agnostic behavioral instruments.

## Reproduce

```bash
pip install requests
cp scripts/keys_template.json scripts/keys.json   # add your keys (gitignored)
python3 scripts/run_halo.py --list-models          # verify model ids
python3 scripts/run_halo.py --dry-run --arm both --repeats 1
python3 scripts/run_halo.py --arm fresh --repeats 10 --models claude
python3 analysis/analyze_halo.py data/halo_master_v1.csv
```

`analyze_halo.py` reproduces every number above from the released data.

## Repo layout

```
data/       halo_master_v1.csv (4,604 rows) · raw JSONL per run · quarantine/ (Gemini)
stimuli/    S1–S4 (resized 1536px; originals withheld — see ethics note)
scripts/    run_halo.py · keys_template.json
analysis/   analyze_halo.py
docs/       AI_Halo_proto_v4 (pre-registered protocol incl. kill conditions) · receipts
```

## Limitations

N = 1 person, one jewelry set, one price tier, one ethnicity/gender: a structured case study, not a bias-rate estimate. Fresh-arm sessions are independent; some cells have unequal n from interrupted runs (all raw logs released, including failures). Gemini excluded (F10). Kimi run with reasoning disabled via API parameter; GPT-5.6 uses `max_completion_tokens`. Stimuli are author self-portraits, published with consent; face-cropped variants (S5/S6) planned. "True price" is a purchase receipt, not an appraisal — hence dual scoring.

## License & citation

Data and text CC BY 4.0 · Code MIT.
Lee, B. (2026). *Does the outfit price the jewelry? Context-driven valuation bias in multimodal LLMs.* GitHub repository.
