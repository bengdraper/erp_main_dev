# # models.py; here create models for flask to interact with database via orm.
# # So, orm models.  I think.
# # from flask_sqlalchemy import SQLAlchemy  # for database adapter
# import datetime
# from sqlalchemy.sql import text
# from datetime import timezone

# # instantiate db object from SQLAlchemy class
# # db = SQLAlchemy()
# from . import db

# # create User class as subclass of SQLAlchemy.Model
# # note class creates model for record in table 'users'; object instance of class == record

# # CLASS of table users; to create an object representing a user record, and interact with it
# class User(db.Model):
#     __tablename__ = 'users'

#     # instantiate attributes matching user table columns
#     # col id 
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(128), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     permissions = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String(128), nullable=False)
#     date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
#     # constraint fkey company id
#     # company_id = db.Column(db.Integer(128), nullable=False)
#     company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)

#     # relates to
#     # -- users
#     # -- CONSTRAINT fk_users_company
#     # -- FOREIGN KEY (company_id)
#     # -- REFERENCES companies (id) ON DELETE SET NULL

#     # create here object from user instance
#     def __init__(self, email: str, password: str, permissions: int, name: str, company_id: int):
#         self.email = email
#         self.password = password
#         self.permissions = 0
#         self.name = name
#         # self.date_updated = datetime.now(datetime.timezone.utc)
#         self.date_updated = datetime.datetime.utcnow()
#         self.company_id = company_id

#     # serialize this object instance to json for tranmssion
#     def serialize(self):
#         return {
#             'id': self.id,
#             'email': self.email,
#             'password': self.password,
#             'permissions': self.permissions,
#             'name': self.name,
#             'date_updated': self.date_updated.isoformat(),
#             'company_id': self.company_id
#         }

# # bridge
# # class UserStore(db.Model):
# #     __tablename__ = 'users_stores'

# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
# #     store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)

# #     def __init__(self, user_id: int, store_id: int):
# #         self.user_id = user_id
# #         self.store_id = store_id

# #     def serialize(self):
# #         return {
# #             'user_id': self.user_id,
# #             'store_id': self.store_id
# #         }

# db.Table(
#     'users_stores',
#     db.Column(
#         'user_id', db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         primary_key=True
#     ),
#     db.Column(
#         'store_id', db.Integer,
#         db.ForeignKey('stores.id', ondelete='CASCADE'),
#         primary_key=True
#     ),
#     db.Column(
#         'date_created', db.DateTime,
#         default=datetime.datetime.utcnow,
#         # default=datetime.now(datetime.timezone.utc)
#         nullable=False
#     )

#     # CREATE TABLE users_stores (
#     #     user_id INT,
#     #     store_id INT,
#     #     PRIMARY KEY (user_id, store_id)

#     #     -- users_stores
#     #     -- CONSTRAINT fk_users_stores_user
#     #     -- FOREIGN KEY (user_id)
#     #     -- REFERENCES users (id) ON DELETE CASCADE,

#     #     -- CONSTRAINT fk_users_stores_store
#     #     -- FOREIGN KEY (store_id)
#     #     -- REFERENCES stores (id) ON DELETE CASCADE
#     # );
# )

# class Company(db.Model):
#     __tablename__ = 'companies'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(128), unique=True, nullable=False)

#     def __init__(self, name: str):
#         self.name = name

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name
#         }

#     # CREATE TABLE companies (
#     #     id SERIAL PRIMARY KEY,
#     #     name TEXT NOT NULL UNIQUE
#     # );

# class Store(db.Model):
#     __tablename__ = 'stores'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(128), unique=True, nullable=False)
#     company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='RESTRICT'), nullable=False)
#     chart_of_accounts_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id', ondelete='SET DEFAULT'), nullable=False)

#     def __init__(self, name: str, company_id: int, chart_of_accounts_id: int):
#         self.name = name
#         self.company_id = company_id
#         self.chart_of_accounts_id = chart_of_accounts_id

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'company_id': self.company_id,
#             'chart_of_accounts_id': self.chart_of_accounts_id
#         }

