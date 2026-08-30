# CreatorRadar — Testing Guidelines & Test Suite Execution

## Testing Philosophy

CreatorRadar enforces strict contract validation and unit test coverage for core configuration, database models, source adapters, AI providers, schemas, and API health endpoints.

## Running Test Suite

### Python Backend & Contract Tests

```bash
pytest tests/ -v
```

### Next.js Frontend Build Verification

```bash
cd apps/web && npm run build
```
