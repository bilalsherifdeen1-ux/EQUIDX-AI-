# EQUIDX AI

**An AI-powered biosensor diagnostics platform — research prototype.**

> ⚠️ **RESEARCH & PROTOTYPE SOFTWARE — NOT FOR CLINICAL USE.**
> EQUIDX AI is an early-stage research and demonstration platform. All patient
> records, biosensor signals, and diagnostic outputs in this repository are
> **synthetic**. No component of this system has been validated, verified, or
> approved by any regulatory body (FDA, CE-IVD, etc.). **Nothing produced by
> this software may be used to diagnose, treat, or make clinical decisions
> about a real person.** See [`docs/docs/disclaimer.md`](docs/docs/disclaimer.md).

---

## What is this?

EQUIDX AI is a monorepo that demonstrates what a modern, modular, cloud-native
architecture for an AI-assisted biosensor diagnostics platform could look
like — end to end, from a marketing site down to Terraform-provisioned
infrastructure. It is built to show engineering practice (clean architecture,
DDD, RBAC, audit logging, observability, CI/CD) rather than to make real
medical claims. Every AI "diagnostic" model in this repo is a placeholder
trained on synthetic data.

## Monorepo layout

| Path | Purpose |
|---|---|
| `web/` | Next.js 15 marketing site + research/clinician dashboard (TypeScript, Tailwind) |
| `backend/` | FastAPI core API — auth, patients, samples, reports, admin, RBAC, audit log, REST + GraphQL |
| `ai-engine/` | Modular AI framework: preprocessing → training → inference → evaluation for urinalysis, HbA1c, blood chemistry, metabolic panel, HIV screening (all placeholder models, synthetic data) |
| `biosensor-simulator/` | Generates realistic synthetic biosensor signal streams (REST + WebSocket) |
| `analytics/` | Aggregation/analytics microservice powering the analytics dashboard |
| `mobile-api/` | Backend-for-frontend gateway tuned for mobile clients |
| `infrastructure/` | Docker Compose, Kubernetes manifests, Terraform, Prometheus/Grafana, ELK/OpenSearch, Nginx |
| `docs/` | MkDocs documentation site — architecture, install, dev, deployment, roadmap |
| `tests/` | Cross-service integration and end-to-end tests |

## Quickstart (local dev)

```bash
git clone https://github.com/equidx-ai/equidx-ai.git
cd equidx-ai
cp .env.example .env
docker compose up --build
```

- Web: http://localhost:3000
- Backend API docs (OpenAPI): http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- AI Engine service: http://localhost:8100/docs
- Biosensor simulator: http://localhost:8200/docs
- Analytics service: http://localhost:8300/docs
- Grafana: http://localhost:3001 (admin/admin)
- MkDocs site: `cd docs && mkdocs serve` → http://localhost:8001

See [`docs/docs/installation.md`](docs/docs/installation.md) for full setup,
and [`docs/docs/developer-guide.md`](docs/docs/developer-guide.md) for the
architecture deep-dive.

## Engineering principles applied

- **Clean Architecture / DDD** — `backend/app` is split into `domain`,
  `application`, `infrastructure`, and `api` layers with dependencies pointing
  inward.
- **Repository pattern + Dependency Injection** — FastAPI's `Depends` wires
  repository interfaces to SQLAlchemy implementations; domain/application
  layers only see abstract repository interfaces.
- **SOLID** — services take narrow interfaces, are composed rather than
  inherited, and are individually testable.
- **Security** — JWT access/refresh tokens, OAuth2 password + authorization
  code flows, password hashing (argon2), RBAC decorators, audit logging on
  all writes, input validation via Pydantic.
- **Observability** — Prometheus metrics on every service, Grafana
  dashboards, structured JSON logs shipped to OpenSearch, correlation IDs.

## License

MIT — see [`LICENSE`](LICENSE). This is a research/demo project; see the
disclaimer above and in `docs/`.
