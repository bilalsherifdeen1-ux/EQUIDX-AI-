.PHONY: up down build logs test test-backend test-ai lint fmt migrate seed docs

up:
	docker compose up --build

down:
	docker compose down -v

build:
	docker compose build

logs:
	docker compose logs -f

test: test-backend test-ai

test-backend:
	docker compose run --rm backend pytest -q

test-ai:
	docker compose run --rm ai-engine pytest -q

lint:
	docker compose run --rm backend ruff check app
	docker compose run --rm web npm run lint

fmt:
	docker compose run --rm backend ruff format app
	docker compose run --rm web npm run format

migrate:
	docker compose run --rm backend alembic upgrade head

seed:
	docker compose run --rm backend python -m app.infrastructure.db.seed

docs:
	cd docs && mkdocs serve