#     # CREATE TABLE stores (
#     #     id SERIAL PRIMARY KEY,
#     #     name TEXT NOT NULL UNIQUE,
#     #     company_id INT NOT NULL,
#     #     chart_of_accounts_id INT NOT NULL DEFAULT 1

#     #     -- stores
#     #     -- CONSTRAINT fk_stores_companies
#     #     -- FOREIGN KEY (company_id)
#     #     #     REFERENCES companies (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_stores_chart_of_accounts
#     #     -- FOREIGN KEY (chart_of_accounts_id)
#     #     -- REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
#     # );


# db.Table(
#     'stores_menus',
#     db.Column(
#         'store_id', db.Integer,
#         db.ForeignKey('stores.id', ondelete='RESTRICT'),
#         primary_key=True
#     ),
#     db.Column(
#         'menu_id', db.Integer,
#         db.ForeignKey('menus.id', ondelete='CASCADE'),
#         primary_key=True
#     ),
#     db.Column(
#         'date_created', db.DateTime,
#         default=datetime.datetime.utcnow,
#         nullable=False
#     )
#     # CREATE TABLE stores_menus (
#     #     store_id INT,
#     #     menu_id INT,
#     #     PRIMARY KEY (store_id, menu_id)

#     #     -- stores_menus
#     #     -- CONSTRAINT fk_stores_menus_store
#     #     -- FOREIGN KEY (store_id)
#     #     -- REFERENCES stores (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_stores_menus_menu
#     #     -- FOREIGN KEY (menu_id)
#     #     -- REFERENCES menus (id) ON DELETE CASCADE
#     # );
# )

# # -- --  ## ***** DB CATEGORY ACCOUNTS

# class ChartOfAccounts(db.Model):
#     __tablename__ = 'chart_of_accounts'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

#     def __init__(self, description: str):
#         self.description = description

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'date_created': self.date_created.isoformat()
#         }

#     # CREATE TABLE chart_of_accounts (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#     # );



# db.Table(
#     'chart_of_accounts_sales_account_categories',
#     db.Column(
#         'chart_of_accounts_id', db.Integer,
#         db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'),
#         primary_key=True
#     ),
#     db.Column(
#         'sales_account_categories_id', db.Integer,
#         db.ForeignKey('sales_account_categories.id', ondelete='CASCADE'),
#         primary_key=True
#     )

#     # CREATE TABLE chart_of_accounts_sales_account_categories (
#     #     chart_of_accounts_id INT,
#     #     sales_account_categories_id INT,
#     #     PRIMARY KEY (chart_of_accounts_id, sales_account_categories_id)

#     #     -- chart_of_accounts_sales_account_categories
#     #     -- CONSTRAINT fk_chart_of_accounts_sales_categories_chart
#     #     -- FOREIGN KEY (chart_of_accounts_id)
#     #     -- REFERENCS chart_of_accounts (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
#     #     -- FOREIGN KEY (sales_account_categories_id)
#     #     -- REFERENCS sales_account_categories (id) ON DELETE CASCADE
#     # );

# )

# db.Table(
#     'chart_of_accounts_cog_account_categories',
#     db.Column(
#         'chart_of_accounts_id', db.Integer,
#         db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'),
#         primary_key=True
#     ),
#     db.Column(
#         'cog_account_categories_id', db.Integer,
#         db.ForeignKey('cog_account_categories.id', ondelete='CASCADE'),
#         primary_key=True
#     )

#     # CREATE TABLE chart_of_accounts_cog_account_categories (
#     #     chart_of_accounts_id INT,
#     #     cog_account_categories_id INT,
#     #     PRIMARY KEY (chart_of_accounts_id, cog_account_categories_id)

#     #     -- chart_of_accounts_cog_account_categories
#     #     -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
#     #     -- FOREIGN KEY (chart_of_accounts_id)
#     #     -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
#     #     -- FOREIGN KEY (cog_account_categories_id)
#     #     -- REFERENCES cog_account_categories (id) ON DELETE CASCADE
#     # );

# )


# class SalesAccountCategory(db.Model):
#     __tablename__ = 'sales_account_categories'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     account_number = db.Column(db.Text, unique=True, nullable=False)

