# Contributing to EQUIDX AI

Thanks for your interest in EQUIDX AI — a research/demo platform, so
contributions here are about improving the architecture, engineering
practice, and demonstration quality rather than clinical accuracy.

## Ground rules

1. **Synthetic data only.** Never introduce real patient data, real PHI, or
   any dataset you don't have clear rights/license to use as synthetic
   training data. All contributed datasets must be either procedurally
   generated or explicitly public-domain/synthetic.
2. **Keep the disclaimers intact.** Any UI, API response, or document that
   surfaces AI-generated findings must retain the research-prototype /
   not-for-clinical-use disclaimer.
3. **Respect the architecture boundaries.** `backend/app` follows Clean
   Architecture: `domain` has no framework imports, `application` depends
   only on domain interfaces, `infrastructure` implements those interfaces,
   and `api` wires everything via dependency injection (see
   `app/core/deps.py`). New features should follow the same layering.

## Development setup

See [`docs/docs/installation.md`](docs/docs/installation.md) for full
setup steps. Quick version:

```bash
cp .env.example .env
docker compose up --build
make migrate
make seed
```

## Making a change

1. Fork and branch from `main` (`feature/short-description`).
2. Write or update tests alongside your change — see each service's
   `tests/` directory for existing patterns.
3. Run `make lint` and `make test` before opening a PR.
4. Fill out the PR template, including the synthetic-data/disclaimer
   checklist items.

## Adding a new AI diagnostic domain

Use the [`new_diagnostic_domain` issue template](.github/ISSUE_TEMPLATE/new_diagnostic_domain.md)
to propose it first. Implementation-wise:

1. Add a synthetic data generator function to
   `ai-engine/ai_engine/datasets/synthetic_data_generator.py`.
2. Create `ai-engine/ai_engine/models/<domain>/model.py` implementing
   `BaseDiagnosticModel` (see `ai_engine/common/base.py`).
3. Register the domain in `ai_engine/pipeline.py`'s `_TRAINERS` dict.
4. Add tests in `ai-engine/tests/`.
5. Add the new `SampleType` enum value in
   `backend/app/domain/entities/sample.py` and the corresponding Alembic
   migration.

## Code style

- Python: `ruff` (see `backend/pyproject.toml`), type hints throughout,
  docstrings on modules/classes explaining *why*, not just *what*.
- TypeScript: `eslint` (Next.js config) + `prettier`.
- Commit messages: conventional-commit style preferred
  (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `infra:`).

## Reporting security issues

Please do not open a public issue for security vulnerabilities — use
GitHub's private security advisory feature (linked in the issue template
chooser) instead.

## Code of conduct

Be respectful, assume good faith, and keep discussion focused on the
technical merits. This is a demonstration project; disagreements about
architecture choices are welcome, but keep them constructive.
