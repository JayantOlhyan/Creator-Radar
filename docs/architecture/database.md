# CreatorRadar — Database Architecture & Schema Specification

## Database Engine

CreatorRadar utilizes **PostgreSQL** managed by SQLAlchemy (async engine) and Alembic migrations.

## Entity Relationship Diagram

```text
User 1──1 UserProfile
User 1──* KnowledgeItem
User 1──* ContentOpportunity
User 1──* Notification

Creator 1──* CreatorSource
Creator 1──* Post
Post 1──* PostMedia
Post 1──1 PostAnalysis
PostAnalysis 1──* ContentOpportunity
ContentPattern 1──* ContentOpportunity
ContentOpportunity 1──* Notification
```

## Post Deduplication Strategy

Post deduplication is enforced at the database constraint level:

```sql
CONSTRAINT uq_creator_external_post UNIQUE (creator_id, external_id)
```

Before processing a detected post, the ingestion worker performs an upsert check against `(creator_id, external_id)`. If the post already exists, duplicate processing is safely bypassed.

## Core Schema Definitions

### `users`
* `id` (PK, UUID String)
* `email` (Unique Index, String 255)
* `full_name` (String 255)
* `created_at`, `updated_at` (Timestamp)

### `user_profiles`
* `id` (PK)
* `user_id` (FK `users.id`, Unique)
* `niche` (String)
* `content_goals` (JSON Array)
* `tone_of_voice` (String)
* `target_audience` (String)

### `creators`
* `id` (PK)
* `name`, `username` (Index), `platform` (Index), `profile_url`
* `is_active` (Boolean)

### `posts`
* `id` (PK)
* `creator_id` (FK `creators.id`, Index)
* `external_id` (String 255, Index)
* `url`, `content_type`, `caption`, `published_at`, `detected_at`
* `status` (Index: detected, ingested, transcribed, analyzed, failed)
* **Unique Constraint**: `(creator_id, external_id)`

### `post_media`
* `id` (PK), `post_id` (FK `posts.id`)
* `media_type`, `media_url`, `thumbnail_url`, `position`

### `post_analysis`
* `id` (PK), `post_id` (FK `posts.id`, Unique)
* `topic`, `hook`, `hook_type`, `format`, `narrative_structure`, `target_audience`
* `emotional_trigger`, `cta`, `visual_structure`, `editing_style`, `content_mechanism`, `why_it_works`
* `relevance_score`, `originality_score`

### `content_patterns`
* `id` (PK), `name`, `description`, `structure`, `example_count`

### `knowledge_items`
* `id` (PK), `user_id` (FK `users.id`, Index)
* `item_type` (project, expertise, experience, opinion, achievement)
* `title`, `content`, `tags` (JSON)

### `content_opportunities`
* `id` (PK), `user_id` (FK `users.id`, Index)
* `post_analysis_id` (FK `post_analysis.id`), `pattern_id` (FK `content_patterns.id`)
* `title`, `hook`, `concept`, `format`, `reasoning`
* `relevance_score`, `originality_score`, `effort_score`, `priority_score`
* `status` (Index: draft, saved, in_progress, completed, archived)

### `notifications`
* `id` (PK), `user_id` (FK `users.id`, Index), `opportunity_id` (FK `content_opportunities.id`)
* `channel`, `status`, `payload` (JSON), `sent_at`
