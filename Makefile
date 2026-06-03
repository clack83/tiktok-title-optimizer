.PHONY: dev test lint build migrate clean

dev:
	docker compose up -d

dev-down:
	docker compose down

dev-logs:
	docker compose logs -f

test:
	cd backend && pytest ../tests/ -v

test-cov:
	cd backend && pytest ../tests/ --cov=. --cov-report=html

test-backend:
	cd backend && pytest ../tests/unit ../tests/integration -v

lint:
	ruff check backend/ algorithms/
	cd frontend && npm run lint

lint-fix:
	ruff check backend/ algorithms/ --fix
	cd frontend && npm run lint -- --fix

build:
	docker compose build

migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(msg)"

shell:
	docker compose exec backend bash

clean:
	docker compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
