# ERP Main Project

Restaurant tools project.  Current iteration includes file system, postgres schema, flask api with basic endpoints, db models, SQLalchemy, a simple data seed using alembic for some data to play with through the flask api.

## Quick start:
1. Clone repo

2. @ root:

        docker compose build
        docker compose up -d

3. docker will bing mount local project root directly, initialize db, and start flask service. If err, see:

        docker compose logs

4. localhost:5001; see /services/flask_api/README.md for paths


## File System Overview

```
erp_main/
├── backend/           # Django backend (future or placeholder)
├── config/            # Shared configuration and environment files
├── docker-compose.yml # Docker Compose orchestration for all services
├── menu_db_init.sql   # Database initialization script
├── services/          # Microservices (Flask API, etc.)
│   └── flask_api/     # Flask-based REST API service
│       ├── Dockerfile
│       ├── README.md
│       ├── requirements.txt
│       ├── wsgi.py
│       ├── instance/
│       ├── migrations/
│       └── src/
│           ├── __init__.py
│           ├── db.py
│           ├── api/
│           └── models/
├── ui/                # User interfaces
│   ├── mobile/        # (future) Mobile UI(s)
│   └── web/           # (future) Web UI (React)
└── ...
```
## Networking:

Please check/modify configs for external ports, host ports non-standard mapping for deconfliction. Internal compose network=erpnet

// Powershell show windows reserved ports:

    netsh interface ipv4 show excludedportrange protocol=tcp

## Flask Service:

See README.md at ./services/flask_api/

## UI/frontend and Django DRF/backend:

Not yet implemented; directories are placeholders...

## Database:

docker image postgres:15, docker volume pg_data. Docker will mount menu_db_init.sql and perform schema init; host port=5435. Flask service will auto-populuate db with some test data once db is up.
