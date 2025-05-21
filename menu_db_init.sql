-- ** init db schema @ ./menu_db_init.sql
-- // i.e. run ...init.sql through docker to inst db from file
cat menu_db_init.sql | docker exec -i erp_postgres psql -U postgres -d erp_main


-- *** backup (for erp_main database in erp_postgres)
-- -- Dump the erp_main database to a file inside the container:
-- $ docker exec erp_postgres pg_dump --verbose --file /tmp/erp_main_dump.sql -U postgres erp_main

-- -- Copy the dump file from the container to the host:
-- $ docker cp erp_postgres:/tmp/erp_main_dump.sql ./erp_main_dump.sql

-- -- (Optional) Remove the dump file from the container after copying:
-- $ docker exec erp_postgres rm /tmp/erp_main_dump.sql

-- -- *** restore (for erp_main database in erp_postgres)
-- -- Copy the backup file from the host to the container:
-- $ docker cp ./erp_main_dump.sql erp_postgres:/tmp/erp_main_dump.sql

-- -- (Optional) Terminate other connections and drop/recreate the database:
-- $ docker exec -i erp_postgres psql -U postgres -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'erp_main' AND pid <> pg_backend_pid();"
-- $ docker exec -i erp_postgres psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS erp_main;"
-- $ docker exec -i erp_postgres psql -U postgres -d postgres -c "CREATE DATABASE erp_main;"

-- -- Restore the database from the dump file:
-- $ docker exec -i erp_postgres psql -U postgres -d erp_main -f /tmp/erp_main_dump.sql

-- -- (Optional) Remove the dump file from the container after restoring:
-- $ docker exec erp_postgres rm /tmp/erp_main_dump.sql


-- kill other connections
\c postgres
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'erp_main' AND pid <> pg_backend_pid();
-- (re)create the database
DROP DATABASE IF EXISTS erp_main;
CREATE DATABASE erp_main;
-- connect via psql
\c erp_main

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;


-- ## ***** DB CATEGORY DOMAINS AND CONTROLS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    permissions INT NOT NULL,
    name TEXT NOT NULL,
    date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company_id INT NOT NULL

    -- users
    -- CONSTRAINT fk_users_company
    -- FOREIGN KEY (company_id)
    -- REFERENCES companies (id) ON DELETE SET NULL

);

CREATE TABLE users_stores (
    user_id INT,
    store_id INT,
    PRIMARY KEY (user_id, store_id)

    -- users_stores
    -- CONSTRAINT fk_users_stores_user
    -- FOREIGN KEY (user_id)
    -- REFERENCES users (id) ON DELETE CASCADE,

    -- CONSTRAINT fk_users_stores_store
    -- FOREIGN KEY (store_id)
    -- REFERENCES stores (id) ON DELETE CASCADE
);

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    company_id INT NOT NULL,
    chart_of_accounts_id INT NOT NULL DEFAULT 1

    -- stores
    -- CONSTRAINT fk_stores_companies
    -- FOREIGN KEY (company_id)
    -- REFERENCES companies (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_stores_chart_of_accounts
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
);

