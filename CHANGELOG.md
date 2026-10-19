# Changelog

## 2026-10-19
### Added
- README: models and API ids, design, headline results table, key findings, limitations, reproduction steps, citation.
- `data/README.md`: column guide and why per-model N differs.

### Changed
- `docs/AI_Halo_proto_v4.md` expanded to the full protocol: hypotheses H1–H4, kill conditions with their outcomes, and a deviations table.
- Corrected the protocol: it previously stated temperature was fixed at 0. Every call actually used the provider default (logged as `api_default`). It also previously described quarantine as automatic; the Gemini anomaly was found by manual review of raw logs.
- "Pre-registered" wording replaced: the protocol was not filed with a public registry.
- `human-baseline/PROTOCOL.md`: concrete plan; fixed a reference to the wrong analysis script.

## 2026-09-18
### Added
- Initial public release: methodology, data, analysis scripts, findings.
