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

def seed_companies(cur, context):

# context.get('orgs')[0]['id']
    companies = [
        {"id": gen_uuid(), "name": "Acme Subsidiary", "org_id": context.get('orgs')[0]['id']},
        {"id": gen_uuid(), "name": "Globex Division", "org_id": context.get('orgs')[1]['id']},
    ]

    sql = """
        INSERT INTO companies (org_id, id, name)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """
    values = [(c["org_id"], c["id"], c["name"], ) for c in companies]
    execute_values(cur, sql, values)
    return companies

def seed_users(cur, context):

    from passlib.hash import bcrypt
    users = [
        {
            "org_id": context.get('orgs')[0]['id'],
            "id": gen_uuid(),
            "email": "admin@acme.com",
            "password": bcrypt.hash("devpassword"),  # Use a known dev password, but always hashed
            "name": "Acme Admin",
            "company_id": context.get('companies')[0]["id"],
        },
        {
            "org_id": context.get('orgs')[0]["id"],
            "id": gen_uuid(),
            "email": "user@globex.com",
            "password": bcrypt.hash("devpassword"),
            "name": "Globex User",
            "company_id": context.get('companies')[1]["id"],
        },
    ]

    sql = """
        INSERT INTO users (org_id, id, email, password, name, company_id)
        VALUES %s
        ON CONFLICT (email) DO NOTHING
    """

    values = [(u["org_id"], u["id"], u["email"], u["password"], u["name"], u["company_id"]) for u in users]
    execute_values(cur, sql, values)
    return users

def seed_roles_permissions(cur, context):
    # Roles

    roles = [
        {
            # role 0, org 0, can edit
            "org_id": context.get('orgs')[0]['id'],
            "id": gen_uuid(),
            "name": "admin",
            "description": "Administrator"
        },
        {
            # role 1, org 0, can view
            "org_id": context.get('orgs')[0]['id'],
            "id": gen_uuid(),
            "name": "user",
            "description": "Regular User"
        },
        {
            # role 2, org 1, edit
            "org_id": context.get('orgs')[1]['id'],
            "id": gen_uuid(),
            "name": "admin",
            "description": "Administrator"
         },
        {
            # role 3, org 1, view
            "org_id": context.get('orgs')[1]['id'],
            "id": gen_uuid(),
            "name": "user",
            "description": "Regular User"
         },
    ]
    for i in roles:
        print(f'role uuid: ${i['id']}')

    sql_roles = """
        INSERT INTO roles (org_id, id, name, description)
        VALUES %s
        ON CONFLICT (org_id, name) DO NOTHING
    """

    execute_values(cur, sql_roles, [(r["org_id"], r["id"], r["name"], r["description"]) for r in roles])

    # Permissions
    permissions = [
        {
            # perm 1, org 0, admin
            "org_id": context.get('orgs')[0]['id'],
            "id": gen_uuid(),
            "codename": "edit_data",
            "description": "Can edit data"
        },
        {
            # perm 1, org 0, user
            "org_id": context.get('orgs')[0]['id'],
            "id": gen_uuid(),
            "codename": "view_data",
            "description": "Can view data"
        },
        {
            # perm 2, org 1, admin
            "org_id": context.get('orgs')[1]['id'],
            "id": gen_uuid(),
            "codename": "edit_data",
            "description": "Can edit data"
        },
        {
            # perm 3, org 1, user
            "org_id": context.get('orgs')[1]['id'],
            "id": gen_uuid(),
            "codename": "view_data",
            "description": "Can view data"
        },
    ]
    sql_perms = """
        INSERT INTO permissions (org_id, id, codename, description)
        VALUES %s
        ON CONFLICT (org_id, codename) DO NOTHING
    """
    execute_values(cur, sql_perms, [(p["org_id"], p["id"], p["codename"], p["description"]) for p in permissions])

    # Roles-Permissions bridge
    sql_rp = """
        INSERT INTO roles_permissions (org_id, role_id, permission_id)
        VALUES %s
        ON CONFLICT DO NOTHING
    """
    rp_values = [
        (
            # relation 0: org 0, user
            context.get('orgs')[0]['id'],
            roles[0]["id"],
            permissions[0]["id"]
        ),
        (
            # rel 1 org 0 admin
            context.get('orgs')[0]['id'],
            roles[1]["id"],
            permissions[1]["id"]
        ),
        (
            context.get('orgs')[1]['id'],
            roles[2]["id"],
            permissions[2]["id"]
        ),
        (
            context.get('orgs')[1]['id'],
            roles[3]["id"],
            permissions[3]["id"]
        ),
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
            context = {}

            print("Seeding organizations...")
            # orgs = seed_organizations(cur)
            context['orgs'] = seed_organizations(cur)

            print("Seeding companies...")
            # companies = seed_companies(cur, orgs)
            context['companies'] = seed_companies(cur, context)

            print("Seeding users...")
            # users = seed_users(cur, orgs, companies)
            context['users'] = seed_users(cur, context)

            print("Seeding roles and permissions...")
            # roles_perms = seed_roles_permissions(cur, orgs)
            context['roles_perms'] = seed_roles_permissions(cur, context)

            # Add more seeding calls here, in dependency order.
            conn.commit()
            print("Seeding complete.")

if __name__ == "__main__":
    main()