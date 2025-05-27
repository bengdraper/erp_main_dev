"""
Instructions to run this script:

1. Ensure the PostgreSQL database container is running:
   docker start pg_container

2. Verify the database connection details in your Flask configuration file (e.g., `config.py`).
   Ensure the database URI points to the `menus_project` database.

3. Run the script using the following command:
   python seed.py

4. If you encounter any issues, check the logs for errors and ensure the database schema matches the models defined in `models.py`.
"""

# Adjust the Python module search path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.menus_api_flask.menus.menus_app.src.models.models import db, User, Company, Store, Vendor, Menu, RecipeNested, RecipePlated, IngredientType, RecipesNested_IngredientsTypes, RecipesPlated_IngredientsTypes, RecipesPlated_RecipesNested, ChartOfAccounts, SalesAccountCategory, CogAccountCategory
from src import app

from datetime import datetime
from sqlalchemy.sql import text

# Wrap database operations in application context
with app.app_context():
    # Seed company
    company = Company(name='Example Company')
    db.session.add(company)

    # Updated User seed data to include the `company_id` field
    users = [
        User(email='user1@example.com', password='password1', permissions=1, name='User One', company_id=company.id),
        User(email='user2@example.com', password='password2', permissions=1, name='User Two', company_id=company.id),
        User(email='user3@example.com', password='password3', permissions=1, name='User Three', company_id=company.id)
    ]
    db.session.bulk_save_objects(users)

    # Seed chart of accounts
    chart_of_accounts = ChartOfAccounts(description='Main Chart of Accounts')
    db.session.add(chart_of_accounts)

    # Seed store
    store = Store(name='Example Store', company_id=company.id, chart_of_accounts_id=chart_of_accounts.id)
    db.session.add(store)

    # Seed sales account categories
    sales_account_categories = [
        SalesAccountCategory(description='Food Sales', account_number='4100'),
        SalesAccountCategory(description='Alcohol Sales', account_number='4200')
    ]
    db.session.bulk_save_objects(sales_account_categories)

    # Seed cost of goods account categories
    cog_account_categories = [
        CogAccountCategory(description='Food Cost', account_number='5100'),
        CogAccountCategory(description='Alcohol Cost', account_number='5200')
    ]
    db.session.bulk_save_objects(cog_account_categories)

    # Link chart of accounts to sales account categories
    chart_of_accounts_sales_links = [
        {'chart_of_accounts_id': chart_of_accounts.id, 'sales_account_categories_id': category.id}
        for category in sales_account_categories
    ]
    db.session.execute(
        text("INSERT INTO chart_of_accounts_sales_account_categories (chart_of_accounts_id, sales_account_categories_id) VALUES (:chart_of_accounts_id, :sales_account_categories_id)"),
        chart_of_accounts_sales_links
    )

    # Link chart of accounts to cost of goods account categories
    chart_of_accounts_cog_links = [
        {'chart_of_accounts_id': chart_of_accounts.id, 'cog_account_categories_id': category.id}
        for category in cog_account_categories
    ]
    db.session.execute(
        text("INSERT INTO chart_of_accounts_cog_account_categories (chart_of_accounts_id, cog_account_categories_id) VALUES (:chart_of_accounts_id, :cog_account_categories_id)"),
        chart_of_accounts_cog_links
    )

    # Seed vendors
    vendors = [
        Vendor(name='Vendor 1', contact_name='Alice', contact_email='alice@vendor1.com', contact_phone='123-456-7890', delivery_days='Mon, Wed, Fri', order_days='Sun, Tue', order_cutoff_time='5 PM', terms='Net 30', notes='Reliable vendor for vegetables', date_created=datetime.now()),
        Vendor(name='Vendor 2', contact_name='Bob', contact_email='bob@vendor2.com', contact_phone='987-654-3210', delivery_days='Tue, Thu', order_days='Mon, Wed', order_cutoff_time='3 PM', terms='Net 15', notes='Specializes in meat products', date_created=datetime.now())
    ]
    db.session.bulk_save_objects(vendors)

    # Seed menu
    menu = Menu(name='Main Menu', description='Primary menu for the store', store_id=store.id, date_created=datetime.now())
    db.session.add(menu)

    # Seed recipes
    burger_sauce = RecipeNested(name='Burger Sauce', description='Tangy sauce for burgers', menu_id=menu.id, date_created=datetime.now())
    salad_dressing = RecipeNested(name='Salad Dressing', description='Light dressing for salads', menu_id=menu.id, date_created=datetime.now())

    burger_recipe = RecipePlated(name='Classic Burger', description='Beef burger with lettuce and tomato', menu_id=menu.id, date_created=datetime.now())
    salad_recipe = RecipePlated(name='Garden Salad', description='Fresh salad with greens and dressing', menu_id=menu.id, date_created=datetime.now())

    nested_recipes = [burger_sauce, salad_dressing]
    recipes = [burger_recipe, salad_recipe]

    db.session.bulk_save_objects(nested_recipes + recipes)

    # Updated seed data to reflect the relationship between IngredientType and Vendor Ingredients

    # Seed ingredient types
    ingredient_types = [
        IngredientType(description='Burger Bun', unit_cost=0.5, unit_of_measure='piece'),
        IngredientType(description='Special Sauce', unit_cost=1.0, unit_of_measure='bottle'),
        IngredientType(description='Cheddar Cheese', unit_cost=2.0, unit_of_measure='kg'),
        IngredientType(description='Ground Beef', unit_cost=5.0, unit_of_measure='kg')
    ]
    db.session.bulk_save_objects(ingredient_types)

    # Ensure all recipes have associated ingredient types

    # Add missing ingredient types for all recipe ingredients
    ingredient_types.extend([
        IngredientType(description='Lettuce', unit_cost=0.2, unit_of_measure='kg'),
        IngredientType(description='Tomato', unit_cost=0.3, unit_of_measure='kg'),
        IngredientType(description='Beef Patty', unit_cost=3.0, unit_of_measure='piece'),
        IngredientType(description='Salad Greens', unit_cost=0.5, unit_of_measure='kg')
    ])
    db.session.bulk_save_objects(ingredient_types)

    # Updated to use `Ingredients_VendorItem` instead of `Ingredient`

    # Seed vendor ingredients
    vendor_ingredients = [
        Ingredients_VendorItem(vendor_item_description='Homemade Burger Bun', purchase_unit='piece', purchase_unit_cost=0.5, split_case_count=10, split_case_cost=5.0, split_case_uom='box', split_case_uom_cost=0.5, notes='Freshly baked burger buns', vendor_id=1, ingredients_type_id=ingredient_types[0].id, date_created=datetime.now()),
        Ingredients_VendorItem(vendor_item_description='Bulk Cheddar', purchase_unit='kg', purchase_unit_cost=2.0, split_case_count=5, split_case_cost=10.0, split_case_uom='block', split_case_uom_cost=2.0, notes='High-quality cheddar cheese', vendor_id=2, ingredients_type_id=ingredient_types[2].id, date_created=datetime.now()),
        Ingredients_VendorItem(vendor_item_description='Organic Ground Beef', purchase_unit='kg', purchase_unit_cost=5.0, split_case_count=20, split_case_cost=100.0, split_case_uom='pack', split_case_uom_cost=5.0, notes='Grass-fed ground beef', vendor_id=2, ingredients_type_id=ingredient_types[3].id, date_created=datetime.now()),
        Ingredients_VendorItem(vendor_item_description='Signature Special Sauce', purchase_unit='bottle', purchase_unit_cost=1.0, split_case_count=12, split_case_cost=12.0, split_case_uom='box', split_case_uom_cost=1.0, notes='Tangy and creamy sauce', vendor_id=1, ingredients_type_id=ingredient_types[1].id, date_created=datetime.now())
    ]
    db.session.bulk_save_objects(vendor_ingredients)

    # Seed RecipesNested_IngredientsTypes relationships
    nested_ingredient_relationships = [
        RecipesNested_IngredientsTypes(recipes_nested_id=burger_sauce.id, ingredients_types_id=ingredient_types[0].id, ingredient_quantity=0.5, ingredient_uom='kg', ingredient_cost=0.5),
        RecipesNested_IngredientsTypes(recipes_nested_id=salad_dressing.id, ingredients_types_id=ingredient_types[0].id, ingredient_quantity=0.2, ingredient_uom='kg', ingredient_cost=0.2)
    ]

    # Update RecipesNested_IngredientsTypes relationships to include all ingredients
    nested_ingredient_relationships.extend([
        RecipesNested_IngredientsTypes(recipes_nested_id=burger_sauce.id, ingredients_types_id=ingredient_types[0].id, ingredient_quantity=0.1, ingredient_uom='kg', ingredient_cost=0.1),
        RecipesNested_IngredientsTypes(recipes_nested_id=salad_dressing.id, ingredients_types_id=ingredient_types[3].id, ingredient_quantity=0.2, ingredient_uom='kg', ingredient_cost=0.2)
    ])
    db.session.bulk_save_objects(nested_ingredient_relationships)

    # Seed RecipesPlatedIngredientsTypes relationships
    plated_ingredient_relationships = [
        RecipesPlated_IngredientsTypes(recipes_plated_id=burger_recipe.id, ingredients_types_id=ingredient_types[1].id, ingredient_quantity=1.0, ingredient_uom='kg', ingredient_cost=5.0),
        RecipesPlated_IngredientsTypes(recipes_plated_id=salad_recipe.id, ingredients_types_id=ingredient_types[0].id, ingredient_quantity=0.5, ingredient_uom='kg', ingredient_cost=0.5)
    ]

    # Update RecipesPlated_IngredientsTypes relationships to include all ingredients
    plated_ingredient_relationships.extend([
        RecipesPlated_IngredientsTypes(recipes_plated_id=burger_recipe.id, ingredients_types_id=ingredient_types[2].id, ingredient_quantity=1.0, ingredient_uom='piece', ingredient_cost=3.0),
        RecipesPlated_IngredientsTypes(recipes_plated_id=salad_recipe.id, ingredients_types_id=ingredient_types[3].id, ingredient_quantity=0.5, ingredient_uom='kg', ingredient_cost=0.5)
    ])
    db.session.bulk_save_objects(plated_ingredient_relationships)

    # Seed RecipesPlatedRecipesNested relationships
    plated_nested_relationships = [
        RecipesPlated_RecipesNested(recipes_plated_id=burger_recipe.id, recipes_nested_id=burger_sauce.id),
        RecipesPlated_RecipesNested(recipes_plated_id=salad_recipe.id, recipes_nested_id=salad_dressing.id)
    ]
    db.session.bulk_save_objects(plated_nested_relationships)

    # Commit all changes
    db.session.commit()
    print("Seed data created successfully.")