#     def __init__(self, description: str, account_number: str):
#         self.description = description
#         self.account_number = account_number

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'account_number': self.account_number
#         }

#     # CREATE TABLE sales_account_categories (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     account_number TEXT NOT NULL UNIQUE
#     # );



# db.Table(
#     'sales_account_categories_sales_accounts',
#     db.Column(
#         'sales_account_categories_id', db.Integer,
#         db.ForeignKey('sales_account_categories.id', ondelete='RESTRICT'),
#         primary_key=True
#     ),
#     db.Column(
#         'sales_accounts_id', db.Integer,
#         db.ForeignKey('sales_accounts.id', ondelete='CASCADE'),
#         primary_key=True
#     )

#     # CREATE TABLE sales_account_categories_sales_accounts (
#     #     sales_account_categories_id INT,
#     #     sales_accounts_id INT,
#     #     PRIMARY KEY (sales_account_categories_id, sales_accounts_id)

#     #     -- sales_account_categories_sales_accounts
#     #     -- CONSTRAINT fk_sales_account_categories_sales_accounts_category
#     #     -- FOREIGN KEY (sales_account_categories_id)
#     #     -- REFERENCES sales_account_categories (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
#     #     -- FOREIGN KEY (sales_accounts_id)
#     #     -- REFERENCES sales_accounts (id) ON DELETE CASCADE
#     # );

# )

# class SalesAccount(db.Model):
#     __tablename__ = 'sales_accounts'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     account_number = db.Column(db.Numeric, unique=True, nullable=False)

#     def __init__(self, description: str, account_number: str):
#         self.description = description
#         self.account_number = account_number

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'account_number': self.account_number
#         }

#     # CREATE TABLE sales_accounts (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     account_number NUMERIC NOT NULL UNIQUE
#     # );

# class CogAccountCategory(db.Model):
#     __tablename__ = 'cog_account_categories'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     account_number = db.Column(db.Numeric, unique=True, nullable=False)

#     def __init__(self, description: str, account_number: str):
#         self.description = description
#         self.account_number = account_number

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'account_number': self.account_number
#         }

#     # CREATE TABLE cog_account_categories (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     account_number NUMERIC NOT NULL UNIQUE
#     # );

# class CogAccount(db.Model):
#     __tablename__ = 'cog_accounts'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     account_number = db.Column(db.Text, unique=True, nullable=False)
#     cog_account_category_id = db.Column(db.Integer, db.ForeignKey('cog_account_categories.id'), nullable=False)

#     def __init__(self, description: str, account_number: str, cog_account_category_id: int):
#         self.description = description
#         self.account_number = account_number
#         self.cog_account_category_id = cog_account_category_id

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'account_number': self.account_number,
#             'cog_account_category_id': self.cog_account_category_id
#         }

#     # CREATE TABLE cog_accounts (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     account_number TEXT NOT NULL UNIQUE,
#     #     cog_account_category_id INT NOT NULL

#     #     -- cog_accounts
#     #     -- CONSTRAINT fk_cog_accounts_cog_account_category
#     #     -- FOREIGN KEY (cog_account_category_id)
#     #     -- REFERENCES cog_account_categories (id) ON DELETE RESTRICT
#     # );

# # -- ## ***** MENU / RECIPE

# class Menu(db.Model):
#     __tablename__ = 'menus'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, unique=True, nullable=False)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     sales_account_id = db.Column(db.Integer, db.ForeignKey('sales_accounts.id'), nullable=True)

#     def __init__(self, name: str, description: str, sales_account_id: int):
#         self.name = name
#         self.description = description
#         self.sales_account_id = sales_account_id

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'sales_account_id': self.sales_account_id
#         }

#     # CREATE TABLE menus (
#     #     id SERIAL PRIMARY KEY,
#     #     name TEXT NOT NULL UNIQUE,
#     #     description TEXT NOT NULL UNIQUE,
#     #     sales_account_id INT
#     # );


# # bridge
# class Menus_RecipesPlated(db.Model):
#     __tablename__ = 'menus_recipes_plated'

