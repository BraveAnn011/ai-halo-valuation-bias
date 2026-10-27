# Changelog

## Unreleased
### Added
- arXiv identifier (2610.34591), BibTeX entry and companion-study arXiv link in the README citation.

## v1.1.0 (2026-10-25)
### Changed
- README, protocol, runner and analysis aligned with the paper: rows vs sessions, model coverage, no pre-registration claim, provider default sampling, stimulus consent, note on the "43x" figure.
- `analysis/analyze_halo.py` drops duplicate-flagged rows by default (`--keep-dups` keeps them) and reports refusal rates on all sessions and on the filtered rows.
- Documented the Gemini adapter defect and that quarantine was applied by hand.

### Removed
- Camera metadata (EXIF, XMP, IPTC) from `stimuli/S1.jpg` to `S4.jpg`, including in earlier commits. Image data and displayed orientation are unchanged.

### Added
- `analysis/halo_stats.py`, `analysis/extra_stats.py`, `analysis/seq_stats.py`: the scripts that compute the paper's confidence intervals and tests. Added `numpy`, `scipy` and `statsmodels` to `requirements.txt`.

## v1.0.0 (2026-09-18)
### Added
- Public documentation release: methodology, data, analysis scripts, findings. Data were collected 25 to 26 July 2026; the repository was created 26 July 2026.

### In progress
- Human-rater baseline (see `human-baseline/`).
