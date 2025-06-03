# Flask API Service

Restaurant ERP Flask service for basic db interactions, recipes and menus function.

## Overview

Using flask, SQLAlchemy, alembic, provides basic CRUD for Postgres instance;


## Directory Structure
```
services/flask_api/
├── Dockerfile
├── requirements.txt
├── wsgi.py
├── src/
│   ├── __init__.py
│   ├── db.py
│   ├── api/
│   └── models/
├── migrations/
└── ...
```

## Setup & Usage

### 1. Prerequisites
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

### 2. Build & Run (via Docker Compose)
From the project root (`erp_main/`):
```bash
docker compose build
docker compose up
```
The Flask API will be available at `http://localhost:<port>` (see `docker-compose.yml`).

### 3. API Endpoints
- See `src/api/` for available endpoints (e.g., `/users`, `/companies`, etc.)

### 4. Database Migrations
To run Alembic migrations inside the container:
```bash
docker compose exec flask_api alembic upgrade head
```

## Development Notes

- **Local Development (optional):** If running outside Docker, create a virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  ```
- **Configuration:** Environment variables and config files are managed in `instance/` or via Docker Compose.