#     menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), primary_key=True)
#     recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)

#     def __init__(self, menu_id: int, recipes_plated_id: int):
#         self.menu_id = menu_id
#         self.recipes_plated_id = recipes_plated_id

#     def serialize(self):
#         return {
#             'menu_id': self.menu_id,
#             'recipes_plated_id': self.recipes_plated_id
#         }

#     # CREATE TABLE menus_recipes_plated (
#     #     menu_id INT,
#     #     recipes_plated_id INT,
#     #     PRIMARY KEY (menu_id, recipes_plated_id)

#     #     -- menus_recipes_plated
#     #     -- CONSTRAINT fk_menus_recipes_plated_menus
#     #     -- FOREIGN KEY (menu_id)
#     #     -- REFERENCES menus (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_menus_recipes_plated_recipes_plated
#     #     -- FOREIGN KEY (recipes_plated_id)
#     #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT
#     # );

# class RecipePlated(db.Model):
#     __tablename__ = 'recipes_plated'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, nullable=False)
#     notes = db.Column(db.Text, nullable=False)
#     recipe_type = db.Column(db.Text, nullable=True)
#     sales_price_basis = db.Column(db.Numeric, nullable=False)

#     def __init__(self, description: str, notes: str, recipe_type: str, sales_price_basis: float):
#         self.description = description
#         self.notes = notes
#         self.recipe_type = recipe_type
#         self.sales_price_basis = sales_price_basis

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'notes': self.notes,
#             'recipe_type': self.recipe_type,
#             'sales_price_basis': self.sales_price_basis
#         }

#     # CREATE TABLE recipes_plated (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL,
#     #     notes TEXT NOT NULL,
#     #     recipe_type TEXT,
#     #     sales_price_basis numeric NOT NULL
#     # );


# # bridge
# class RecipesPlated_RecipesNested(db.Model):
#     __tablename__ = 'recipes_plated_recipes_nested'

#     recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)
#     recipes_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id'), primary_key=True)

#     def __init__(self, recipes_plated_id: int, recipes_nested_id: int):
#         self.recipes_plated_id = recipes_plated_id
#         self.recipes_nested_id = recipes_nested_id

#     def serialize(self):
#         return {
#             'recipes_plated_id': self.recipes_plated_id,
#             'recipes_nested_id': self.recipes_nested_id
#         }

#     # CREATE TABLE recipes_plated_recipes_nested (
#     #     recipes_plated_id INT,
#     #     recipes_nested_id INT,
#     #     PRIMARY KEY (recipes_plated_id, recipes_nested_id)

#     #     -- recpes_plated_recipes_nested
#     #     -- CONSTRAINT fk_recipes_plated_recipes_nested_plated
#     #     -- FOREIGN KEY (recipes_plated_id)
#     #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_recipes_nested_recipes_nested_nested
#     #     -- FOREIGN KEY (recipes_nested_id)
#     #     -- REFERENCES recipes_nested (id) ON DELETE RESTRICT
#     # );

# # bridge
# class RecipesPlated_IngredientsTypes(db.Model):
#     __tablename__ = 'recipes_plated_ingredients_types'

#     recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)
#     ingredients_types_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), primary_key=True)

#     ingredient_quantity = db.Column(db.Numeric, nullable=False)
#     ingredient_uom = db.Column(db.Text, nullable=False)
#     ingredient_cost = db.Column(db.Numeric, nullable=False)

#     def __init__(self, recipes_plated_id: int, ingredients_types_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
#         self.recipes_plated_id = recipes_plated_id
#         self.ingredients_types_id = ingredients_types_id
#         self.ingredient_quantity = ingredient_quantity
#         self.ingredient_uom = ingredient_uom
#         self.ingredient_cost = ingredient_cost

#     def serialize(self):
#         return {
#             'recipes_plated_id': self.recipes_plated_id,
#             'ingredients_types_id': self.ingredients_types_id,
#             'ingredient_quantity': self.ingredient_quantity,
#             'ingredient_uom': self.ingredient_uom,
#             'ingredient_cost': self.ingredient_cost
#         }

