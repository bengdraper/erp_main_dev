<!-- implement data types DONE -->
<!-- ## add ID to all tables in erd; update vendor attributes -->

<!-- implement bridge tables DONE -->
<!-- add detail at bridge tables with extra attributes DONE -->
<!-- implement all constraints @ all tables /...done
implement on delete constraints @ll done
review all constraints for for associated cols don
create schema migration script
deploy schema to postgres
create seed data script
seed db -->

## ***** DB CATEGORY DOMAINS AND CONTROLS

TABLE users

    TABLE users
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        permissions INT NOT NULL,
        name TEXT NOT NULL,
        date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        company_id INT NOT NULL,

        CONSTRAINT fk_users_company
        FOREIGN KEY (company_id)
        REFERENCES companies (id) ON DELETE SET NULL
    ;

    @company
        / users n:1 company /many to one
        f_key company_id references companies (id)
    @stores
        / users n:n stores /many to many
        *bridge table users_stores

BRIDGE TABLE users_stores

    BRIDGE TABLE users_stores
        user_id INT,
        store_id INT,
        PRIMARY KEY (user_id, store_id),

        CONSTRAINT fk_users_stores_user
        FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE CASCADE,

        CONSTRAINT fk_users_stores_store
        FOREIGN KEY (store_id)
        REFERENCES stores (id) ON DELETE CASCADE
    ;

TABLE companies

    TABLE companies
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    ;

    @users
        / companies 1:n users / one to many
        none
    @stores
        / companies 1:n stores / one company to many stores
        none

TABLE stores

    TABLE stores
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        company_id INT NOT NULL,
        chart_of_accounts_id INT NOT NULL DEFAULT 1,

        CONSTRAINT fk_stores_companies
        FOREIGN KEY (company_id)
        REFERENCES companies (id) ON DELETE RESTRICT,

        CONSTRAINT fk_stores_chart_of_accounts
        FOREIGN KEY (chart_of_accounts_id)
        REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
    ;

    @companies
        / stores n:1 companies
        f_key company_id FOREIGN KEY references companies (id)
    @users
        / stores n:n users 
        *bridge table users_stores
    @chart_of_accounts
        / stores n:1 chart_of_accounts
        f_key chart_of_accounts_id FOREIGN KEY references chart_of_accounts (id)
    @menus
        / stores n:n menus
        *bridge table stores_menus

BRIDGE TABLE stores_menus

    BRIDGE TABLE stores_menus
        store_id INT,
        menu_id INT,
        PRIMARY KEY (store_id, menu_id),

        CONSTRAINT fk_stores_menus_store
        FOREIGN KEY (store_id)
        REFERENCES stores (id) ON DELETE RESTRICT,

        CONSTRAINT fk_stores_menus_menu
        FOREIGN KEY (menu_id)
        REFERENCES menus (id) ON DELETE CASCADE
    ;

 ## ***** DB CATEGORY ACCOUNTS

TABLE chart_of_accounts

    TABLE chart_of_accounts
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL UNIQUE,
        date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ;

    @stores
        / chart_of_accounts 1:n stores
        none
    @sales_account_categories
        / chart_of_accounts n:n sales_account_categories
        *bridge table chart_of_accounts_sales_account_categories
    @cog_account_categories
        / chart_of_accounts n:n cog_account_categories
        *bridge table chart_of_accounts_cog_account_categories

BRIDGE TABLE chart_of_accounts_sales_account_categories

    BRIDGE TABLE chart_of_accounts_sales_account_categories

        chart_of_accounts_id INT,
        sales_account_categories_id INT,

        PRIMARY KEY (chart_of_accounts_id, sales_account_categories_id),

        CONSTRAINT fk_chart_of_accounts_sales_categories_chart
        FOREIGN KEY (chart_of_accounts_id)
        REFERENCS chart_of_accounts (id) ON DELETE RESTRICT,

        CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
        FOREIGN KEY (sales_account_categories_id)
        REFERENCS sales_account_categories (id) ON DELETE CASCADE
    ;

BRIDGE TABLE chart_of_accounts_cog_account_categories

    BRIDGE TABLE chart_of_accounts_cog_account_categories
        chart_of_accounts_id INT,
        cog_account_categories_id INT,
        PRIMARY KEY (chart_of_accounts_id, cog_account_categories_id),

        CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
        FOREIGN KEY (chart_of_accounts_id)
        REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

        CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
        FOREIGN KEY (cog_account_categories_id)
        REFERENCES cog_account_categories (id) ON DELETE CASCADE

    ;

TABLE sales_account_categories

    TABLE sales_account_categories
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL UNIQUE,
        account_number TEXT NOT NULL UNIQUE
    ;

    @chart_of_accounts
        / sales_account_categories n:n chart_of_accounts
        *bridge table chart_of_accounts_sales_account_categories
    @sales_accounts
        / sales_account_categories n:n sales_accounts
        *bridge table sales_account_categories_sales_accounts
    @menus
        sales_account_categories 1:n menus
        none