CREATE TABLE stores_menus (
    store_id INT,
    menu_id INT,
    PRIMARY KEY (store_id, menu_id)

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
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chart_of_accounts_sales_account_categories (
    chart_of_accounts_id INT,
    sales_account_categories_id INT,
    PRIMARY KEY (chart_of_accounts_id, sales_account_categories_id)

    -- chart_of_accounts_sales_account_categories
    -- CONSTRAINT fk_chart_of_accounts_sales_categories_chart
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCS chart_of_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
    -- FOREIGN KEY (sales_account_categories_id)
    -- REFERENCS sales_account_categories (id) ON DELETE CASCADE
);

CREATE TABLE chart_of_accounts_cog_account_categories (
    chart_of_accounts_id INT,
    cog_account_categories_id INT,
    PRIMARY KEY (chart_of_accounts_id, cog_account_categories_id)

    -- chart_of_accounts_cog_account_categories
    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
    -- FOREIGN KEY (chart_of_accounts_id)
    -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

    -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
    -- FOREIGN KEY (cog_account_categories_id)
    -- REFERENCES cog_account_categories (id) ON DELETE CASCADE
);

CREATE TABLE sales_account_categories (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number TEXT NOT NULL UNIQUE
);

CREATE TABLE sales_account_categories_sales_accounts (
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
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE
);

CREATE TABLE cog_account_categories (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    account_number NUMERIC NOT NULL UNIQUE
);

CREATE TABLE cog_accounts (
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
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL UNIQUE,
    sales_account_id INT
);

-- this shouldnt be here>
-- CREATE TABLE stores_menus (
--     store_id INT,
--     menu_id INT,
--     PRIMARY KEY (store_id, menu_id)

--     -- stores_menus
--     -- CONSTRAINT f_key store_id REFERENCES stores (id) ON DELETE RESTRICT,
--     -- CONSTRAINT f_key menu_id REFERENCES menus (id) ON DELETE CASCADE
-- );
-- <

CREATE TABLE menus_recipes_plated (
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
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT NOT NULL,
    recipe_type TEXT,
    sales_price_basis numeric NOT NULL
);

CREATE TABLE recipes_plated_recipes_nested (
    recipes_plated_id INT,
    recipes_nested_id INT,
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
    recipes_plated_id INT,
    ingredients_types_id INT,

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
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    notes TEXT,
    recipe_type TEXT,
    yield numeric NOT NULL,
    yield_uom TEXT NOT NULL
);

CREATE TABLE recipes_nested_ingredients_types (
    recipes_nested_id INT,
    ingredients_types_id INT,

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

    -- users
    ALTER TABLE users ADD
    CONSTRAINT fk_users_company
    FOREIGN KEY (company_id)
    REFERENCES companies (id) ON DELETE SET NULL
    ;

    -- stores
    ALTER TABLE stores ADD
    CONSTRAINT fk_stores_companies
    FOREIGN KEY (company_id)
    REFERENCES companies (id) ON DELETE RESTRICT
    ;

    ALTER TABLE stores ADD
    CONSTRAINT fk_stores_chart_of_accounts
    FOREIGN KEY (chart_of_accounts_id)
    REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
    ;

    -- -- stores_menus
    ALTER TABLE stores_menus ADD
    CONSTRAINT fk_stores_menus_store
    FOREIGN KEY (store_id)
    REFERENCES stores (id) ON DELETE RESTRICT
    ;

    ALTER TABLE stores_menus ADD
    CONSTRAINT fk_stores_menus_menu
    FOREIGN KEY (menu_id)
    REFERENCES menus (id) ON DELETE CASCADE
    ;


    -- -- chart_of_accounts_sales_account_categories
    ALTER TABLE chart_of_accounts_sales_account_categories ADD
    CONSTRAINT fk_chart_of_accounts_sales_categories_chart
    FOREIGN KEY (chart_of_accounts_id)
    REFERENCES chart_of_accounts (id) ON DELETE RESTRICT
    ;

    ALTER TABLE chart_of_accounts_sales_account_categories ADD
    CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
    FOREIGN KEY (sales_account_categories_id)
    REFERENCES sales_account_categories (id) ON DELETE CASCADE
    ;

    -- -- chart_of_accounts_cog_account_categories
    ALTER TABLE chart_of_accounts_cog_account_categories ADD
    CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
    FOREIGN KEY (chart_of_accounts_id)
    REFERENCES chart_of_accounts (id) ON DELETE RESTRICT
    ;

    ALTER TABLE chart_of_accounts_cog_account_categories ADD
    CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
    FOREIGN KEY (cog_account_categories_id)
    REFERENCES cog_account_categories (id) ON DELETE CASCADE
    ;

    -- -- sales_account_categories_sales_accounts
    ALTER TABLE sales_account_categories_sales_accounts ADD
    CONSTRAINT fk_sales_account_categories_sales_accounts_category
    FOREIGN KEY (sales_account_categories_id)
    REFERENCES sales_account_categories (id) ON DELETE RESTRICT
    ;

    ALTER TABLE sales_account_categories_sales_accounts ADD
    CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
    FOREIGN KEY (sales_accounts_id)
    REFERENCES sales_accounts (id) ON DELETE CASCADE
    ;

    -- -- cog_accounts
    ALTER TABLE cog_accounts ADD
    CONSTRAINT fk_cog_accounts_cog_account_category
    FOREIGN KEY (cog_account_category_id)
    REFERENCES cog_account_categories (id) ON DELETE RESTRICT
    ;

    -- menus
    ALTER TABLE menus ADD
    CONSTRAINT fk_menus_sales_account
    FOREIGN KEY (sales_account_id)
    REFERENCES sales_accounts (id) ON DELETE RESTRICT;

    -- -- menus_recipes_plated
    ALTER TABLE menus_recipes_plated ADD
    CONSTRAINT fk_menus_recipes_plated_menus
    FOREIGN KEY (menu_id)
    REFERENCES menus (id) ON DELETE RESTRICT
    ;

    ALTER TABLE menus_recipes_plated ADD
    CONSTRAINT fk_menus_recipes_plated_recipes_plated
    FOREIGN KEY (recipes_plated_id)
    REFERENCES recipes_plated (id) ON DELETE RESTRICT
    ;

    -- -- recipes_plated_recipes_nested
    ALTER TABLE recipes_plated_recipes_nested ADD
    CONSTRAINT fk_recipes_plated_recipes_nested_plated
    FOREIGN KEY (recipes_plated_id)
    REFERENCES recipes_plated (id) ON DELETE RESTRICT
    ;

    ALTER TABLE recipes_plated_recipes_nested ADD
    CONSTRAINT fk_recipes_nested_recipes_nested_nested
    FOREIGN KEY (recipes_nested_id)
    REFERENCES recipes_nested (id) ON DELETE RESTRICT
    ;

    -- -- recipes_plated_ingredients_types
    ALTER TABLE recipes_plated_ingredients_types ADD
    CONSTRAINT fk_recipes_plated_ingredients_types_recipe
    FOREIGN KEY (recipes_plated_id)
    REFERENCES recipes_plated (id) ON DELETE RESTRICT
    ;

    ALTER TABLE recipes_plated_ingredients_types ADD
    CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    FOREIGN KEY (ingredients_types_id)
    REFERENCES ingredients_types (id) ON DELETE RESTRICT
    ;

    -- -- recipes_nested_ingredients_types
    ALTER TABLE recipes_nested_ingredients_types ADD
    CONSTRAINT fk_recipes_nested_ingredients_types_recipe
    FOREIGN KEY (recipes_nested_id)
    REFERENCES recipes_nested (id) ON DELETE RESTRICT
    ;

    ALTER TABLE recipes_nested_ingredients_types ADD
    CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    FOREIGN KEY (ingredients_types_id)
    REFERENCES ingredients_types (id) ON DELETE RESTRICT
    ;

    -- -- ingredients_types
    ALTER TABLE ingredients_types ADD
    CONSTRAINT fk_ingredients_types_cog_account
    FOREIGN KEY (cog_account_id)
    REFERENCES cog_accounts (id) ON DELETE RESTRICT
    ;

    ALTER TABLE ingredients_types ADD
    CONSTRAINT fk_ingredients_types_preferred_ingredient
    FOREIGN KEY (preferred_ingredient_item_id)
    REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT
    ;

    ALTER TABLE ingredients_types ADD
    CONSTRAINT fk_ingredients_types_current_ingredient
    FOREIGN KEY (current_ingredient_item_id)
    REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
    ;

    -- -- ingredients_vendor_items
    ALTER TABLE ingredients_vendor_items ADD
    CONSTRAINT fk_ingredients_vendor_items_ingredients_type
    FOREIGN KEY (ingredients_type_id)
    REFERENCES ingredients_types (id) ON DELETE RESTRICT
    ;

    ALTER TABLE ingredients_vendor_items ADD
    CONSTRAINT fk_ingredients_vendor_items_vendor
    FOREIGN KEY (vendor_id)
    REFERENCES vendors (id) ON DELETE RESTRICT
    ;