#     # CREATE TABLE recipes_plated_ingredients_types (
#     #     recipes_plated_id INT,
#     #     ingredients_types_id INT,

#     #     ingredient_quantity numeric NOT NULL,
#     #     ingredient_uom TEXT NOT NULL,
#     #     ingredient_cost numeric NOT NULL,

#     #     PRIMARY KEY (recipes_plated_id, ingredients_types_id)

#     #     -- recpes_plated_ingredients_types
#     #     -- CONSTRAINT fk_recipes_plated_ingredients_types_recipe
#     #     -- FOREIGN KEY (recipes_plated_id)
#     #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
#     #     -- FOREIGN KEY (ingredients_types_id)
#     #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
#     # );

# class RecipeNested(db.Model):
#     __tablename__ = 'recipes_nested'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, nullable=False)
#     notes = db.Column(db.Text, nullable=False)
#     recipe_type = db.Column(db.Text, nullable=True)
#     yield_amount = db.Column(db.Numeric, nullable=False)
#     yield_uom = db.Column(db.Text, nullable=False)

#     def __init__(self, description: str, notes: str, recipe_type: str, yield_amount: float, yield_uom: str):
#         self.description = description
#         self.notes = notes
#         self.recipe_type = recipe_type
#         self.yield_amount = yield_amount
#         self.yield_uom = yield_uom

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'notes': self.notes,
#             'recipe_type': self.recipe_type,
#             'yield_amount': self.yield_amount,
#             'yield_uom': self.yield_uom
#         }

#     # CREATE TABLE recipes_nested (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL,
#     #     notes TEXT,
#     #     recipe_type TEXT,
#     #     yield numeric NOT NULL,
#     #     yield_uom TEXT NOT NULL
#     # );


# # bridge
# class RecipesNested_IngredientsTypes(db.Model):
#     __tablename__ = 'recipes_nested_ingredients_types'

#     recipes_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id'), primary_key=True)
#     ingredients_types_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), primary_key=True)

#     ingredient_quantity = db.Column(db.Numeric, nullable=False)
#     ingredient_uom = db.Column(db.Text, nullable=False)
#     ingredient_cost = db.Column(db.Numeric, nullable=False)

#     def __init__(self, recipes_nested_id: int, ingredients_types_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
#         self.recipes_nested_id = recipes_nested_id
#         self.ingredients_types_id = ingredients_types_id
#         self.ingredient_quantity = ingredient_quantity
#         self.ingredient_uom = ingredient_uom
#         self.ingredient_cost = ingredient_cost

#     def serialize(self):
#         return {
#             'recipes_nested_id': self.recipes_nested_id,
#             'ingredients_types_id': self.ingredients_types_id,
#             'ingredient_quantity': self.ingredient_quantity,
#             'ingredient_uom': self.ingredient_uom,
#             'ingredient_cost': self.ingredient_cost
#         }

#     # CREATE TABLE recipes_nested_ingredients_types (
#     #     recipes_nested_id INT,
#     #     ingredients_types_id INT,

#     #     ingredient_quantity numeric NOT NULL,
#     #     ingredient_uom TEXT NOT NULL,
#     #     ingredient_cost numeric NOT NULL,

#     #     PRIMARY KEY (recipes_nested_id, ingredients_types_id)

#     #     -- recipes_nested_ingredients_types
#     #     -- CONSTRAINT fk_recipes_nested_ingredients_types_recipe
#     #     -- FOREIGN KEY (recipes_nested_id)
#     #     -- REFERENCES recipes_nested (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
#     #     -- FOREIGN KEY (ingredients_types_id)
#     #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
#     # );

# # -- -- ## ***** CATEGORY PRODUCT


# class IngredientType(db.Model):
#     __tablename__ = 'ingredients_types'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     description = db.Column(db.Text, unique=True, nullable=False)
#     unit_cost = db.Column(db.Numeric, nullable=False)
#     unit_of_measure = db.Column(db.Text, nullable=False)

#     def __init__(self, description: str, unit_cost: float, unit_of_measure: str):
#         self.description = description
#         self.unit_cost = unit_cost
#         self.unit_of_measure = unit_of_measure

