# CreatorRadar — Local Development & Docker Workflow Setup

## Prerequisites

* Docker & Docker Compose
* Python 3.11+
* Node.js 18+ / npm

## Environment Configuration

1. Copy the example environment configuration:
   ```bash
   cp .env.example .env
   ```
2. Verify default settings in `.env`:
   - `DATABASE_URL=postgresql+asyncpg://creatorradar:creatorradar_dev_pass@postgres:5432/creatorradar_db`
   - `REDIS_URL=redis://redis:6379/0`
   - `AI_PROVIDER=mock`

## Starting Local Development Stack via Docker Compose

```bash
docker compose up --build
```

This starts:
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **FastAPI Backend**: `http://localhost:8000` (OpenAPI Docs at `/docs`)
- **Async Queue Worker**: Background Arq runner
- **Next.js Web UI**: `http://localhost:3000`

## Running Migrations Manually

```bash
alembic upgrade head
```
