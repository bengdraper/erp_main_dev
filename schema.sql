-- '''
-- todo:
-- - all org_id and fkey refs
-- - all fkey refs everywhere
-- - refactor 1 create table 1 alter table as possible
-- - clean bridge table on delete flows
-- - metadata cols any/all
-- - created / updated timestamps any/all
-- - review config settings for deployment states
-- - clean up dev comments
-- '''

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ## ***** DB CATEGORY DOMAINS AND CONTROLS
CREATE TABLE users (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company_id UUID,
    metadata JSONB DEFAULT '{}'::jsonb
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT

    -- users
    -- CONSTRAINT fk_users_company
    -- FOREIGN KEY (company_id)
    -- REFERENCES companies (id) ON DELETE SET NULL

);

CREATE TABLE users_stores (
    org_id UUID NOT NULL,
    user_id UUID NOT NULL,
    store_id UUID NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, store_id)
    -- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT

    -- users_stores
    -- CONSTRAINT fk_users_stores_user
    -- FOREIGN KEY (user_id)
    -- REFERENCES users (id) ON DELETE CASCADE,

    -- CONSTRAINT fk_users_stores_store
    -- FOREIGN KEY (store_id)
    -- REFERENCES stores (id) ON DELETE CASCADE
);

CREATE TABLE companies (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    metadata JSONB DEFAULT '{}'::jsonb
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
);