#     def serialize(self):
#         return {
#             'id': self.id,
#             'description': self.description,
#             'unit_cost': self.unit_cost,
#             'unit_of_measure': self.unit_of_measure
#         }

#     # CREATE TABLE ingredients_types (
#     #     id SERIAL PRIMARY KEY,
#     #     description TEXT NOT NULL UNIQUE,
#     #     unit_cost numeric NOT NULL,
#     #     unit_of_measure TEXT NOT NULL,

#     #     cog_account_id INT NOT NULL,
#     #     preferred_ingredient_item_id INT,
#     #     current_ingredient_item_id INT

#     #     -- ingredients_types
#     #     -- CONSTRAINT fk_ingredients_types_cog_account
#     #     -- FOREIGN KEY (cog_account_id)
#     #     -- REFERENCES cog_accounts (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_ingredients_types_preferred_ingredient
#     #     -- FOREIGN KEY (preferred_ingredient_item_id)
#     #     -- REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_ingredients_types_current_ingredient
#     #     -- FOREIGN KEY (current_ingredient_item_id)
#     #     -- REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
#     # );

# class Ingredients_VendorItem(db.Model):
#     __tablename__ = 'ingredients_vendor_items'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     vendor_item_id = db.Column(db.Numeric, nullable=False)
#     vendor_item_description = db.Column(db.Text, unique=True, nullable=False)
#     purchase_unit = db.Column(db.Text, nullable=False)
#     purchase_unit_cost = db.Column(db.Numeric, nullable=False)
#     split_case_count = db.Column(db.Integer, nullable=False)
#     split_case_cost = db.Column(db.Numeric, nullable=False)
#     split_case_uom = db.Column(db.Text, nullable=False)
#     split_case_uom_cost = db.Column(db.Numeric, nullable=False)
#     notes = db.Column(db.Text, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)
#     date_updated = db.Column(db.DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)

#     ingredients_type_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), nullable=False)
#     vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

#     def __init__(self, vendor_item_id: float, vendor_item_description: str, purchase_unit: str,
#                  purchase_unit_cost: float, split_case_count: int,
#                  split_case_cost: float, split_case_uom: str,
#                  split_case_uom_cost: float, notes: str,
#                  ingredients_type_id: int, vendor_id: int):
#         self.vendor_item_id = vendor_item_id
#         self.vendor_item_description = vendor_item_description
#         self.purchase_unit = purchase_unit
#         self.purchase_unit_cost = purchase_unit_cost
#         self.split_case_count = split_case_count
#         self.split_case_cost = split_case_cost
#         self.split_case_uom = split_case_uom
#         self.split_case_uom_cost = split_case_uom_cost
#         self.notes = notes
#         self.ingredients_type_id = ingredients_type_id
#         self.vendor_id = vendor_id

#     def serialize(self):
#         return {
#             'id': self.id,
#             'vendor_item_id': self.vendor_item_id,
#             'vendor_item_description': self.vendor_item_description,
#             'purchase_unit': self.purchase_unit,
#             'purchase_unit_cost': self.purchase_unit_cost,
#             'split_case_count': self.split_case_count,
#             'split_case_cost': self.split_case_cost,
#             'split_case_uom': self.split_case_uom,
#             'split_case_uom_cost': self.split_case_uom_cost,
#             'notes': self.notes,
#             'date_created': self.date_created.isoformat(),
#             'date_updated': self.date_updated.isoformat(),
#             'ingredients_type_id': self.ingredients_type_id,
#             'vendor_id': self.vendor_id
#         }

#     # CREATE TABLE ingredients_vendor_items (
#     #     id SERIAL PRIMARY KEY,
#     #     vendor_item_id NUMERIC NOT NULL,
#     #     vendor_item_description TEXT NOT NULL UNIQUE,
#     #     purchase_unit TEXT NOT NULL,
#     #     purchase_unit_cost numeric NOT NULL,
#     #     split_case_count INT NOT NULL,
#     #     split_case_cost numeric NOT NULL,
#     #     split_case_uom TEXT NOT NULL,
#     #     split_case_uom_cost numeric NOT NULL,
#     #     notes TEXT NOT NULL,
#     #     date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     #     date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

