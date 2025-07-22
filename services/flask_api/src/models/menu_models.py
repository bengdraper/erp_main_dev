# 2025-07-21 up to date

from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

__all__ = [
    'Menu',
    'MenuRecipePlated',
    'RecipePlated',
    'RecipePlatedRecipeNested',
    'RecipePlatedIngredientType',
    'RecipeNested',
    'RecipeNestedIngredientType',
    'IngredientType',
    'StoreMenu'
]

class Menu(db.Model):
    __tablename__ = 'menus'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    sales_account_id = db.Column(db.Integer, db.ForeignKey('sales_accounts.id', ondelete='RESTRICT'), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, name: str, description: str, sales_account_id: int = None):
        self.org_id = org_id
        self.name = name
        self.description = description
        self.sales_account_id = sales_account_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sales_account_id': self.sales_account_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class MenuRecipePlated(db.Model):
    __tablename__ = 'menus_recipes_plated'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', ondelete='RESTRICT'), primary_key=True)
    recipe_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id', ondelete='RESTRICT'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, menu_id: int, recipe_plated_id: int):
        self.org_id = org_id
        self.menu_id = menu_id
        self.recipe_plated_id = recipe_plated_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'menu_id': self.menu_id,
            'recipe_plated_id': self.recipe_plated_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RecipePlated(db.Model):
    __tablename__ = 'recipes_plated'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    recipe_type = db.Column(db.Text, nullable=True)
    sales_price_basis = db.Column(db.Numeric, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, notes: str, recipe_type: str, sales_price_basis: float):
        self.org_id = org_id
        self.description = description
        self.notes = notes
        self.recipe_type = recipe_type
        self.sales_price_basis = sales_price_basis

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'notes': self.notes,
            'recipe_type': self.recipe_type,
            'sales_price_basis': self.sales_price_basis,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RecipePlatedRecipeNested(db.Model):
    __tablename__ = 'recipes_plated_recipes_nested'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    recipe_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id', ondelete='RESTRICT'), primary_key=True)
    recipe_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id', ondelete='RESTRICT'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, recipe_plated_id: int, recipe_nested_id: int):
        self.org_id = org_id
        self.recipe_plated_id = recipe_plated_id
        self.recipe_nested_id = recipe_nested_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'recipe_plated_id': self.recipe_plated_id,
            'recipe_nested_id': self.recipe_nested_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RecipePlatedIngredientType(db.Model):
    __tablename__ = 'recipes_plated_ingredients_types'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    recipe_plated_id = db.Column(db.Integer, db.ForeignKey('recipes_plated.id', ondelete='RESTRICT'), primary_key=True)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id', ondelete='RESTRICT'), primary_key=True)
    ingredient_quantity = db.Column(db.Numeric, nullable=False)
    ingredient_uom = db.Column(db.Text, nullable=False)
    ingredient_cost = db.Column(db.Numeric, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, recipe_plated_id: int, ingredient_type_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
        self.org_id = org_id
        self.recipe_plated_id = recipe_plated_id
        self.ingredient_type_id = ingredient_type_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_uom = ingredient_uom
        self.ingredient_cost = ingredient_cost

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'recipe_plated_id': self.recipe_plated_id,
            'ingredient_type_id': self.ingredient_type_id,
            'ingredient_quantity': self.ingredient_quantity,
            'ingredient_uom': self.ingredient_uom,
            'ingredient_cost': self.ingredient_cost,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RecipeNested(db.Model):
    __tablename__ = 'recipes_nested'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recipe_type = db.Column(db.Text, nullable=True)
    yield_ = db.Column('yield', db.Numeric, nullable=False)
    yield_uom = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, notes: str, recipe_type: str, yield_: float, yield_uom: str):
        self.org_id = org_id
        self.description = description
        self.notes = notes
        self.recipe_type = recipe_type
        self.yield_ = yield_
        self.yield_uom = yield_uom

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'notes': self.notes,
            'recipe_type': self.recipe_type,
            'yield': self.yield_,
            'yield_uom': self.yield_uom,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RecipeNestedIngredientType(db.Model):
    __tablename__ = 'recipes_nested_ingredients_types'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    recipe_nested_id = db.Column(db.Integer, db.ForeignKey('recipes_nested.id', ondelete='RESTRICT'), primary_key=True)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id', ondelete='RESTRICT'), primary_key=True)
    ingredient_quantity = db.Column(db.Numeric, nullable=False)
    ingredient_uom = db.Column(db.Text, nullable=False)
    ingredient_cost = db.Column(db.Numeric, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, recipe_nested_id: int, ingredient_type_id: int, ingredient_quantity: float, ingredient_uom: str, ingredient_cost: float):
        self.org_id = org_id
        self.recipe_nested_id = recipe_nested_id
        self.ingredient_type_id = ingredient_type_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_uom = ingredient_uom
        self.ingredient_cost = ingredient_cost

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'recipe_nested_id': self.recipe_nested_id,
            'ingredient_type_id': self.ingredient_type_id,
            'ingredient_quantity': self.ingredient_quantity,
            'ingredient_uom': self.ingredient_uom,
            'ingredient_cost': self.ingredient_cost,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class IngredientType(db.Model):
    __tablename__ = 'ingredients_types'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    unit_cost = db.Column(db.Numeric, nullable=False)
    unit_of_measure = db.Column(db.Text, nullable=False)
    cog_account_id = db.Column(db.Integer, db.ForeignKey('cog_accounts.id', ondelete='RESTRICT'), nullable=False)
    preferred_ingredient_item_id = db.Column(db.Integer, db.ForeignKey('ingredients_vendor_items.id', ondelete='RESTRICT'), nullable=True)
    current_ingredient_item_id = db.Column(db.Integer, db.ForeignKey('ingredients_vendor_items.id', ondelete='SET NULL'), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, unit_cost: float, unit_of_measure: str, cog_account_id: int, preferred_ingredient_item_id: int = None, current_ingredient_item_id: int = None):
        self.org_id = org_id
        self.description = description
        self.unit_cost = unit_cost
        self.unit_of_measure = unit_of_measure
        self.cog_account_id = cog_account_id
        self.preferred_ingredient_item_id = preferred_ingredient_item_id
        self.current_ingredient_item_id = current_ingredient_item_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'unit_cost': self.unit_cost,
            'unit_of_measure': self.unit_of_measure,
            'cog_account_id': self.cog_account_id,
            'preferred_ingredient_item_id': self.preferred_ingredient_item_id,
            'current_ingredient_item_id': self.current_ingredient_item_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class StoreMenu(db.Model):
    __tablename__ = 'stores_menus'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='RESTRICT'), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, store_id: int, menu_id: int):
        self.org_id = org_id
        self.store_id = store_id
        self.menu_id = menu_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'store_id': self.store_id,
            'menu_id': self.menu_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }
