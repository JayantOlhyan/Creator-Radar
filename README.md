# CreatorRadar

> Open-Source Creator Intelligence & Original Opportunity Generation Platform.

CreatorRadar monitors domain experts across social platforms, detects new content, extracts underlying structural mechanisms, and transforms those blueprints into **original content opportunities** tailored to your personal expertise.

---

## Philosophy: Inspiration ≠ Replication

CreatorRadar explicitly rejects content scraping, script copying, and auto-reposting. 

It is built on a strict technical mandate: **Inspiration ≠ Replication**.

The platform uses AI to dissect source content into structural metadata (hook type, narrative pacing, emotional triggers, visual structure). It then discards the original wording and applies the extracted mechanism to your own knowledge base, ensuring all generated opportunities are 100% original.

---

## Current Project Status: Phase 1 (Active)

**⚠️ IMPORTANT:** CreatorRadar is currently in **Phase 1** of development. 

* **IMPLEMENTED:** Architecture foundation, Docker orchestration, database schemas, Next.js dashboard, FastAPI backend, async worker queues, and the idempotent **post ingestion pipeline**.
* **STUBBED / MOCKED:** AI analysis (OpenAI/Gemini), media transcription, personalization generation, and real platform acquisition (Instagram/LinkedIn APIs). 
* **NOT IMPLEMENTED:** Real-world Telegram notifications, interactive opportunity builder.

