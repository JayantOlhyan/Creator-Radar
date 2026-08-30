# CreatorRadar — Event Driven Architecture Specification

## Overview

CreatorRadar uses an event-driven queue model to process content asynchronously.

## System Events Registry

| Event Name | Producer | Consumer | Payload Highlights | Failure Policy |
| :--- | :--- | :--- | :--- | :--- |
| `post.detected` | Source Adapter / Ingestion Job | Ingestion Queue Handler | `creator_id`, `external_id`, `platform`, `url` | Retry 3x exponential backoff |
| `post.ingested` | Ingestion Worker | Transcription Worker | `post_id`, `creator_id`, `media_urls` | Dead letter queue on media error |
| `post.transcription.completed` | Transcription Worker | Content Analysis Worker | `post_id`, `transcript_text`, `language` | Fallback to caption analysis |
| `post.analysis.completed` | Content Analysis Worker | Pattern Detection & Opportunity Worker | `post_id`, `analysis_id`, `relevance_score` | Log error & flag post status |
| `pattern.detected` | Pattern Extraction Worker | Database / Opportunity Generator | `pattern_id`, `structure`, `matched_posts` | Non-blocking warning |
| `opportunity.generated` | Personalization Worker | Notification Worker | `opportunity_id`, `user_id`, `priority_score` | Retry notification delivery |
| `notification.created` | Opportunity Generator | Telegram Delivery Worker | `notification_id`, `user_id`, `channel`, `payload` | Log delivery failure |
