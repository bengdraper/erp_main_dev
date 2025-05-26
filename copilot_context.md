# Copilot Context & Architectural Notes

_Last updated: 2025-05-26_

## Project Overview
- **Frontend:** React (see `/frontend`)
- **Backend:** Flask API (see `/modules/menus_api_flask/menus/menus_app/src`)
- **Database:** Postgres (via Docker Compose)
- **Future:** Plan to migrate/extend backend to Django; may add mobile clients.

## Key Priorities
- **Learning and understanding best practices** for architecture and design.
- **Start monolithic, then refactor**: MVP first, then abstract to service layers as project matures.
- **Separation of concerns**: Keep business logic (service layer) separate from API (route/view) layer.
- **Modular code organization**: Models, APIs, and services in their own files/folders.
- **Pluggable/extensible architecture**: Design so new clients (mobile, CLI, etc.) can use the same backend API/services with minimal refactor.

## Naming Conventions
- `frontend/` for React app (preferred over `client/` or `app/` for clarity)
- `backend/` or `api/` for Flask/Django API (use subfolders for multiple backends)
- Use plural, snake_case for API endpoint files (e.g., `users.py`), singular or domain-grouped for model files (e.g., `user.py`, `chart_of_accounts.py`).

## Service Layer Abstraction
- **Goal:** Move business logic and DB access to `services/` modules, keep API routes thin.
- **Pattern:**
  - API route parses request, calls service, returns response.
  - Service handles validation, business rules, DB interaction.
- **Benefits:**
  - Reusable logic for multiple clients (web, mobile, CLI).
  - Easier migration to Django or other frameworks.
  - Improved testability and maintainability.
- **Current status:**
  - MVP may have business logic in API routes; refactor to services as features stabilize.
  - Reminder: Look for "refactor points" to extract logic from routes to services.

## API Design
- **RESTful endpoints** returning JSON.
- **Consistent response format** (e.g., `{ "data": ..., "error": ... }`).
- **Document endpoints and data contracts** (OpenAPI/Swagger recommended for future).
- **Versioning:** Consider for future extensibility.

## ORM & Models
- Using SQLAlchemy for now; keep model logic separate from Flask-specific code.
- If migrating to Django ORM, service layer will need refactor, but API and business rules remain portable.

## Migration & Extensibility
- **Keep business logic and data access decoupled from framework-specific code.**
- **Avoid Flask/Django globals in business logic.**
- **Document architectural decisions and refactor opportunities here.**

## To Future Copilot/AI
- Use this file to quickly reacquire project context, priorities, and architectural direction.
- Remind user of service layer abstraction opportunities as project matures, but do not overcomplicate MVP.
- Prioritize learning, clarity, and maintainability in all suggestions.

---

**Recent architectural focus:**
- Modularizing models and APIs.
- Avoiding SQLAlchemy table redefinition errors.
- Planning for service layer abstraction and future Django migration.
- Naming and folder structure best practices.
