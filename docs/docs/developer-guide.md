# Developer Guide

## Codebase tour

```
equidx-ai/
├── web/                  Next.js 15 + TS + Tailwind — marketing site + dashboard
├── backend/              FastAPI — core domain API (Clean Architecture / DDD)
├── ai-engine/             Modular placeholder AI framework (5 diagnostic domains)
├── biosensor-simulator/  Synthetic biosensor signal generator (REST + WS)
├── analytics/            Read-only aggregation microservice
├── mobile-api/           Backend-for-frontend for mobile clients
├── infrastructure/       docker-compose, k8s, terraform, monitoring, logging
├── docs/                 This MkDocs site
└── tests/                Cross-service integration/e2e tests
```

## Adding a new backend feature (example: a "specimen notes" field)

1. **Domain**: add/modify the field on the relevant dataclass in
   `backend/app/domain/entities/`.
2. **Infrastructure**: update the SQLAlchemy model in
   `app/infrastructure/db/models/orm_models.py`, then generate an Alembic
   migration:
   ```bash
   docker compose run --rm backend alembic revision --autogenerate -m "add specimen notes"
   ```
3. **Repository**: update the `_to_entity` mapper and CRUD methods in the
   matching file under `app/infrastructure/db/repositories/`.
4. **Application**: add/adjust a method on the relevant service in
   `app/application/services/`.
5. **API**: add/adjust the Pydantic DTO in
   `app/application/dto/schemas.py` and the router in
   `app/api/v1/routers/`.
6. **Tests**: add a unit test (fake repository) and/or integration test
   (real DB via the `client`/`db_session` fixtures in `backend/tests/conftest.py`).

This keeps each layer's responsibility narrow and testable in isolation —
the point of the repository-pattern + DI setup in `app/core/deps.py`.

## Adding a new AI diagnostic domain

See [`CONTRIBUTING.md`](https://github.com/equidx-ai/equidx-ai/blob/main/CONTRIBUTING.md#adding-a-new-ai-diagnostic-domain)
for the full checklist. In short: synthetic data generator → model class
implementing `BaseDiagnosticModel` → register in `pipeline.py` → new
`SampleType` enum value + migration in the backend.

## Frontend conventions

- App Router (`web/app/`), server components by default; anything with
  interactivity/state is marked `"use client"`.
- Shared fetch logic lives in `web/lib/api-client.ts` — don't call `fetch`
  directly from components.
- Design tokens (colors, fonts) are defined in `tailwind.config.ts` and
  `app/globals.css` — reuse the `ink`/`signal`/`amber`/`mist` palette
  rather than introducing new ad hoc colors.

## Local debugging tips

- `docker compose logs -f backend` — structured JSON logs, one line per
  request plus explicit `logger.info(...)` calls.
- `docker compose exec postgres psql -U equidx` — direct DB access.
- The `ai-engine` service trains its placeholder models **in memory, lazily,
  on first request** per domain (see `ai_engine/pipeline.py`) — the first
  call to a new domain will be slower than subsequent ones.

## Style / linting

```bash
make lint   # ruff (backend) + eslint (web)
make fmt    # ruff format (backend) + prettier (web)
```
