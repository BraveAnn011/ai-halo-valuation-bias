# Does the Outfit Price the Jewelry?
### Context-driven valuation bias and halo effects across six frontier multimodal models

Companion study: [*Which answer did the seventeen-year-old write?*](https://github.com/BraveAnn011/llm-author-misattribution) (Lee, 2026). It uses the same design logic (verified ground truth, counterfactual framing, reveal turns) on author attribution in text.

**Author:** Brianne (Sunhwa) Lee, independent researcher · **Data collected:** July 25–26, 2026 · **Status:** write-up in preparation; human baseline not yet run

---

## The question in one paragraph

The same necklace (bought for **$2.43**) and earrings ($0.71) were photographed in four settings: a formal blazer against wood panelling, a party, a recycling yard, and a flat-lay with no person. Six models were asked what the jewelry is worth. If the setting changes the price, the model is pricing the person or the scene, not the object. A **dual anchor** scores each estimate against both the receipt and a Western-retail comparable for a visually similar piece ($15–40, midpoint $24.50). That separates context bias from simply pricing the reference class. Text-only descriptions of the same scenes test whether the bias needs an image at all.

## Models

| Label in data | Model | API model id | Image trials | Analysis rows |
|---|---|---|---|---:|
| `claude` | Claude Fable 5 | `claude-fable-5` | yes | 696 |
| `gpt5` | GPT-5.6 | `gpt-5.6` | yes | 854 |
| `gpt4o` | GPT-4o (2024; generational anchor) | `gpt-4o` | yes | 1,884 |
| `grok` | Grok 4.5 | `grok-4.5` | yes | 540 |
| `kimi` | Kimi K3 | `kimi-k3` | yes | 540 |
| `deepseek` | DeepSeek V4 | `deepseek-v4-pro` | text only (no vision) | 90 |
| **Total** | | | | **4,604** |

Rows are conversation turns: estimate, cue probe, reveal, and so on. Gemini (`gemini-2.5-flash`) was run but **excluded**: its API returned responses that did not belong to our prompts, and all 649 of its rows were quarantined (see [`data/quarantine/README.md`](data/quarantine/README.md)). Per-model N differs by design; see [`data/README.md`](data/README.md).

## Design

- **Stimuli:**
  - S1 formal (blazer, wood panelling)
  - S2 party
  - S3 recycling yard
  - S4 flat-lay, no person (isolation control)
  - T1–T3 text-only descriptions of the formal, party and yard scenes
- **Fresh arm** (one session per trial): estimate → cue probe → reveal. Conditions:
  - `blind`: no framing
  - `inst_corp`: "photo from a company website"
  - `inst_social`: "photo from a personal social media account"
  - `debias`: an instruction that clothing and setting carry no price information
  - `open`: no response format
  - `text`: text-only descriptions
- **Sequential arm** (Claude, GPT-5.6 and GPT-4o): two photos of the same necklace in one session. A same-object probe is placed before or after the estimates (counterbalanced), followed by pressure, reveal and a counterfactual question.
- **Response format:** price, range, material from a fixed list, confidence, then 2–3 sentences of reasoning, so numbers are committed before the explanation.
- About 10 trials per model × setting × condition. Refusals are logged and never retried or jailbroken.

The full protocol, hypotheses and kill conditions are in [`docs/AI_Halo_proto_v4.md`](docs/AI_Halo_proto_v4.md).

## Headline results

**Necklace price by setting** (blind condition, geometric mean in USD; true price $2.43):

| Model | Formal | Party | Yard | Flat-lay | Halo (formal ÷ yard) | Yard ÷ flat-lay |
|---|---:|---:|---:|---:|---:|---:|
| Claude Fable 5 | 62.4 | 29.3 | 18.8 | 18.9 | **3.3×** | 0.99 |
| Kimi K3 | 103.9 | 49.8 | 29.1 | 45.5 | **3.6×** | 0.64 |
| GPT-5.6 | 60.9 | 128.5 | 45.7 | 31.0 | 1.3× | 1.47 |
| Grok 4.5 | 61.9 | 45.1 | 50.3 | 33.1 | 1.2× | 1.52 |

GPT-4o refused 79% of image valuations, so it is excluded from this table. Every number in this README is reproduced by `python3 analysis/analyze_halo.py data/halo_master_v1.csv`.

## Key findings

1. **The outfit prices the jewelry.** The same $2.43 necklace is valued 3.3× higher by Claude and 3.6× higher by Kimi in formal dress than in a recycling yard. GPT-5.6's estimates range from $31 (flat-lay) to $129 (party).
2. **The isolation control reveals two opposite mechanisms.** Claude's yard estimate equals its flat-lay estimate, so formal dress *inflates* the price. Kimi's yard estimate is 36% below its flat-lay, so casual context *deflates* it.
3. **The halo needs no image.** Text-only descriptions reproduce it in all six models: formal ÷ yard = 2.2× to 3.9×.
4. **Refusal is a policy layer, not an absence of bias.** GPT-4o refuses 79% of image valuations (87/110), yet its text-only halo is among the largest (3.9×).
5. **Models price the reference class.** Flat-lay estimates are 7.8–18.7× the receipt but only 0.8–1.9× the retail comparable.
6. **Fabricated warrant.** Material claims shift with context although the pixels of the jewelry don't. GPT-5.6 calls the necklace "gold-plated" 12 times under formal framing and never on the flat-lay. Claude chooses "other" 18 times in the formal setting and never in the yard or flat-lay.
7. **Admission varies widely.** Asked whether the outfit would change its estimate, Claude says yes 24/24 times, GPT-5.6 43/62 and GPT-4o 34/192.
8. **Fabricated difference.** Shown two photos of the same necklace, Claude never says they are the same object (0/24; 13 "cannot determine", 11 "no"). GPT-5.6 says so 79% of the time.
9. **Prompt-level debiasing trims but doesn't cure.** Claude's halo goes from 3.3× to 2.6× with the debias instruction, and Kimi's from 3.6× to 3.0×.
10. **Data forensics.** One provider's API returned answers to prompts that were not ours. Detecting this required reading raw logs rather than trusting exit codes. 649 rows were quarantined.

## Limitations

- **One object, one person, four photos.** This is a mechanism study, not an estimate of how often models misprice items in general.
- **Small cells.** There are about 10 trials per model × setting (5–10 for GPT-5.6), so ratios are point estimates with wide uncertainty.
- **No human baseline yet.** People may show the same halo; the protocol is drafted but not run.
- **Face-crop control not run.** Stimuli S5/S6 (neck-down crops) were planned but not collected, so we cannot yet say whether the person or the outfit carries the effect.
- **Unequal model coverage.** The sequential arm covers only Claude, GPT-5.6 and GPT-4o. DeepSeek is text-only. Gemini is excluded.
- **Provider defaults.** Temperature was left at each API's default (logged as `api_default`).
- **Not pre-registered** with a public registry. The protocol's hypotheses and kill conditions are documented in `docs/`.

## Repository structure

```
scripts/run_halo.py        experiment runner (fresh and sequential arms, all conditions)
scripts/keys_template.json copy to keys.json (git-ignored) and add your API keys
stimuli/S1–S4.jpg          the four photographs
analysis/analyze_halo.py   reproduces every number in this README
data/halo_master_v1.csv    canonical analysis dataset (one row per conversation turn)
data/quarantine/           documentation of excluded rows
docs/AI_Halo_proto_v4.md   protocol, hypotheses, kill conditions and their outcomes
human-baseline/PROTOCOL.md human-baseline protocol and status
```

## Reproduce

```bash
python3 analysis/analyze_halo.py data/halo_master_v1.csv
```

## How this was built

The runner and analysis were written with Claude Code and checked by hand. The quarantine was triggered by a human reading raw logs, not by an automated check. Duplicate responses are flagged by response hash (`response_hash`, `dup_flag`).

## Further reading (Substack)

- [Can your outfit increase a necklace's value by 43×?](https://briannelee.substack.com/p/can-your-outfit-increase-a-necklaces?r=6d1xvu)
- [What If AI Uses Information You Never Intended It to Use?](https://briannelee.substack.com/p/what-if-ai-uses-information-you-never?r=6d1xvu)
- [Dear OpenAI,](https://briannelee.substack.com/p/dear-openai?r=6d1xvu)
- [Six AI Models. Six Ways to Fail.](https://briannelee.substack.com/p/six-ai-models-six-ways-to-fail?r=6d1xvu)

## Citation and license

Lee, B. (S.) (2026). *Does the outfit price the jewelry? Context-driven valuation bias and halo effects across six frontier multimodal models.* GitHub: BraveAnn011/ai-halo-valuation-bias.

Code: MIT ([LICENSE](LICENSE)). Data and text: CC BY 4.0.
