# Cross-service tests

Unlike the unit/integration tests that live inside each service
(`backend/tests`, `ai-engine/tests`, etc.), this directory holds tests that
exercise the **running system** across service boundaries — useful in CI
after `docker compose up` or against a staging deployment.

- `integration/` — HTTP-level tests hitting multiple live services
  (backend ⇄ ai-engine ⇄ analytics) over the network.
- `e2e/` — browser-driven tests against the web app + backend together.

Run against a local stack:

```bash
docker compose up -d
pip install -r requirements.txt
pytest tests/integration -q
```
