import datetime
from sqlalchemy.sql import text
from datetime import timezone

from . import db

__all__ = [
    'Menu',
    'Menus_RecipesPlated',
    'RecipePlated',
    'RecipesPlated_RecipesNested',
    'RecipesPlated_IngredientsTypes',
    'RecipeNested',
    'RecipesNested_IngredientsTypes',
    'IngredientType'
]

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    sales_account_id = db.Column(db.Integer, db.ForeignKey('sales_accounts.id'), nullable=True)

    def __init__(self, name: str, description: str, sales_account_id: int):
        self.name = name
        self.description = description
        self.sales_account_id = sales_account_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sales_account_id': self.sales_account_id
        }

    # CREATE TABLE menus (
    #     id SERIAL PRIMARY KEY,
    #     name TEXT NOT NULL UNIQUE,
    #     description TEXT NOT NULL UNIQUE,
    #     sales_account_id INT
    # );


# bridge
class Menus_RecipesPlated(db.Model):
    __tablename__ = 'menus_recipes_plated'

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), primary_key=True)
    recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)

    def __init__(self, menu_id: int, recipes_plated_id: int):
        self.menu_id = menu_id
        self.recipes_plated_id = recipes_plated_id

    def serialize(self):
        return {
            'menu_id': self.menu_id,
            'recipes_plated_id': self.recipes_plated_id
        }

    # CREATE TABLE menus_recipes_plated (
    #     menu_id INT,
    #     recipes_plated_id INT,
    #     PRIMARY KEY (menu_id, recipes_plated_id)

    #     -- menus_recipes_plated
    #     -- CONSTRAINT fk_menus_recipes_plated_menus
    #     -- FOREIGN KEY (menu_id)
    #     -- REFERENCES menus (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_menus_recipes_plated_recipes_plated
    #     -- FOREIGN KEY (recipes_plated_id)
    #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT
    # );

class RecipePlated(db.Model):
    __tablename__ = 'recipes_plated'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    recipe_type = db.Column(db.Text, nullable=True)
    sales_price_basis = db.Column(db.Numeric, nullable=False)

    def __init__(self, description: str, notes: str, recipe_type: str, sales_price_basis: float):
        self.description = description
        self.notes = notes
        self.recipe_type = recipe_type
        self.sales_price_basis = sales_price_basis

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'notes': self.notes,
            'recipe_type': self.recipe_type,
            'sales_price_basis': self.sales_price_basis
        }

    # CREATE TABLE recipes_plated (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL,
    #     notes TEXT NOT NULL,
    #     recipe_type TEXT,
    #     sales_price_basis numeric NOT NULL
    # );


# bridge
class RecipesPlated_RecipesNested(db.Model):
    __tablename__ = 'recipes_plated_recipes_nested'

    recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)
    recipes_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id'), primary_key=True)

    def __init__(self, recipes_plated_id: int, recipes_nested_id: int):
        self.recipes_plated_id = recipes_plated_id
        self.recipes_nested_id = recipes_nested_id

    def serialize(self):
        return {
            'recipes_plated_id': self.recipes_plated_id,
            'recipes_nested_id': self.recipes_nested_id
        }

    # CREATE TABLE recipes_plated_recipes_nested (
    #     recipes_plated_id INT,
    #     recipes_nested_id INT,
    #     PRIMARY KEY (recipes_plated_id, recipes_nested_id)

    #     -- recpes_plated_recipes_nested
    #     -- CONSTRAINT fk_recipes_plated_recipes_nested_plated
    #     -- FOREIGN KEY (recipes_plated_id)
    #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_recipes_nested_recipes_nested_nested
    #     -- FOREIGN KEY (recipes_nested_id)
    #     -- REFERENCES recipes_nested (id) ON DELETE RESTRICT
    # );

