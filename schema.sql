SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- dateTime
CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP ='INSERT' THEN
        NEW.date_created = NOW();
        NEW.date_updated = NOW();
    ELSIF TG_OP = 'UPDATE' THEN
        NEW.date_updated = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TABLES
CREATE TABLE users (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    -- company_id UUID,
    metadata JSONB DEFAULT '{}'::jsonb,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_users
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

-- track changes to users
CREATE TABLE users_audit (
    org_id UUID,  -- rls / org of altered user fkey
    id SERIAL PRIMARY KEY,  -- this_record.id
    user_id UUID,  -- altered user fkey
    audit_action TEXT NOT NULL,  -- elsewhere defined
    audit_timestamp TIMESTAMPTZ NOT NULL,
    audit_user UUID,  -- ref to user who acted on this.user fkey
    old_data JSONB,
    new_data JSONB
);

-- user change audit pusher
CREATE OR REPLACE FUNCTION audit_users_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO users_audit (
            org_id, user_id, audit_action, audit_timestamp, audit_user, old_data, new_data
        )
        VALUES (
            OLD.org_id, OLD.id, 'DELETE', NOW(), current_setting('app.current_user', true)::uuid, to_jsonb(OLD), NULL
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO users_audit (
            org_id, user_id, audit_action, audit_timestamp, audit_user, old_data, new_data
        )
        VALUES (
            NEW.org_id, NEW.id, 'UPDATE', NOW(), current_setting('app.current_user', true)::uuid, to_jsonb(OLD), to_jsonb(NEW)
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO users_audit (
            org_id, user_id, audit_action, audit_timestamp, audit_user, old_data, new_data
        )
        VALUES (
            NEW.org_id, NEW.id, 'INSERT', NOW(), current_setting('app.current_user', true)::uuid, NULL, to_jsonb(NEW)
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- pushit
CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_users_changes();

-- back to building all the other tables
CREATE TABLE users_stores (
    org_id UUID NOT NULL,
    user_id UUID NOT NULL,
    store_id UUID NOT NULL,
    PRIMARY KEY (user_id, store_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_users_stores
BEFORE INSERT OR UPDATE ON users_stores
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE companies (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_companies
BEFORE INSERT OR UPDATE ON companies
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE stores (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    company_id UUID NOT NULL,
    chart_of_accounts_id INT NOT NULL DEFAULT 1,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_stores
BEFORE INSERT OR UPDATE ON stores
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE stores_menus (
    org_id UUID NOT NULL,
    store_id UUID NOT NULL,
    menu_id INT NOT NULL,
    PRIMARY KEY (store_id, menu_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_stores_menus
BEFORE INSERT OR UPDATE ON stores_menus
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE chart_of_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_chart_of_accounts
BEFORE INSERT OR UPDATE ON chart_of_accounts
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE chart_of_accounts_sales_account_categories (
    org_id UUID NOT NULL,
    chart_of_accounts_id INT,
    sales_account_category_id INT,
    PRIMARY KEY (chart_of_accounts_id, sales_account_category_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_chart_of_accounts_sales_account_categories
BEFORE INSERT OR UPDATE ON chart_of_accounts_sales_account_categories
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE chart_of_accounts_cog_account_categories (
    org_id UUID NOT NULL,
    chart_of_accounts_id INT,
    cog_account_category_id INT,
    PRIMARY KEY (chart_of_accounts_id, cog_account_category_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_chart_of_accounts_cog_account_categories 
BEFORE INSERT OR UPDATE ON chart_of_accounts_cog_account_categories 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE sales_account_categories (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number TEXT NOT NULL UNIQUE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_sales_account_categories
BEFORE INSERT OR UPDATE ON sales_account_categories
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE sales_account_categories_sales_accounts (
    org_id UUID NOT NULL,
    sales_account_category_id INT,
    sales_account_id INT,
    PRIMARY KEY (sales_account_category_id, sales_account_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_sales_account_categories_sales_accounts 
BEFORE INSERT OR UPDATE ON sales_account_categories_sales_accounts 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE sales_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_sales_accounts
BEFORE INSERT OR UPDATE ON sales_accounts
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE cog_account_categories (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_cog_account_categories 
BEFORE INSERT OR UPDATE ON cog_account_categories
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE cog_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number TEXT NOT NULL UNIQUE,
    cog_account_category_id INT NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_cog_accounts
BEFORE INSERT OR UPDATE ON cog_accounts
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE menus (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL UNIQUE,
    sales_account_id INT,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_menus
BEFORE INSERT OR UPDATE ON menus
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE menus_recipes_plated (
    org_id UUID NOT NULL,
    menu_id INT,
    recipe_plated_id INT,
    PRIMARY KEY (menu_id, recipe_plated_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_menus_recipes_plated
BEFORE INSERT OR UPDATE ON menus_recipes_plated
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE recipes_plated (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT NOT NULL,
    recipe_type TEXT,
    sales_price_basis numeric NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_recipes_plated
BEFORE INSERT OR UPDATE ON recipes_plated
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE recipes_plated_recipes_nested (
    org_id UUID NOT NULL,
    recipe_plated_id INT NOT NULL,
    recipe_nested_id INT NOT NULL,
    PRIMARY KEY (recipe_plated_id, recipe_nested_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_recipes_plated_recipes_nested 
BEFORE INSERT OR UPDATE ON recipes_plated_recipes_nested 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE recipes_plated_ingredients_types (
    org_id UUID NOT NULL,
    recipe_plated_id INT NOT NULL,
    ingredient_type_id INT NOT NULL,
    PRIMARY KEY (recipe_plated_id, ingredient_type_id),
    ingredient_quantity numeric NOT NULL,
    ingredient_uom TEXT NOT NULL,
    ingredient_cost numeric NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_recipes_plated_ingredients_types 
BEFORE INSERT OR UPDATE ON recipes_plated_ingredients_types 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE recipes_nested (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT,
    recipe_type TEXT,
    yield numeric NOT NULL,
    yield_uom TEXT NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_recipes_nested
BEFORE INSERT OR UPDATE ON recipes_nested
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE recipes_nested_ingredients_types (
    org_id UUID NOT NULL,
    recipe_nested_id INT NOT NULL,
    ingredient_type_id INT NOT NULL,
    PRIMARY KEY (recipe_nested_id, ingredient_type_id),
    ingredient_quantity numeric NOT NULL,
    ingredient_uom TEXT NOT NULL,
    ingredient_cost numeric NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_recipes_nested_ingredients_types 
BEFORE INSERT OR UPDATE ON recipes_nested_ingredients_types 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE ingredients_types (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    unit_cost numeric NOT NULL,
    unit_of_measure TEXT NOT NULL,
    cog_account_id INT NOT NULL,
    preferred_ingredient_item_id INT,
    current_ingredient_item_id INT,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_ingredients_types
BEFORE INSERT OR UPDATE ON recipes_nested_ingredients_types
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE ingredients_vendor_items (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    vendor_item_id NUMERIC NOT NULL,
    vendor_item_description TEXT NOT NULL UNIQUE,
    purchase_unit TEXT NOT NULL,
    purchase_unit_cost numeric NOT NULL,
    split_case_count INT NOT NULL,
    split_case_cost numeric NOT NULL,
    split_case_uom TEXT NOT NULL,
    split_case_uom_cost numeric NOT NULL,
    notes TEXT NOT NULL,
    ingredient_type_id INT NOT NULL,
    vendor_id INT NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_ingredients_vendor_items 
BEFORE INSERT OR UPDATE ON ingredients_vendor_items 
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE vendors (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact_name TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    delivery_days TEXT,
    order_days TEXT,
    order_cutoff_time TEXT,
    terms TEXT,
    notes TEXT,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_vendors
BEFORE INSERT OR UPDATE ON vendors
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE roles (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    CONSTRAINT uq_org_name UNIQUE (org_id, name),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_roles
BEFORE INSERT OR UPDATE ON roles
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE permissions (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codename TEXT NOT NULL,
    description TEXT,
    CONSTRAINT uq_org_codename UNIQUE (org_id, codename),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_permissions
BEFORE INSERT OR UPDATE ON permissions
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_organizations
BEFORE INSERT OR UPDATE ON organizations
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE divisions (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_divisions
BEFORE INSERT OR UPDATE ON divisions
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE users_roles (
    org_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    division_id UUID,
    company_id UUID,
    store_id UUID,
    CONSTRAINT uq_org_user_role_division_company_store UNIQUE (org_id, user_id, role_id, division_id, company_id, store_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_users_roles
BEFORE INSERT OR UPDATE ON users_roles
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE roles_permissions (
    org_id UUID NOT NULL,
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_roles_permissions
BEFORE INSERT OR UPDATE ON roles_permissions
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

CREATE TABLE orgs_members (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    CONSTRAINT uq_orgs_members UNIQUE (org_id, user_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_orgs_members
BEFORE INSERT OR UPDATE ON orgs_members
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

ALTER TABLE orgs_members
    ADD CONSTRAINT fk_orgs_members_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;
ALTER TABLE orgs_members
    ADD CONSTRAINT fk_orgs_members_users
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT
;
ALTER TABLE orgs_members
    ADD CONSTRAINT fk_orgs_members_roles
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
;

CREATE TABLE companies_members (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    CONSTRAINT uq_companies_members UNIQUE (org_id, company_id, user_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_companies_members
BEFORE INSERT OR UPDATE ON companies_members
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

ALTER TABLE companies_members
    ADD CONSTRAINT fk_companies_members_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;
ALTER TABLE companies_members
    ADD CONSTRAINT fk_companies_members_companies
        FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE RESTRICT
;
ALTER TABLE companies_members
    ADD CONSTRAINT fk_companies_members_users
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT
;
ALTER TABLE companies_members
    ADD CONSTRAINT fk_companies_members_roles
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
;

CREATE TABLE stores_members (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    CONSTRAINT uq_stores_members UNIQUE (org_id, store_id, user_id),
    date_created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER set_timestamp_roles_permissions
BEFORE INSERT OR UPDATE ON stores_members
FOR EACH ROW EXECUTE FUNCTION set_timestamp();

ALTER TABLE stores_members
    ADD CONSTRAINT fk_stores_members_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;
ALTER TABLE stores_members
    ADD CONSTRAINT fk_stores_members_stores
        FOREIGN KEY (store_id) REFERENCES stores (id) ON DELETE RESTRICT
;
ALTER TABLE stores_members
    ADD CONSTRAINT fk_orgs_members_users
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT
;
ALTER TABLE stores_members
    ADD CONSTRAINT fk_stores_members_roles
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
;

-- now change everything
ALTER TABLE users_audit
    ADD CONSTRAINT fk_users_audit_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE SET NULL
;
ALTER TABLE users_audit
    ADD CONSTRAINT fk_users_audit_users
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
;

ALTER TABLE roles_permissions
    ADD CONSTRAINT fk_roles_permissions_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;
ALTER TABLE roles_permissions
    ADD CONSTRAINT fk_roles_permissions_roles
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
;
ALTER TABLE roles_permissions
    ADD CONSTRAINT fk_roles_permissions_permissions
        FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE
;

ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;
ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_users
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
;
ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_roles
        FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
;
ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_divisions
        FOREIGN KEY (division_id) REFERENCES divisions (id) ON DELETE CASCADE
;
ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_companies
        FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
;
ALTER TABLE users_roles
    ADD CONSTRAINT fk_users_roles_stores
        FOREIGN KEY (store_id) REFERENCES stores (id) ON DELETE CASCADE
;

ALTER TABLE permissions
    ADD CONSTRAINT fk_permissions_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE chart_of_accounts_sales_account_categories
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_chart_of_accounts
        FOREIGN KEY (chart_of_accounts_id) REFERENCES chart_of_accounts(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account_categories
        FOREIGN KEY (sales_account_category_id) REFERENCES sales_account_categories(id) ON DELETE CASCADE
;

ALTER TABLE chart_of_accounts_cog_account_categories
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_organizations
        foreign key (org_id) references organizations (id) on delete restrict,
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart_of_accounts
        foreign key (chart_of_accounts_id) references chart_of_accounts (id) on delete restrict,
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_cog_account_categories
        FOREIGN KEY (cog_account_category_id) REFERENCES cog_account_categories (id) ON DELETE CASCADE
;

ALTER TABLE sales_account_categories_sales_accounts
    ADD CONSTRAINT fk_sales_account_categories_sales_accounts_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id),
    ADD CONSTRAINT fk_sales_account_categories_sales_accounts_category
        FOREIGN KEY (sales_account_category_id) REFERENCES sales_account_categories (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
        FOREIGN KEY (sales_account_id) REFERENCES sales_accounts (id) ON DELETE CASCADE
;

ALTER TABLE cog_accounts
    ADD CONSTRAINT fk_cog_accounts_cog_account_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_cog_accounts_cog_account_categories
        FOREIGN KEY (cog_account_category_id) REFERENCES cog_account_categories (id) ON DELETE RESTRICT
;

ALTER TABLE menus
    ADD CONSTRAINT fk_menus_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_menus_sales_account
        FOREIGN KEY (sales_account_id) REFERENCES sales_accounts (id) ON DELETE RESTRICT
;

ALTER TABLE menus_recipes_plated
    ADD CONSTRAINT fk_menus_recipes_plated_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_menus_recipes_plated_menus
        FOREIGN KEY (menu_id) REFERENCES menus (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_menus_recipes_plated_recipes_plated
        FOREIGN KEY (recipe_plated_id) REFERENCES recipes_plated (id) ON DELETE CASCADE
;

ALTER TABLE recipes_plated_recipes_nested
    ADD CONSTRAINT fk_recipes_plated_recipes_nested_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_recipes_plated_recipes_nested_recipes_plated
        FOREIGN KEY (recipe_plated_id) REFERENCES recipes_plated (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_recipes_nested_recipes_nested_recipes_nested
        FOREIGN KEY (recipe_nested_id) REFERENCES recipes_nested (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_recipes_plated_ingredients_types_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_recipes_plated_ingredients_types_recipes_plated
        FOREIGN KEY (recipe_plated_id) REFERENCES recipes_plated (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_ingredients_types_ingredients_types_ingredient_types
        FOREIGN KEY (ingredient_type_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
;

-- -- recipes_nested_ingredients_types
ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_recipes_nested_ingredients_types_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_recipes_nested_ingredients_types_recipes_nested
        FOREIGN KEY (recipe_nested_id) REFERENCES recipes_nested (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_ingredients_types_ingredients_types_ingredient_types
        FOREIGN KEY (ingredient_type_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
;

ALTER TABLE ingredients_types
    ADD CONSTRAINT fk_ingredient_types_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_ingredients_types_cog_account
        FOREIGN KEY (cog_account_id) REFERENCES cog_accounts (id) ON DELETE RESTRICT
;

ALTER TABLE ingredients_types
    ADD CONSTRAINT fk_ingredients_types_preferred_ingredient
        FOREIGN KEY (preferred_ingredient_item_id) REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT
;

ALTER TABLE ingredients_types
    ADD CONSTRAINT fk_ingredients_types_current_ingredient
        FOREIGN KEY (current_ingredient_item_id) REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
;

-- -- ingredients_vendor_items
ALTER TABLE ingredients_vendor_items
    ADD CONSTRAINT fk_ingredients_vendor_items_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE ingredients_vendor_items
    ADD CONSTRAINT fk_ingredients_vendor_items_ingredients_type
        FOREIGN KEY (ingredient_type_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
;

ALTER TABLE ingredients_vendor_items
    ADD CONSTRAINT fk_ingredients_vendor_items_vendor
        FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated
    ADD CONSTRAINT fk_recipes_plated_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE recipes_nested
    ADD CONSTRAINT fk_recipes_nested_organization
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE vendors
    ADD CONSTRAINT fk_vendors_organization
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE chart_of_accounts
    ADD CONSTRAINT fk_chart_of_accounts_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE sales_account_categories
    ADD CONSTRAINT fk_sales_account_categories_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE sales_accounts
    ADD CONSTRAINT fk_sales_accounts_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE cog_account_categories
    ADD CONSTRAINT fk_cog_account_categories_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE users_stores
    ADD CONSTRAINT fk_users_stores_org_id
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_users_stores_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_users_stores_store_id
        FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
;

ALTER TABLE stores
    ADD CONSTRAINT fk_stores_organization
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_stores_companies
        FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_stores_chart_of_accounts
        FOREIGN KEY (chart_of_accounts_id) REFERENCES chart_of_accounts(id) ON DELETE RESTRICT
;

ALTER TABLE stores_menus
    ADD CONSTRAINT fk_stores_menus_menus
        FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_stores_menus_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
;

ALTER TABLE divisions
    ADD CONSTRAINT fk_divisions_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE
;