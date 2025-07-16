# ---------------------------------------------------------------------------
# HOW TO RUN THIS SEED SCRIPT AUTOMATICALLY WITH DOCKER COMPOSE
#
# 1. Place this script (seed_db.py) in a directory accessible to your backend
#    or database service container (e.g., /seed/seed_db.py).
#
# 2. In your docker-compose.yml, add a service or an entrypoint/command override
#    to run this script after the database is ready. Example options:
#
#    a) As a one-off service (recommended for idempotent scripts):
#       services:
#         db-seed:
#           image: python:3.12
#           depends_on:
#             - db
#           volumes:
#             - ./seed/seed_db.py:/seed/seed_db.py
#           environment:
#             - PGHOST=db
#             - PGUSER=youruser
#             - PGPASSWORD=yourpassword
#             - PGDATABASE=yourdb
#           command: ["python", "/seed/seed_db.py"]
#
#    b) Or as a post-init command in your backend service:
#       command: >
#         bash -c "python /seed/seed_db.py && exec your-backend-start-command"
#
# 3. Ensure the script is idempotent (safe to run multiple times).
#
# 4. For local development, you can also run it manually:
#       docker-compose run --rm db-seed
#
# 5. Adjust environment variables and paths as needed for your setup.
# ---------------------------------------------------------------------------

"""
Seed script for ERP Postgres DB (multi-tenant, RLS-ready, UUID PKs)
- Each table's seed logic is in its own function, grouped by dependency.
- Uses psycopg2 for direct SQL execution.
- Idempotent: safe to run multiple times.
- Customize/add data as needed for your dev/test needs.
"""

import uuid
import psycopg2
from psycopg2.extras import execute_values

# ---- CONFIG ----
DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "dbname": "erp_main",
    "user": "postgres",
    "password": "postgres"
}

# ---- UTILS ----
def get_conn():
    """Get a new DB connection."""
    return psycopg2.connect(**DB_CONFIG)

def gen_uuid():
    """Generate a new UUID string."""
    return str(uuid.uuid4())

# ---- SEED FUNCTIONS ----

def seed_organizations(cur):
    """
    Seed organizations table.
    Returns: list of org dicts (id, name, description)
    """
    orgs = [
        {"id": gen_uuid(), "name": "Acme Corp", "description": "Demo org"},
        {"id": gen_uuid(), "name": "Globex Inc", "description": "Test org"},
    ]
    sql = """
        INSERT INTO organizations (id, name, description)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """
    values = [(o["id"], o["name"], o["description"]) for o in orgs]
    execute_values(cur, sql, values)
    return orgs

def seed_companies(cur, orgs):
    """
    Seed companies table.
    Returns: list of company dicts (id, name, org_id)
    """
    companies = [
        {"id": gen_uuid(), "name": "Acme Subsidiary", "org_id": orgs[0]["id"]},
        {"id": gen_uuid(), "name": "Globex Division", "org_id": orgs[1]["id"]},
    ]
    sql = """
        INSERT INTO companies (id, name, org_id)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """
    values = [(c["id"], c["name"], c["org_id"]) for c in companies]
    execute_values(cur, sql, values)
    return companies

def seed_users(cur, orgs, companies):
    """
    Seed users table.
    Returns: list of user dicts (id, email, org_id, company_id)
    """
    # Use passlib to hash passwords securely for seed users
    from passlib.hash import bcrypt
    users = [
        {
            "id": gen_uuid(),
            "email": "admin@acme.com",
            "password": bcrypt.hash("devpassword"),  # Use a known dev password, but always hashed
            "name": "Acme Admin",
            "org_id": orgs[0]["id"],
            "company_id": companies[0]["id"]
        },
        {
            "id": gen_uuid(),
            "email": "user@globex.com",
            "password": bcrypt.hash("devpassword"),
            "name": "Globex User",
            "org_id": orgs[1]["id"],
            "company_id": companies[1]["id"]
        },
    ]
    sql = """
        INSERT INTO users (id, email, password, name, org_id, company_id)
        VALUES %s
        ON CONFLICT (email) DO NOTHING
    """
    values = [(u["id"], u["email"], u["password"], u["name"], u["org_id"], u["company_id"]) for u in users]
    execute_values(cur, sql, values)
    return users

def seed_roles_permissions(cur, orgs):
    """
    Seed roles, permissions, and users_roles tables.
    Returns: dicts of roles, permissions, users_roles
    """
    # Roles
    roles = [
        {"id": gen_uuid(), "name": "admin", "description": "Administrator"},
        {"id": gen_uuid(), "name": "user", "description": "Regular User"},
    ]
    sql_roles = """
        INSERT INTO roles (id, name, description)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """
    execute_values(cur, sql_roles, [(r["id"], r["name"], r["description"]) for r in roles])

    # Permissions
    permissions = [
        {"id": gen_uuid(), "codename": "view_data", "description": "Can view data"},
        {"id": gen_uuid(), "codename": "edit_data", "description": "Can edit data"},
    ]
    sql_perms = """
        INSERT INTO permissions (id, codename, description)
        VALUES %s
        ON CONFLICT (codename) DO NOTHING
    """
    execute_values(cur, sql_perms, [(p["id"], p["codename"], p["description"]) for p in permissions])

    # Roles-Permissions bridge
    sql_rp = """
        INSERT INTO roles_permissions (role_id, permission_id)
        VALUES %s
        ON CONFLICT DO NOTHING
    """
    rp_values = [
        (roles[0]["id"], permissions[0]["id"]),
        (roles[0]["id"], permissions[1]["id"]),
        (roles[1]["id"], permissions[0]["id"]),
    ]
    execute_values(cur, sql_rp, rp_values)

    return {"roles": roles, "permissions": permissions}

# Add more seed functions for each table as needed, following the above pattern.
# For bridge tables, pass in the relevant parent objects and use their IDs.

# ---- MAIN ORCHESTRATION ----

def main():
    """
    Orchestrate the seeding process.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            print("Seeding organizations...")
            orgs = seed_organizations(cur)
            print("Seeding companies...")
            companies = seed_companies(cur, orgs)
            print("Seeding users...")
            users = seed_users(cur, orgs, companies)
            print("Seeding roles and permissions...")
            roles_perms = seed_roles_permissions(cur, orgs)
            # Add more seeding calls here, in dependency order.
            conn.commit()
            print("Seeding complete.")

if __name__ == "__main__":
    main()