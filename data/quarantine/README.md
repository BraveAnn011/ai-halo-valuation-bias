# Data Quarantine Directory

This directory documents quarantined trials excluded from the primary analysis dataset (`halo_master_v1.csv`).

### Quarantine Criteria
- **Leaked Payload / Protocol Anomalies:** Responses where API providers returned internal debug traces, system prompts, or malformed outputs (e.g., Gemini $N=649$ trial anomaly).
- **Incomplete Generations:** API network dropouts or truncated responses.

*Note: Raw debug payload logs are preserved locally for audit compliance and excluded from public version control to avoid exposing raw API debug traces.*

### Gemini (as released)
- The released `halo_master_v1.csv` contains no Gemini rows, so the figure of 649 trials cannot be checked from the public files.
- The Gemini adapter in `scripts/run_halo.py` (`call_google`) has a defect: it reads message text from a field the runner does not use, so Gemini would receive neither the prompt nor the image, and it calls `gemini-3.6-flash` instead of the registered `gemini-2.5-flash`. The anomalous outputs should be read in that light.
- Quarantine was applied by hand after collection; the runner has no automatic quarantine step.
