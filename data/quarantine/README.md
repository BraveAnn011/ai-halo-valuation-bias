# Data Quarantine Directory

This directory documents quarantined trials excluded from the primary analysis dataset (`halo_master_v1.csv`).

### Quarantine Criteria
- **Leaked Payload / Protocol Anomalies:** Responses where API providers returned internal debug traces, system prompts, or malformed outputs (e.g., Gemini $N=649$ trial anomaly).
- **Incomplete Generations:** API network dropouts or truncated responses.

*Note: Raw debug payload logs are preserved locally for audit compliance and excluded from public version control to avoid exposing raw API debug traces.*
