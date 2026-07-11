# EQUIDX AI

**A research/prototype AI-powered biosensor diagnostics platform.**

!!! warning "Research prototype — not for clinical use"
    EQUIDX AI is an early-stage research and demonstration platform. All
    patient records, biosensor signals, and diagnostic outputs are
    **synthetic**. Nothing produced by this software may be used to
    diagnose, treat, or make clinical decisions about a real person. See
    the full [disclaimer](disclaimer.md).

## What's in this documentation

- **[Architecture](architecture.md)** — system diagram, layering, and the
  design principles behind each service.
- **[Installation](installation.md)** — get the full stack running
  locally with Docker Compose.
- **[Developer Guide](developer-guide.md)** — codebase tour, how to add a
  feature, how to add a new AI diagnostic domain.
- **[Deployment Guide](deployment.md)** — Kubernetes + Terraform path to a
  cloud environment.
- **[API Reference](api-reference.md)** — REST (OpenAPI) and GraphQL
  surfaces.
- **[Roadmap](roadmap.md)** — where this prototype is headed.

## Quick links

| | |
|---|---|
| Backend OpenAPI docs | `http://localhost:8000/docs` |
| GraphQL playground | `http://localhost:8000/graphql` |
| AI Engine docs | `http://localhost:8100/docs` |
| Grafana | `http://localhost:3001` |
| OpenSearch Dashboards | `http://localhost:5601` |
