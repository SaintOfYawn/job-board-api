# Job Board API (FastAPI + PostgreSQL)

Мини-сервис вакансий и откликов (мини HeadHunter). Проект сделан в стиле "фриланс/коммерция":
слои (routers/schemas/crud/models), JWT, роли, миграции, Docker, тесты и CI.

## Features
- JWT auth (user / company / admin)
- Company profile (1 company на company-user)
- Vacancies CRUD (только владелец компании / admin)
- Applications (без дублей)
- Filters + pagination
- Swagger `/docs`
- Alembic migrations (авто при старте docker)
- Seed demo-data
- Tests + GitHub Actions CI

## Run (Docker)
```bash
cp .env.example .env
docker compose up --build
```

Swagger:
- http://localhost:8000/docs

## Seed demo data
```bash
docker compose exec api python scripts/seed.py
```

## Tests (local)
```bash
pytest -q
```