# bridge
class RecipesPlated_IngredientsTypes(db.Model):
    __tablename__ = 'recipes_plated_ingredients_types'

    recipes_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id'), primary_key=True)
    ingredients_types_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), primary_key=True)

    ingredient_quantity = db.Column(db.Numeric, nullable=False)
    ingredient_uom = db.Column(db.Text, nullable=False)
    ingredient_cost = db.Column(db.Numeric, nullable=False)

    def __init__(self, recipes_plated_id: int, ingredients_types_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
        self.recipes_plated_id = recipes_plated_id
        self.ingredients_types_id = ingredients_types_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_uom = ingredient_uom
        self.ingredient_cost = ingredient_cost

    def serialize(self):
        return {
            'recipes_plated_id': self.recipes_plated_id,
            'ingredients_types_id': self.ingredients_types_id,
            'ingredient_quantity': self.ingredient_quantity,
            'ingredient_uom': self.ingredient_uom,
            'ingredient_cost': self.ingredient_cost
        }

    # CREATE TABLE recipes_plated_ingredients_types (
    #     recipes_plated_id INT,
    #     ingredients_types_id INT,

    #     ingredient_quantity numeric NOT NULL,
    #     ingredient_uom TEXT NOT NULL,
    #     ingredient_cost numeric NOT NULL,

    #     PRIMARY KEY (recipes_plated_id, ingredients_types_id)

    #     -- recpes_plated_ingredients_types
    #     -- CONSTRAINT fk_recipes_plated_ingredients_types_recipe
    #     -- FOREIGN KEY (recipes_plated_id)
    #     -- REFERENCES recipes_plated (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    #     -- FOREIGN KEY (ingredients_types_id)
    #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
    # );

class RecipeNested(db.Model):
    __tablename__ = 'recipes_nested'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    recipe_type = db.Column(db.Text, nullable=True)
    yield_amount = db.Column(db.Numeric, nullable=False)
    yield_uom = db.Column(db.Text, nullable=False)

    def __init__(self, description: str, notes: str, recipe_type: str, yield_amount: float, yield_uom: str):
        self.description = description
        self.notes = notes
        self.recipe_type = recipe_type
        self.yield_amount = yield_amount
        self.yield_uom = yield_uom

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'notes': self.notes,
            'recipe_type': self.recipe_type,
            'yield_amount': self.yield_amount,
            'yield_uom': self.yield_uom
        }

    # CREATE TABLE recipes_nested (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL,
    #     notes TEXT,
    #     recipe_type TEXT,
    #     yield numeric NOT NULL,
    #     yield_uom TEXT NOT NULL
    # );


# bridge
class RecipesNested_IngredientsTypes(db.Model):
    __tablename__ = 'recipes_nested_ingredients_types'

    recipes_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id'), primary_key=True)
    ingredients_types_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), primary_key=True)

    ingredient_quantity = db.Column(db.Numeric, nullable=False)
    ingredient_uom = db.Column(db.Text, nullable=False)
    ingredient_cost = db.Column(db.Numeric, nullable=False)

    def __init__(self, recipes_nested_id: int, ingredients_types_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
        self.recipes_nested_id = recipes_nested_id
        self.ingredients_types_id = ingredients_types_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_uom = ingredient_uom
        self.ingredient_cost = ingredient_cost

    def serialize(self):
        return {
            'recipes_nested_id': self.recipes_nested_id,
            'ingredients_types_id': self.ingredients_types_id,
            'ingredient_quantity': self.ingredient_quantity,
            'ingredient_uom': self.ingredient_uom,
            'ingredient_cost': self.ingredient_cost
        }

    # CREATE TABLE recipes_nested_ingredients_types (
    #     recipes_nested_id INT,
    #     ingredients_types_id INT,

    #     ingredient_quantity numeric NOT NULL,
    #     ingredient_uom TEXT NOT NULL,
    #     ingredient_cost numeric NOT NULL,

    #     PRIMARY KEY (recipes_nested_id, ingredients_types_id)

    #     -- recipes_nested_ingredients_types
    #     -- CONSTRAINT fk_recipes_nested_ingredients_types_recipe
    #     -- FOREIGN KEY (recipes_nested_id)
    #     -- REFERENCES recipes_nested (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_ingredients_types_ingredients_types_ingredient
    #     -- FOREIGN KEY (ingredients_types_id)
    #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT
    # );

# -- -- ## ***** CATEGORY PRODUCT


class IngredientType(db.Model):
    __tablename__ = 'ingredients_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    unit_cost = db.Column(db.Numeric, nullable=False)
    unit_of_measure = db.Column(db.Text, nullable=False)

    def __init__(self, description: str, unit_cost: float, unit_of_measure: str):
        self.description = description
        self.unit_cost = unit_cost
        self.unit_of_measure = unit_of_measure

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'unit_cost': self.unit_cost,
            'unit_of_measure': self.unit_of_measure
        }

    # CREATE TABLE ingredients_types (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     unit_cost numeric NOT NULL,
    #     unit_of_measure TEXT NOT NULL,

    #     cog_account_id INT NOT NULL,
    #     preferred_ingredient_item_id INT,
    #     current_ingredient_item_id INT

    #     -- ingredients_types
    #     -- CONSTRAINT fk_ingredients_types_cog_account
    #     -- FOREIGN KEY (cog_account_id)
    #     -- REFERENCES cog_accounts (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_ingredients_types_preferred_ingredient
    #     -- FOREIGN KEY (preferred_ingredient_item_id)
    #     -- REFERENCES ingredients_vendor_items (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_ingredients_types_current_ingredient
    #     -- FOREIGN KEY (current_ingredient_item_id)
    #     -- REFERENCES ingredients_vendor_items (id) ON DELETE SET NULL
    # );