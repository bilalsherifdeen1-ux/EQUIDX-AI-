# Installation Guide

## Prerequisites

- Docker & Docker Compose v2
- (Optional, for non-Docker dev) Python 3.11+, Node.js 20+

## 1. Clone and configure

```bash
git clone https://github.com/equidx-ai/equidx-ai.git
cd equidx-ai
cp .env.example .env
```

Edit `.env` if you want non-default credentials — the defaults work for
local development out of the box.

## 2. Start the stack

```bash
docker compose up --build
```

This starts:

| Service | Port |
|---|---|
| `web` (Next.js) | 3000 |
| `backend` (FastAPI) | 8000 |
| `ai-engine` | 8100 |
| `biosensor-simulator` | 8200 |
| `analytics` | 8300 |
| `mobile-api` | 8400 |
| `postgres` | 5432 |
| `redis` | 6379 |
| `minio` (S3-compatible) | 9000 / 9001 (console) |
| `prometheus` | 9090 |
| `grafana` | 3001 |
| `opensearch` | 9200 |
| `opensearch-dashboards` | 5601 |

## 3. Run database migrations

```bash
make migrate
# equivalent: docker compose run --rm backend alembic upgrade head
```

## 4. Seed synthetic demo data

```bash
make seed
# equivalent: docker compose run --rm backend python -m app.infrastructure.db.seed
```

This creates:

- `admin@equidx.ai` / `ChangeMe123!` (ADMIN role)
- `clinician@equidx.ai` / `ChangeMe123!` (CLINICIAN role)
- `researcher@equidx.ai` / `ChangeMe123!` (RESEARCHER role)
- 25 synthetic patients with associated samples

**Change these passwords immediately if you deploy this anywhere beyond
your own machine.**

## 5. Explore

- Web app: <http://localhost:3000>
- API docs (Swagger): <http://localhost:8000/docs>
- GraphQL: <http://localhost:8000/graphql>
- Grafana: <http://localhost:3001> (admin/admin by default)

## Running tests

```bash
make test            # backend + ai-engine
make test-backend
make test-ai
```

Or per-service:

```bash
docker compose run --rm biosensor-simulator pytest -q
docker compose run --rm analytics pytest -q
docker compose run --rm mobile-api pytest -q
cd web && npm install && npm run lint && npm run build
```

## Running the documentation site

```bash
cd docs
pip install -r requirements.txt
mkdocs serve
```

Visit <http://localhost:8001> (or whatever port `mkdocs serve` reports).

## Troubleshooting

- **`backend` can't reach `postgres`**: wait for the `postgres` healthcheck
  to pass (`docker compose ps`) before running migrations.
- **MinIO bucket errors**: the backend calls `ensure_bucket_exists()` on
  first upload; if you see access-denied errors, check `S3_ACCESS_KEY`
  / `S3_SECRET_KEY` match between `.env` and the `minio` service.
- **Port conflicts**: adjust the host-side port mappings in
  `docker-compose.yml` if something else on your machine is already using
  one of the ports above.