#     #     ingredients_type_id INT NOT NULL,
#     #     vendor_id INT NOT NULL

#     #     -- ingredients_vendor_items
#     #     -- CONSTRAINT fk_ingredients_vendor_items_ingredients_type
#     #     -- FOREIGN KEY (ingredients_type_id)
#     #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT,

#     #     -- CONSTRAINT fk_ingredients_vendor_items_vendor
#     #     -- FOREIGN KEY (vendor_id)
#     #     -- REFERENCES vendors (id) ON DELETE RESTRICT
#     # );


# class Vendor(db.Model):
#     __tablename__ = 'vendors'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, unique=True, nullable=False)
#     contact_name = db.Column(db.Text, nullable=False)
#     contact_email = db.Column(db.Text, nullable=False)
#     contact_phone = db.Column(db.Text, nullable=False)
#     delivery_days = db.Column(db.Text, nullable=False)
#     order_days = db.Column(db.Text, nullable=False)
#     order_cutoff_time = db.Column(db.Text, nullable=False)
#     terms = db.Column(db.Text, nullable=False)
#     notes = db.Column(db.Text, nullable=False)
#     date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

#     def __init__(self, name: str, contact_name: str,
#                  contact_email: str, contact_phone: str,
#                  delivery_days: str, order_days: str,
#                  order_cutoff_time: str, terms: str,
#                  notes: str):
#         self.name = name
#         self.contact_name = contact_name
#         self.contact_email = contact_email
#         self.contact_phone = contact_phone
#         self.delivery_days = delivery_days
#         self.order_days = order_days
#         self.order_cutoff_time = order_cutoff_time
#         self.terms = terms
#         self.notes = notes

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'contact_name': self.contact_name,
#             'contact_email': self.contact_email,
#             'contact_phone': self.contact_phone,
#             'delivery_days': self.delivery_days,
#             'order_days': self.order_days,
#             'order_cutoff_time': self.order_cutoff_time,
#             'terms': self.terms,
#             'notes': self.notes,
#             'date_updated': self.date_updated.isoformat()
#         }

#     # CREATE TABLE vendors (
#     #     id SERIAL PRIMARY KEY,
#     #     name TEXT NOT NULL UNIQUE,
#     #     contact_name TEXT,
#     #     contact_email TEXT,
#     #     contact_phone TEXT,
#     #     delivery_days TEXT,
#     #     order_days TEXT,
#     #     order_cutoff_time TEXT,
#     #     terms TEXT,
#     #     notes TEXT,
#     #     date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#     # );

# # tests
# if __name__ == '__main__':

#     # Create a Flask app for testing
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database for testing
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     with app.app_context():
#         # Create all tables
#         db.create_all()

#         # Test User model
#         user = User(email='test@example.com', password='password', permissions=1, name='Test User', company_id=None)
#         db.session.add(user)
#         db.session.commit()
#         print('User:', user.serialize())

#         # Test Companies model
#         company = Company(name='Test Company')
#         db.session.add(company)
#         db.session.commit()
#         print('Company:', company.serialize())

#         # Test Stores model
#         store = Store(name='Test Store', company_id=company.id, chart_of_accounts_id=1)
#         db.session.add(store)
#         db.session.commit()
#         print('Store:', store.serialize())

#         # Test users_stores bridge table
#         db.session.execute(
#             text("""INSERT INTO users_stores (user_id, store_id, date_created) VALUES (:user_id, :store_id, :date_created)"""),
#             {'user_id': user.id, 'store_id': store.id, 'date_created': datetime.datetime.now(datetime.UTC)}
#         )
#         db.session.commit()
#         print('users_stores bridge table entry created successfully.')

#         # Test stores_menus bridge table
#         db.session.execute(
#             text("""INSERT INTO stores_menus (store_id, menu_id, date_created) VALUES (:store_id, :menu_id, :date_created)"""),
#             {'store_id': store.id, 'menu_id': 1, 'date_created': datetime.datetime.now(datetime.UTC)}
#         )
#         db.session.commit()
#         print('stores_menus bridge table entry created successfully.')