BRIDGE TABLE sales_account_categories_sales_accounts

    BRIDGE TABLE sales_account_categories_sales_accounts
        sales_account_categories_id INT,
        sales_accounts_id INT,
        PRIMARY KEY (sales_account_categories_id, sales_accounts_id),

        CONSTRAINT fk_sales_account_categories_sales_accounts_category
        FOREIGN KEY (sales_account_categories_id)
        REFERENCES sales_account_categories (id) ON DELETE RESTRICT,

        CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
        FOREIGN KEY (sales_accounts_id)
        REFERENCES sales_accounts (id) ON DELETE CASCADE
    ;

TABLE sales_accounts

    TABLE sales_accounts
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL UNIQUE,
        account_number NUMERIC NOT NULL UNIQUE
    ;

    @sales_account_categories
        / sales_accounts n:1 sales_account_categories
        *bridge table sales_account_categories_sales_accounts
    @menus
        / sales_accounts 1:n menus
        none

TABLE cog_account_categories

    TABLE cog_account_categories
        primary key id SERIAL,
        description TEXT NOT NULL UNIQUE,
        account_number NUMERIC NOT NULL UNIQUE
    ;

    @chart_of_accounts
        / cog_account_categories n:n chart_of_accounts
        *bridge table chart_of_accounts_cog_account_categories
    @cog_account
        / cog_account_categories 1:n cog_account
        none

TABLE cog_accounts

    TABLE cog_accounts
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL UNIQUE,
        account_number TEXT NOT NULL UNIQUE

        cog_account_category_id INT NOT NULL

        CONSTRAINT fk_cog_accounts_cog_account_category
        FOREIGN KEY (cog_account_category_id)
        REFERENCES cog_account_categories (id) ON DELETE RESTRICT
    ;

    @cog_account_categories
        / cog_accounts n:1 cog_account_categories
        fk_cog_account_category_id not null
    @ingredient_type
        / cog_accounts 1:n ingredient_types
        none


## ***** MENU / RECIPE

TABLE menus

    TABLE menus
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL UNIQUE

        sales_account_id NUMERIC

        CONSTRAINT fk_menus_sales_account
        FOREIGN KEY sales_account_id
        REFERENCES sales_account (id)
        ON DELETE RESTRICT
    ;


    @stores
        / menus n:n stores
        *bridge table stores_menus
    @recipes_plated
        / menus n:n recipes_plated
        *bridge table menus_recipes_plated
    @sales_account_categories
        / menus n:1 sales_accounts_categories
        fk_menus_sales_accounts_category id not null


<!-- BRIDGE TABLE stores_menus

    BRIDGE TABLE stores_menus
        store_id INT,
        menu_id INT,
        PRIMARY KEY (store_id, menu_id),
        CONSTRAINT f_key store_id FOREIGN KEY REFERENCES stores (id) ON DELETE SET RESTRICT,
        CONSTRAINT f_key menu_id FOREIGN KEY REFERENCES menus (id) ON DELETE CASCADE
    ; -->

BRIDGE TABLE menus_recipes_plated

    BRIDGE TABLE menus_recipes_plated
        menu_id INT,
        recipes_plated_id INT,
        PRIMARY KEY (menu_id, recipes_plated_id),

        CONSTRAINT fk_menus_recipes_plated_menus
        FOREIGN KEY (menu_id)
        REFERENCES menus (id) ON DELETE RESTRICT,

        CONSTRAINT fk_menus_recipes_plated_recipes_plated
        FOREIGN KEY (recipes_plated_id)
        REFERENCES recipes_plated (id) ON DELETE RESTRICT
    ;

TABLE recipes_plated

    TABLE recipes_plated
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        notes TEXT NOT NULL,
        recipe_type TEXT,
        sales_price_basis numeric NOT NULL
    ;

    @menus
        / recipes_plated n:n menus
        *bridge table menus_recipes_plated
    @recipes_nested
        / recipes_plated n:n recipes_nested
        *bridge table recipes_plated_recipes_nested
    @ingredient_types  // *bridge recipe_ingredients
        / recipes_plated n:n ingredient_types
        *bridge table recipes_plated_ingredients_types

BRIDGE TABLE recipes_plated_recipes_nested

    BRIDGE TABLE recipes_plated_recipes_nested
        recipes_plated_id INT,
        recipes_nested_id INT,
        PRIMARY KEY (recipes_plated_id, recipes_nested_id),

        CONSTRAINT fk_recipes_plated_recipes_nested_plated
        FOREIGN KEY (recipes_plated_id)
        REFERENCES recipes_plated (id) ON DELETE RESTRICT,

        CONSTRAINT fk_recipes_nested_recipes_nested_nested
        FOREIGN KEY (recipes_nested_id)
        REFERENCES recipes_nested (id) ON DELETE RESTRICT
    ;

