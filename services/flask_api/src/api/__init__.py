from .tables import bp as tables_bp
from .users import blueprints as users_blueprints
from .coas import blueprints as accounts_blueprints
from .locations import blueprints as locations_blueprints
from .products import blueprints as products_blueprints
from .menus import blueprints as menus_blueprints

blueprints = [
    tables_bp,
    *users_blueprints,
    *accounts_blueprints,
    *locations_blueprints,
    *products_blueprints,
    *menus_blueprints
    ]



# blueprints = [
#     tables_bp,

#     # users
#     users_bp,
#     users_stores_bp,
#     roles_bp,
#     users_roles_bp,
#     permissions_bp,
#     roles_permissions_bp,

#     # locations
#     companies_bp,
#     stores_bp,
#     organizations_bp,
#     divisions_bp,

#     # menus
#     menus_np,
#     menus_recipes_plated_bp,
#     recipes_plated_bp,
#     recipes_plated_recipes_nested_bp,
#     recipes_plated_ingredients_types_bp,
#     recipes_nested_bp,
#     recipes_nested_ingredients_types_bp,
#     ingredients_types_bp,
#     stores_menus_bp,

#     # products
#     vendors_bp,
#     ingredients_vendor_items_bp,

#     # accounts
#     chart_of_accounts_bp,
#     chart_of_accounts_sales_accounts_categories_bp,
#     chart_of_accounts_cog_accounts_categories_bp,
#     sales_accounts_categories_bp,
#     sales_accounts_categories_sales_accounts_bp,
#     sales_accountes_bp,
#     cog_accounts_categories_bp,
#     cog_accounts_bp
# ]