#         # Test Menu model
#         menu = Menu(name='Test Menu', description='Test Description', sales_account_id=None)
#         db.session.add(menu)
#         db.session.commit()
#         print('Menu:', menu.serialize())

#         # Test RecipePlated model
#         recipe_plated = RecipePlated(description='Test Recipe Plated', notes='Test Notes', recipe_type='Type A', sales_price_basis=10.5)
#         db.session.add(recipe_plated)
#         db.session.commit()
#         print('RecipePlated:', recipe_plated.serialize())

#         # Test RecipeNested model
#         recipe_nested = RecipeNested(description='Test Recipe Nested', notes='Test Notes', recipe_type='Type B', yield_amount=5.0, yield_uom='kg')
#         db.session.add(recipe_nested)
#         db.session.commit()
#         print('RecipeNested:', recipe_nested.serialize())

#         # Test RecipesPlated_RecipesNested bridge table
#         db.session.execute(
#             text("""INSERT INTO recipes_plated_recipes_nested (recipes_plated_id, recipes_nested_id) VALUES (:recipes_plated_id, :recipes_nested_id)"""),
#             {'recipes_plated_id': recipe_plated.id, 'recipes_nested_id': recipe_nested.id}
#         )
#         db.session.commit()
#         print('recipes_plated_recipes_nested bridge table entry created successfully.')

#         # Test RecipesPlated_IngredientsTypes bridge table
#         ingredient_type = IngredientType(description='Test Ingredient', unit_cost=2.5, unit_of_measure='kg')
#         db.session.add(ingredient_type)
#         db.session.commit()
#         db.session.execute(
#             text(
#             """INSERT INTO recipes_plated_ingredients_types (recipes_plated_id, ingredients_types_id, ingredient_quantity, ingredient_uom, ingredient_cost) VALUES (:recipes_plated_id, :ingredients_types_id, :ingredient_quantity, :ingredient_uom, :ingredient_cost)"""
#             ),
#             {'recipes_plated_id': recipe_plated.id, 'ingredients_types_id': ingredient_type.id, 'ingredient_quantity': 1.0, 'ingredient_uom': 'kg', 'ingredient_cost': 2.5}
#         )
#         db.session.commit()
#         print('recipes_plated_ingredients_types bridge table entry created successfully.')

#         # Test RecipesNested_IngredientsTypes bridge table
#         db.session.execute(
#             text(
#             """INSERT INTO recipes_nested_ingredients_types (recipes_nested_id, ingredients_types_id, ingredient_quantity, ingredient_uom, ingredient_cost) VALUES (:recipes_nested_id, :ingredients_types_id, :ingredient_quantity, :ingredient_uom, :ingredient_cost)"""
#             ),
#             {'recipes_nested_id': recipe_nested.id, 'ingredients_types_id': ingredient_type.id, 'ingredient_quantity': 2.0, 'ingredient_uom': 'kg', 'ingredient_cost': 5.0}
#         )
#         db.session.commit()
#         print('recipes_nested_ingredients_types bridge table entry created successfully.')

#         # Test Ingredients_VendorItem model
#         vendor = Vendor(name='Test Vendor', contact_name='John Doe', contact_email='vendor@example.com', contact_phone='1234567890', delivery_days='Mon-Fri', order_days='Mon-Wed', order_cutoff_time='5 PM', terms='Net 30', notes='Test Notes')
#         db.session.add(vendor)
#         db.session.commit()
#         vendor_item = IngredientVendorItem(vendor_item_id=12345, vendor_item_description='Test Vendor Item', purchase_unit='box', purchase_unit_cost=50.0, split_case_count=10, split_case_cost=5.0, split_case_uom='kg', split_case_uom_cost=0.5, notes='Test Notes', ingredients_type_id=ingredient_type.id, vendor_id=vendor.id)
#         db.session.add(vendor_item)
#         db.session.commit()
#         print('Ingredients_VendorItem:', vendor_item.serialize())

#         # Test Vendor model
#         print('Vendor:', vendor.serialize())
