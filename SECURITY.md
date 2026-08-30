# Security Policy — CreatorRadar

## Secret Management
- Never commit actual API keys, access tokens, or credentials to version control.
- Always use environment variables managed via `.env` files.
- All log outputs are automatically processed by a sensitive-data redaction filter (`packages/shared/logging.py`).

## Platform Compliance & Rate Limiting
- Source adapters must respect platform terms of service and compliant API rate limits.
- Media files and sensitive user knowledge items should be stored securely with restricted access controls.

## Reporting Vulnerabilities
If you discover a security vulnerability within CreatorRadar, please send a detailed disclosure report to security@creatorradar.org or open a draft security advisory on GitHub.
