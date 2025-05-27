# Flask API Service

This directory contains the Flask-based REST API service for the ERP system.

## Overview
- **Framework:** Flask (with SQLAlchemy, Alembic for migrations)
- **Purpose:** Provides backend API endpoints for ERP modules (users, companies, stores, etc.)
- **Database:** PostgreSQL (configured via Docker Compose)
- **Containerized:** Yes (Docker/Docker Compose)

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

## Additional Information

- This service is part of a modular ERP system and is designed for extensibility and maintainability.
- For questions or contributions, see the main project documentation or contact the maintainers.
