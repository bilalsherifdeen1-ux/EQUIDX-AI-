# Logging pipeline

Structured JSON logs are written to stdout by every FastAPI service (see
`app/core/logging.py` in `backend/`, mirrored in the other Python
services). Two ways to collect them:

1. **Quick start (already in root docker-compose.yml)** — OpenSearch +
   OpenSearch Dashboards only; point your container runtime's log driver
   or a lightweight shipper at stdout.
2. **Full ELK-style pipeline (this directory)** — Filebeat tails Docker
   container logs, ships to Logstash, which parses JSON and indexes into
   OpenSearch:

   ```bash
   docker compose -f infrastructure/logging/docker-compose.logging.yml up
   ```

Dashboards: http://localhost:5601 — create an index pattern on
`equidx-logs-*`.