Please see the [Roadmap & Known Limitations](#roadmap--known-limitations) section before attempting to use this in production.

---

## Tech Stack

### Backend
* **Framework:** FastAPI (Python 3.11+)
* **Database:** PostgreSQL (with `asyncpg`)
* **ORM & Migrations:** SQLAlchemy 2.0 (Async) & Alembic
* **Queue & Workers:** Redis & `arq` (Async Job Queues)
* **Validation:** Pydantic 2.0

### Frontend
* **Framework:** Next.js 14 (App Router)
* **Language:** TypeScript
* **Styling:** Tailwind CSS
* **Icons:** Lucide React

### Infrastructure
* **Containerization:** Docker & Docker Compose
* **Caching/Brokers:** Redis 7

---

## Architecture

CreatorRadar utilizes a decoupled, event-driven monorepo architecture. 

### High-Level Request Flow

```text
User / Cron Schedule
       │
       ▼
[ FastAPI (API) ] ─── (CRUD / Config) ───> [ PostgreSQL ]
       │
   (Queues Job)
       │
       ▼
[ Redis Broker ] 
       │
   (Executes)
       ▼
[ Arq Worker ] ── (Fetches via Adapter) ──> [ Mock / External API ]
       │
   (Saves Data)
       ▼
[ PostgreSQL ]
```

### Repository Structure

```text
creator-radar/
├── apps/
│   ├── api/             # FastAPI backend (routers, models, main.py)
│   └── web/             # Next.js 14 Web UI Dashboard
├── workers/             # Async Redis queue workers (Arq)
│   ├── jobs/            # Job implementations (ingestion, analysis, etc.)
│   └── runner.py        # Arq worker entrypoint
├── packages/
│   ├── ai/              # AI Provider abstraction drivers (Currently mocked)
│   ├── schemas/         # Shared Pydantic domain models & event schemas
│   ├── source_adapters/ # Platform adapters (Instagram, LinkedIn)
│   └── shared/          # Config, DB connections, structured logging
├── infrastructure/      # Dockerfiles & postgres initialization scripts
└── tests/               # Pytest test suite
```

---

## Prerequisites

To run CreatorRadar locally, you must have:
* **Docker** & **Docker Compose**
* **Python 3.11+** (for local worker/API development without Docker)
* **Node.js 20+** (for local Next.js development without Docker)

---

## Installation & Setup (Docker)

The recommended way to run CreatorRadar is via Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CreatorRadar
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   *(Note: Because AI and External APIs are currently mocked, default values in `.env.example` are sufficient to spin up the stack).*

3. **Start the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the services:**
   * Web Dashboard: [http://localhost:3000](http://localhost:3000)
   * FastAPI Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
   * API Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## Environment Variables

| Variable | Required | Purpose | Example |
| -------- | -------- | ------- | ------- |
| `APP_ENV` | No | Environment mode | `development` |
| `DATABASE_URL` | Yes | Postgres connection string | `postgresql+asyncpg://user:pass@postgres:5432/db` |
| `REDIS_URL` | Yes | Redis broker connection | `redis://redis:6379/0` |
| `AI_PROVIDER` | No | AI Driver (`mock`, `openai`, `gemini`) | `mock` |
| `OPENAI_API_KEY` | No | Used if `AI_PROVIDER=openai` | `sk-proj-...` |
| `TELEGRAM_BOT_TOKEN` | No | Notification delivery | `12345:ABCDEF...` |

> **Security Note:** Never commit your `.env` file to version control. 

---

## Core Workflows (Implemented)

### 1. Watchlist Ingestion Pipeline

The only fully implemented background pipeline is the Post Ingestion workflow.

```text
Arq Scheduler (Cron) 
    ↓ 
Queues `poll_watchlist_creators_job` 
    ↓ 
Queues `check_creator_job` for active creators 
    ↓ 
Invokes SourceAdapter (e.g., InstagramAdapter) 
    ↓ 
App-level deduplication (`creator_id` + `external_id`) 
    ↓ 
Persists `PostModel` & `PostMediaModel` to DB 
    ↓ 
Emits `PostDetectedEvent`
```

---

## Database Architecture

The PostgreSQL schema is implemented via SQLAlchemy 2.0.

* **Creators (`creators`, `creator_sources`)**: Watchlist state, health, and tracking.
* **Posts (`posts`, `post_media`)**: Deduplicated content references.
* **Analysis (`post_analysis`, `content_patterns`)**: AI-extracted mechanisms.
* **Users (`users`, `user_profiles`, `knowledge_items`)**: User context for personalization.
* **Opportunities (`content_opportunities`, `notifications`)**: Generated output and delivery state.

---

## API Endpoints

The FastAPI backend exposes the following namespaces:

* `GET /api/v1/health` - System health check (API, Database, Redis).
* `GET /api/v1/config` - Public system configuration state.
* `/api/v1/creators` - Watchlist management CRUD.
* `/api/v1/opportunities` - Opportunity fetching and management.

Visit `/docs` on your local API server for the interactive OpenAPI schema.

---

## Testing

The project uses `pytest` with `pytest-asyncio` for the backend. 

To run tests locally:
```bash
pip install -r requirements.txt -r requirements-dev.txt (if applicable)
pytest tests/
```

---

## Roadmap & Known Limitations

**CreatorRadar is actively under development.** The current repository state reflects the foundational architecture, but lacks live execution engines for external dependencies.

### Implemented 
* Monorepo architecture & Database schema
* Web Dashboard UI (Creator Watchlist Interface)
* FastAPI REST Endpoints
* Idempotent Async Post Ingestion Pipeline (`check_creator_job`)
* Redis Queue integration & Rate Limiting Abstraction

### Mocked / Stubs (Known Limitations)
* **Source Acquisition:** The Instagram and LinkedIn adapters currently return mock data or rely on stubbed responses. Real Graph API integration is pending.
* **AI Processing:** The `OpenAIProvider` and `GeminiProvider` are implemented as shells that immediately fallback to the `MockProvider`. No real LLM network calls are made.
* **Media Transcription:** `transcribe_media_job` returns hardcoded dummy text.
* **Notifications:** The Telegram notification job logs to the console rather than sending HTTP requests.

### Planned (Future Phases)
* **Phase 2:** Real integration with OpenAI/Anthropic for the `analyze_content_job`.
* **Phase 3:** Real integration with Instagram Graph API or third-party proxy APIs.
* **Phase 4:** Interactive Opportunity Builder UI.
* **Phase 5:** Production deployment configurations.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Ensure tests pass (`pytest`)
4. Commit your changes (`git commit -m 'feat: add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).