CREATE TABLE stores (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    company_id UUID NOT NULL,
    chart_of_accounts_id INT NOT NULL DEFAULT 1
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT,
    -- FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE RESTRICT,
    -- FOREIGN KEY (chart_of_accounts_id) REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT

    -- stores
    -- CONSTRAINT fk_stores_companies
    -- FOREIGN KEY (company_id)
    -- REFERENCES companies (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_stores_chart_of_accounts
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
);

CREATE TABLE stores_menus (
    org_id UUID NOT NULL,
    store_id UUID NOT NULL,
    menu_id INT NOT NULL,
    PRIMARY KEY (store_id, menu_id)
    -- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT

    -- stores_menus
    -- CONSTRAINT fk_stores_menus_store
    -- FOREIGN KEY (store_id)
    -- REFERENCES stores (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_stores_menus_menu
    -- FOREIGN KEY (menu_id)
    -- REFERENCES menus (id) ON DELETE CASCADE
);

-- --  ## ***** DB CATEGORY ACCOUNTS

CREATE TABLE chart_of_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
);

CREATE TABLE chart_of_accounts_sales_account_categories (
    org_id UUID NOT NULL,
    chart_of_accounts_id INT,
    sales_account_categories_id INT,
    PRIMARY KEY (chart_of_accounts_id, sales_account_categories_id)
    -- FOREIGN KEY (chart_of_accounts_id) REFERENCES chart_of_accounts(id) ON DELETE CASCADE
    -- FOREIGN KEY (sales_account_categories_id) REFERENCES sales_account_categories(id) ON DELETE RESTRICT
    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT
    -- chart_of_accounts_sales_account_categories
    -- CONSTRAINT fk_chart_of_accounts_sales_categories_chart
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
    -- FOREIGN KEY (sales_account_categories_id)
    -- REFERENCES sales_account_categories (id) ON DELETE CASCADE
);

CREATE TABLE chart_of_accounts_cog_account_categories (
    org_id UUID NOT NULL,
    chart_of_accounts_id INT,
    cog_account_categories_id INT,
    PRIMARY KEY (chart_of_accounts_id, cog_account_categories_id)

    -- FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
    -- FOREIGN KEY (cog_account_categories_id)
    -- REFERENCES cog_account_categories (id) ON DELETE CASCADE


    -- chart_of_accounts_cog_account_categories
    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
    -- FOREIGN KEY (cog_account_categories_id)
    -- REFERENCES cog_account_categories (id) ON DELETE CASCADE
);

CREATE TABLE sales_account_categories (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number TEXT NOT NULL UNIQUE
);

CREATE TABLE sales_account_categories_sales_accounts (
    org_id UUID NOT NULL,
    sales_account_categories_id INT,
    sales_accounts_id INT,
    PRIMARY KEY (sales_account_categories_id, sales_accounts_id)

    -- sales_account_categories_sales_accounts
    -- CONSTRAINT fk_sales_account_categories_sales_accounts_category
    -- FOREIGN KEY (sales_account_categories_id)
    -- REFERENCES sales_account_categories (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
    -- FOREIGN KEY (sales_accounts_id)
    -- REFERENCES sales_accounts (id) ON DELETE CASCADE
);

CREATE TABLE sales_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE
);

CREATE TABLE cog_account_categories (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE
);

CREATE TABLE cog_accounts (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number TEXT NOT NULL UNIQUE,
    cog_account_category_id INT NOT NULL

    -- cog_accounts
    -- CONSTRAINT fk_cog_accounts_cog_account_category
    -- FOREIGN KEY (cog_account_category_id)
    -- REFERENCES cog_account_categories (id) ON DELETE RESTRICT
);

-- ## ***** MENU / RECIPE

CREATE TABLE menus (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL UNIQUE,
    sales_account_id INT
);

CREATE TABLE menus_recipes_plated (
    org_id UUID NOT NULL,
    menu_id INT,
    recipes_plated_id INT,
    PRIMARY KEY (menu_id, recipes_plated_id)

    -- menus_recipes_plated
    -- CONSTRAINT fk_menus_recipes_plated_menus
    -- FOREIGN KEY (menu_id)
    -- REFERENCES menus (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_menus_recipes_plated_recipes_plated
    -- FOREIGN KEY (recipes_plated_id)
    -- REFERENCES recipes_plated (id) ON DELETE RESTRICT
);

CREATE TABLE recipes_plated (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT NOT NULL,
    recipe_type TEXT,
    sales_price_basis numeric NOT NULL
);

CREATE TABLE recipes_plated_recipes_nested (
    org_id UUID NOT NULL,
    recipes_plated_id INT NOT NULL,
    recipes_nested_id INT NOT NULL,
    PRIMARY KEY (recipes_plated_id, recipes_nested_id)

    -- recpes_plated_recipes_nested
    -- CONSTRAINT fk_recipes_plated_recipes_nested_plated
    -- FOREIGN KEY (recipes_plated_id)
    -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_recipes_nested_recipes_nested_nested
    -- FOREIGN KEY (recipes_nested_id)
    -- REFERENCES recipes_nested (id) ON DELETE RESTRICT
);

CREATE TABLE recipes_plated_ingredients_types (
    org_id UUID NOT NULL,
    recipes_plated_id INT NOT NULL,
    ingredients_types_id INT NOT NULL,

    ingredient_quantity numeric NOT NULL,
    ingredient_uom TEXT NOT NULL,
    ingredient_cost numeric NOT NULL,

    PRIMARY KEY (recipes_plated_id, ingredients_types_id)

    -- recpes_plated_ingredients_types
    -- CONSTRAINT fk_recipes_plated_ingredients_types_recipe
    -- FOREIGN KEY (recipes_plated_id)
    -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    -- FOREIGN KEY (ingredients_types_id)
    -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
);

CREATE TABLE recipes_nested (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT,
    recipe_type TEXT,
    yield numeric NOT NULL,
    yield_uom TEXT NOT NULL
);

CREATE TABLE recipes_nested_ingredients_types (
    org_id UUID NOT NULL,
    recipes_nested_id INT NOT NULL,
    ingredients_types_id INT NOT NULL,

    ingredient_quantity numeric NOT NULL,
    ingredient_uom TEXT NOT NULL,
    ingredient_cost numeric NOT NULL,

    PRIMARY KEY (recipes_nested_id, ingredients_types_id)

    -- recipes_nested_ingredients_types
    -- CONSTRAINT fk_recipes_nested_ingredients_types_recipe
    -- FOREIGN KEY (recipes_nested_id)
    -- REFERENCES recipes_nested (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    -- FOREIGN KEY (ingredients_types_id)
    -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
);

-- -- ## ***** CATEGORY PRODUCT

CREATE TABLE ingredients_types (
    org_id UUID NOT NULL,
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    unit_cost numeric NOT NULL,
    unit_of_measure TEXT NOT NULL,

    cog_account_id INT NOT NULL,
    preferred_ingredient_item_id INT,
    current_ingredient_item_id INT

    -- ingredients_types
    -- CONSTRAINT fk_ingredients_types_cog_account
    -- FOREIGN KEY (cog_account_id)
    -- REFERENCES cog_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_ingredients_types_preferred_ingredient
    -- FOREIGN KEY (preferred_ingredient_item_id)
    -- REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_ingredients_types_current_ingredient
    -- FOREIGN KEY (current_ingredient_item_id)
    -- REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
);

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
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    ingredients_type_id INT NOT NULL,
    vendor_id INT NOT NULL

    -- ingredients_vendor_items
    -- CONSTRAINT fk_ingredients_vendor_items_ingredients_type
    -- FOREIGN KEY (ingredients_type_id)
    -- REFERENCES ingredients_types (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_ingredients_vendor_items_vendor
    -- FOREIGN KEY (vendor_id)
    -- REFERENCES vendors (id) ON DELETE RESTRICT
);

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
    date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- roles and permissions

CREATE TABLE roles (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    UNIQUE (org_id, name)
);

CREATE TABLE permissions (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codename TEXT NOT NULL,
    description TEXT,
    UNIQUE (org_id, codename)
);


CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE divisions (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE
);

CREATE TABLE users_roles (
    org_id UUID NOT NULL,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    division_id UUID,
    company_id UUID,
    store_id UUID,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (division_id) REFERENCES divisions(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    UNIQUE (user_id, role_id, org_id, division_id, company_id, store_id)
);

CREATE TABLE roles_permissions (
    org_id UUID NOT NULL,
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

ALTER TABLE roles_permissions
    ADD CONSTRAINT fk_roles_permissions_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE permissions
    ADD CONSTRAINT fk_permissions_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE users
    ADD CONSTRAINT fk_users_company
        FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE SET NULL
;

ALTER TABLE chart_of_accounts_sales_account_categories
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_organizations
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_chart_of_accounts
        FOREIGN KEY (chart_of_accounts_id) REFERENCES chart_of_accounts(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account_categories
        FOREIGN KEY (sales_account_categories_id) REFERENCES sales_account_categories(id) ON DELETE CASCADE
;

ALTER TABLE chart_of_accounts_cog_account_categories
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_organizations
        foreign key (org_id) references organizations (id) on delete restrict,
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart_of_accounts
        foreign key (chart_of_accounts_id) references chart_of_accounts (id) on delete restrict,
    ADD CONSTRAINT fk_chart_of_accounts_cog_account_categories_cog_account_categories
        FOREIGN KEY (cog_account_categories_id) REFERENCES cog_account_categories (id) ON DELETE CASCADE
;

ALTER TABLE sales_account_categories_sales_accounts
    ADD CONSTRAINT fk_sales_account_categories_sales_accounts_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id),
    ADD CONSTRAINT fk_sales_account_categories_sales_accounts_category
        FOREIGN KEY (sales_account_categories_id) REFERENCES sales_account_categories (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
        FOREIGN KEY (sales_accounts_id) REFERENCES sales_accounts (id) ON DELETE CASCADE
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
        FOREIGN KEY (recipes_plated_id) REFERENCES recipes_plated (id) ON DELETE CASCADE
;

ALTER TABLE recipes_plated_recipes_nested
    ADD CONSTRAINT fk_recipes_plated_recipes_nested_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_recipes_plated_recipes_nested_recipes_plated
        FOREIGN KEY (recipes_plated_id) REFERENCES recipes_plated (id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_recipes_nested_recipes_nested_recipes_nested
        FOREIGN KEY (recipes_nested_id) REFERENCES recipes_nested (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_recipes_plated_ingredients_types_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_recipes_plated_ingredients_types_recipes_plated
        FOREIGN KEY (recipes_plated_id) REFERENCES recipes_plated (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_plated_ingredients_types
    ADD CONSTRAINT fk_ingredients_types_ingredients_types_ingredient_types
        FOREIGN KEY (ingredients_types_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
;

-- -- recipes_nested_ingredients_types
ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_recipes_nested_ingredients_types_organizations
        FOREIGN KEY (org_id) REFERENCES organizations (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_recipes_nested_ingredients_types_recipes_nested
        FOREIGN KEY (recipes_nested_id) REFERENCES recipes_nested (id) ON DELETE RESTRICT
;

ALTER TABLE recipes_nested_ingredients_types
    ADD CONSTRAINT fk_ingredients_types_ingredients_types_ingredient_types
        FOREIGN KEY (ingredients_types_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
;

-- -- ingredients_types
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
        FOREIGN KEY (ingredients_type_id) REFERENCES ingredients_types (id) ON DELETE RESTRICT
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