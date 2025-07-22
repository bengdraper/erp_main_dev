'''
answering @
/menus
/menus_recipes_plated
/recipes_plated
/recipes_plated_recipes_nested
/recipes_plated_ingredient_types
/recipes_nested
/recipes_nested_ingredient_types
/ingredients_types
/stores_menus
'''
from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    Menu,
    MenuRecipePlated,
    RecipePlated,
    RecipePlatedRecipeNested,
    RecipePlatedIngredientType,
    RecipeNested,
    RecipeNestedIngredientType,
    IngredientType,
    StoreMenu
)
from .config import CORE_PREFIX

tables_models = {
    'menus': Menu,
    'menus_recipes_plated': MenuRecipePlated,
    'recipes_plated': RecipePlated,
    'recipes_plated_recipes_nested': RecipePlatedRecipeNested,
    'recipes_plated_ingredients_types': RecipePlatedIngredientType,
    'recipes_nested': RecipeNested,
    'recipes_nested_ingredients_types': RecipeNestedIngredientType,
    'ingredients_types': IngredientType,
    'stores_menus': StoreMenu,
}

menus_bp = Blueprint('menus', __name__, url_prefix=f'{CORE_PREFIX}/menus')
menus_recipes_plated_bp = Blueprint('menus_recipes_plated', __name__, url_prefix=f'{CORE_PREFIX}/menus_recipes_plated')
recipes_plated_bp = Blueprint('recipes_plated', __name__, url_prefix=f'{CORE_PREFIX}/recipes_plated')
recipes_plated_recipes_nested_bp = Blueprint('recipes_plated_recipes_nested', __name__, url_prefix=f'{CORE_PREFIX}/recipes_plated_recipes_nested')
recipes_plated_ingredients_types_bp = Blueprint('recipes_plated_ingredients_types', __name__, url_prefix=f'{CORE_PREFIX}/recipes_plated_ingredients_types')
recipes_nested_bp = Blueprint('recipes_nested', __name__, url_prefix=f'{CORE_PREFIX}/recipes_nested')
recipes_nested_ingredients_types_bp = Blueprint('recipes_nested_ingredients_types', __name__, url_prefix=f'{CORE_PREFIX}/recipes_nested_ingredients_types')
ingredients_types_bp = Blueprint('ingredients_types', __name__, url_prefix=f'{CORE_PREFIX}/ingredients_types')
stores_menus_bp = Blueprint('stores_menus', __name__, url_prefix=f'{CORE_PREFIX}/stores_menus')

# flat index table from any tablename in request
def index_any():
    if tables_models.get(request.blueprint):
        res = db.session.query(tables_models.get(request.blueprint)).all()
        return jsonify([r.serialize() for r in res])
    abort(404, description="model not found")

blueprints = [
menus_bp,
menus_recipes_plated_bp,
recipes_plated_bp,
recipes_plated_recipes_nested_bp,
recipes_plated_ingredients_types_bp,
recipes_nested_bp,
recipes_nested_ingredients_types_bp,
ingredients_types_bp,
stores_menus_bp
]

# index
for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)