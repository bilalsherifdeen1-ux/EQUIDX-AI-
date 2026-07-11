# Roadmap

EQUIDX AI is a research/demonstration platform. This roadmap describes
plausible **future directions for the prototype's engineering scope** — it
is not a claim about real clinical capability or a regulatory timeline.

## Near term (prototype maturity)

- [ ] Replace in-memory AI model caching with persisted, versioned model
      artifacts in object storage (`BaseDiagnosticModel.save/load` is
      already scaffolded for this).
- [ ] Add a model registry service that tracks which model version
      generated which report, for full reproducibility.
- [ ] Expand GraphQL surface with mutations behind the same RBAC checks as
      REST.
- [ ] Add end-to-end (Playwright) tests for the web dashboard.
- [ ] Add rate limiting (Redis-backed) on authentication endpoints.

## Mid term (platform depth)

- [ ] Real-time dashboard updates via WebSocket from the biosensor
      simulator directly into the sample-tracking UI.
- [ ] Multi-tenancy (organization-scoped data isolation) for a
      multi-lab research deployment.
- [ ] Configurable alert rules per diagnostic domain (Prometheus Alertmanager
      routing to email/Slack).
- [ ] SDK/client libraries (Python, TypeScript) generated from the OpenAPI
      spec for third-party research integrations.

## Long term (exploratory — not committed)

- [ ] Federated-learning exploration across simulated multi-site data, to
      demonstrate privacy-preserving training patterns.
- [ ] Explainability layer (e.g. SHAP) surfaced alongside confidence
      scores in diagnostic reports.
- [ ] A formal "path to clinical validation" document outlining what real
      regulatory, data, and clinical-trial work would be required to move
      any single domain (e.g. urinalysis) from prototype to a real IVD
      product — explicitly out of scope for the codebase itself.

## Explicitly out of scope for this repository

- Real patient data ingestion of any kind.
- Any claim of regulatory clearance or clinical validation.
- Production-grade security hardening beyond what's needed to demonstrate
  the pattern (e.g. this repo's JWT secret rotation, WAF rules, and
  penetration testing are left to a real deployment's security team).