BRIDGE TABLE recipes_plated_ingredients_types

    BRIDGE TABLE recipes_plated_ingredients_types
        recipes_plated_id INT,
        ingredients_types_id INT,

        ingredient_quantity numeric NOT NULL,
        ingredient_uom TEXT NOT NULL,
        ingredient_cost numeric NOT NULL,

        PRIMARY KEY (recipes_plated_id, ingredients_types_id),

        CONSTRAINT fk_recipes_plated_ingredients_types_recipe
        FOREIGN KEY (recipes_plated_id)
        REFERENCES recipes_plated (id) ON DELETE RESTRICT,

        CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
        FOREIGN KEY (ingredients_types_id)
        REFERENCES ingredients_types (id) ON DELETE RESTRICT
    ;

TABLE recipes_nested  // note: this routes nested as ingredient direct to plated: // likely transition later route through vendors as local vendor 

    TABLE recipes_nested  
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        notes TEXT,
        recipe_type TEXT,
        yield numeric NOT NULL,
        yield_uom TEXT NOT NULL
    ;

    @recipes_plated
        / recipes_nested n:n recipes_plated
        *bridge table recipes_plated_recipes_nested
    @ingredient_types  // recipe_ingredients
        / recipes_nested n:n ingredient_types
        *bridge table recipes_nested_ingredients_types

BRIDGE TABLE recipes_nested_ingredients_types

    BRIDGE TABLE recipes_nested_ingredients_types
        recipes_nested_id INT,
        ingredients_types_id INT,

        ingredient_quantity numeric NOT NULL,
        ingredient_uom TEXT NOT NULL,
        ingredient_cost numeric NOT NULL,

        PRIMARY KEY (recipes_nested_id, ingredients_types_id),

        CONSTRAINT fk_recipes_nested_ingredients_types_recipe
        FOREIGN KEY (recipes_nested_id)
        REFERENCES recipes_nested (id) ON DELETE RESTRICT,

        CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
        FOREIGN KEY (ingredients_types_id)
        REFERENCES ingredients_types (id) ON DELETE RESTRICT
    ;


## ***** CATEGORY PRODUCT

TABLE ingredients_types

    TABLE ingredients_types
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL UNIQUE,
        unit_cost numeric NOT NULL,
        unit_of_measure TEXT NOT NULL,

        cog_account_id INT NOT NULL,
        preferred_ingredient_item_id INT,
        current_ingredient_item_id INT,

        CONSTRAINT fk_ingredients_types_cog_account
        FOREIGN KEY (cog_account_id)
        REFERENCES cog_accounts (id) ON DELETE RESTRICT,

        CONSTRAINT fk_ingredients_types_preferred_ingredient
        FOREIGN KEY (preferred_ingredient_item_id)
        REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT,

        CONSTRAINT fk_ingredients_types_current_ingredient
        FOREIGN KEY (current_ingredient_item_id)
        REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
    ;

    @recipes_plated
        / ingredients_types n:n recipes_plated
        *bridge table recipes_plated_ingredients_types
    @recipes_nested
        / ingredients_types n:n recipes_nested
        *bridge table recipes_nested_ingredients_types
    @cog_accounts
        / ingredients_types n:1 cog_accounts
        f_key cog_account_id references cog_accounts (id)
    @ingredients_vendor_items
        / ingredients_types 1:n ingredients_vendor_items
        none
    @ingredients_vendor_items
        @ingredients_types 1:1 ingredients_vendor_items  // ???
        f_key preferred_ingredient_item_id references ingredients_vendor_items (id)
            // preferred ingredient_item for this type
            // must exist in list of ingredients associated with current type
    @ ingredients_vendor_items
        @ingredients_types 1:1 ingredients_vendor_items  // ???
        f_key current_ingredient_item_id references ingredients_vendor_items (id)

TABLE ingredients_vendor_items

    TABLE ingredients_vendor_items
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
        vendor_id INT NOT NULL,

        CONSTRAINT fk_ingredients_vendor_items_ingredients_type
        FOREIGN KEY (ingredients_type_id)
        REFERENCES ingredients_types (id) ON DELETE RESTRICT,

        CONSTRAINT fk_ingredients_vendor_items_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors (id) ON DELETE RESTRICT
    ;

    @ingredients_types
        / ingredients_vendor_items n:1 ingredients_types
        f_key ingredients_type_id references ingredients_types (id)
    @vendors
        / ingredients_vendor_items n:1 vendors
        f_key vendor_id references vendors (id)

TABLE vendors

    TABLE vendors
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
    ;

