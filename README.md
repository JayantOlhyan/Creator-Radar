# CreatorRadar

> Open-Source Creator Intelligence & Original Opportunity Generation Platform.

CreatorRadar monitors creators you follow, detects new content, analyzes underlying content patterns, and transforms those patterns into **original content opportunities** tailored specifically to your own expertise, projects, and experiences.

---

## Philosophy: Inspiration ≠ Replication

CreatorRadar is **NOT** a content-copying system, script scraper, or auto-reposting bot.

It explicitly enforces:

$$\text{INSPIRATION} \neq \text{REPLICATION}$$

The platform dissects source content into transferable structural mechanisms:
- Hook type & framing
- Narrative structure & pacing
- Target audience & emotional trigger
- Visual structure & CTA
- Strategic reason the content succeeds

It then applies those structural blueprints to your personal knowledge base to generate **100% original angles**, avoiding reproduction of the source creator's wording, jokes, or unique framing.

---

## Non-Goals

CreatorRadar is **NOT**:
- An automatic reposting system
- A content-copying engine
- An engagement bot or auto-commenter
- An automatic social-media posting service
- An Instagram-only product
- A generic AI writing assistant
- An automated follower-growth service

---

## Monorepo Architecture

```text
creator-radar/
├── apps/
│   ├── api/                     # FastAPI backend application & REST endpoints
│   └── web/                     # Next.js 14 Web UI Dashboard (TypeScript + Tailwind)
├── workers/                     # Async Redis queue workers (Arq worker pipeline)
├── packages/
│   ├── schemas/                 # Shared Pydantic domain models & event schemas
│   ├── ai/                      # AI Provider abstraction drivers (OpenAI, Gemini, Anthropic, Local)
│   ├── source_adapters/         # Source Adapter abstraction (Instagram, LinkedIn, YouTube, etc.)
│   └── shared/                  # Config, database, structured logging, error handling
├── infrastructure/              # Dockerfiles & PostgreSQL init scripts
├── docs/                        # Architecture & development documentation
└── tests/                       # Pytest test suite for contracts, adapters & health
```

---

## Core Product Pipeline

```text
WATCH → DETECT → INGEST → ANALYZE → EXTRACT PATTERN → PERSONALIZE → SCORE → NOTIFY → CREATE
```

---

## Quickstart (Docker Compose)

1. Clone the repository and configure environment variables:
   ```bash
   cp .env.example .env
   ```

2. Start the full application stack:
   ```bash
   docker compose up --build
   ```

3. Access services:
   - **Web Dashboard**: `http://localhost:3000`
   - **FastAPI Documentation**: `http://localhost:8000/docs`
   - **API Health Check**: `http://localhost:8000/api/v1/health`

---

## License

[MIT License](LICENSE)
