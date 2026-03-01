# Job Board API

Backend service for job posting and application management (Mini HeadHunter).

## Tech Stack

- FastAPI
- Async SQLAlchemy
- PostgreSQL
- Alembic
- JWT Authentication
- Docker
- pytest
- GitHub Actions (CI)

---

## Features

- JWT authentication
- Role-based access (user / company / admin)
- Company profiles
- CRUD operations for job vacancies
- Apply to jobs (no duplicate applications)
- Filtering and pagination
- Async architecture
- Swagger documentation
- Database migrations (Alembic)
- Docker deployment
- Automated tests
- CI pipeline

---

## Project Structure


app/
├── models/
├── schemas/
├── routers/
├── services/
├── database/
├── core/
└── main.py


---

## Run Locally

### 1. Clone repository


git clone https://github.com/SaintOfYawn/job-board-api.git

cd job-board-api


### 2. Run with Docker


docker-compose up --build


API будет доступен:

http://localhost:8000/docs


---

## API Documentation

Swagger UI:

/docs


---

## Tests


pytest


---

## Author

Danila Denisov 
Junior Python Backend Developer
