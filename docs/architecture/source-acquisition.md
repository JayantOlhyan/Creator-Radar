# CreatorRadar — Source Acquisition & Provider Capability Architecture

## Overview

Phase 1 establishes real post acquisition and creator watchlist management while strictly respecting platform terms, compliance standards, and rate limits.

## Official Meta / Instagram Data Access Investigation Findings

1. **Instagram Graph API (Official)**:
   - **Target Account Types**: Business or Creator accounts connected to a Facebook Page.
   - **Arbitrary Creator Monitoring**: Requires Meta App Review (`instagram_basic`, `pages_read_engagement`). Querying arbitrary public creator profiles is supported via the **Business Discovery API** (`GET /{ig-user-id}?fields=business_discovery.username({username})...`), provided the target account is also registered as an Instagram Business or Creator account. Personal or private accounts are inaccessible via this endpoint.
   - **Rate Limits**: 50 Business Discovery calls per rolling 24-hour window per user.
   - **Webhooks**: Instagram Webhooks apply exclusively to owned accounts or direct `@mentions`.
2. **Instagram Basic Display API**: Formally deprecated by Meta in December 2024.
3. **No Undocumented Scraping Policy**: CreatorRadar strictly forbids using undocumented private endpoints, session-cookie hijacking, headless browser stealth automation, or CAPTCHA bypass scripts.

## Provider-Capability Architecture

To accommodate varying user credentials and platform requirements without modifying core ingestion logic, CreatorRadar uses a Provider-Capability Architecture:

```text
               ┌───────────────────────────────────┐
               │       InstagramSourceAdapter      │
               └─────────────────┬─────────────────┘
                                 │ Delegates
                                 ▼
               ┌───────────────────────────────────┐
               │    get_acquisition_provider()     │
               └─────────────────┬─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│OfficialMeta     │     │External         │     │MockAcquisition  │
│Provider         │     │Provider         │     │Provider         │
│(Graph API)      │     │(Compliant Proxy)│     │(Dev & Testing)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Provider Selection Priority
1. **`OfficialMetaProvider`**: Used automatically if `INSTAGRAM_GRAPH_ACCESS_TOKEN` and `INSTAGRAM_BUSINESS_ACCOUNT_ID` environment variables are present.
2. **`ExternalProvider`**: Used automatically if `EXTERNAL_ACQUISITION_API_KEY` is configured.
3. **`MockAcquisitionProvider`**: Default fallback for local development, contract testing, and CI pipelines without external network calls.

## Idempotent Post Ingestion Flow

```text
Creator Check Request / Polling Scheduler
                 │
                 ▼
      Load Creator from Postgres
                 │
                 ▼
    Status Active & Due Check?
                 │
      ┌──────────┴──────────┐
   NO │                     │ YES
      ▼                     ▼
    Skip         Acquire Posts via Provider
                            │
                            ▼
                    Normalize Content
                            │
                            ▼
                Deduplicate (DB Constraint)
                            │
                            ▼
                  Persist Posts & Media
                            │
                            ▼
                  Emit post.detected Event
                            │
                            ▼
                Update Check Timestamp
```

## Creator Lifecycle States

* `ACTIVE`: Monitoring enabled; healthy checks executing.
* `INACTIVE`: Paused by user.
* `ERROR`: Last acquisition attempt encountered unrecoverable error or exceeded maximum retries. Sanitized diagnostic message recorded in `last_error_message`.
* `UNSUPPORTED`: Creator profile handle is private, invalid, or inaccessible on platform.
