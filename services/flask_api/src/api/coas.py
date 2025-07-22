'''
answering @
/chart_of_accounts
/chart_of_accounts_sales_account_categories
/chart_of_accounts_cog_account_categories
/sales_account_categories
/sales_account_category_sales_accounts
/sales_accounts
/cog_account_categories
/cog_accounts
'''

from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    ChartOfAccounts,
    ChartOfAccountsSalesAccountCategory,
    ChartOfAccountsCogAccountCategory,
    SalesAccountCategory,
    SalesAccountCategorySalesAccount,
    SalesAccount,
    CogAccountCategory,
    CogAccount
)
from .config import CORE_PREFIX

tables_models = {
    'chart_of_accounts': ChartOfAccounts,
    'chart_of_accounts_sales_account_categories': ChartOfAccountsSalesAccountCategory,
    'chart_of_accounts_cog_account_categories': ChartOfAccountsCogAccountCategory,
    'sales_account_categories': SalesAccountCategory,
    'sales_account_categories_sales_accounts': SalesAccountCategorySalesAccount,
    'sales_accounts': SalesAccount,
    'cog_account_categories': CogAccountCategory,
    'cog_accounts': CogAccount
}

accounts_bp = Blueprint('chart_of_accounts', __name__, url_prefix=f'{CORE_PREFIX}/chart_of_accounts')
accounts_sales_categories_bp = Blueprint('chart_of_accounts_sales_account_categories', __name__, url_prefix=f'{CORE_PREFIX}/chart_of_accounts_sales_account_categories')
accounts_cog_categories_bp = Blueprint('chart_of_accounts_cog_account_categories', __name__, url_prefix=f'{CORE_PREFIX}/chart_of_accounts_cog_account_categories')
sales_categories_bp = Blueprint('sales_account_categories', __name__, url_prefix=f'{CORE_PREFIX}/sales_account_categories')
sales_categories_sales_accounts_bp = Blueprint('sales_account_categories_sales_accounts', __name__, url_prefix=f'{CORE_PREFIX}/sales_account_categories_sales_accounts')
sales_accounts_bp = Blueprint('sales_accounts', __name__, url_prefix=f'{CORE_PREFIX}/sales_accounts')
cog_categories_bp = Blueprint('cog_account_categories', __name__, url_prefix=f'{CORE_PREFIX}/cog_account_categories')
cog_accounts_bp = Blueprint('cog_accounts', __name__, url_prefix=f'{CORE_PREFIX}/cog_accounts')

# flat index table from any tablename in request
def index_any():
    if tables_models.get(request.blueprint):
        res = db.session.query(tables_models.get(request.blueprint)).all()
        return jsonify([r.serialize() for r in res])
    abort(404, description="model not found")

blueprints = [
    accounts_bp,
    accounts_sales_categories_bp,
    accounts_cog_categories_bp,
    sales_categories_bp,
    sales_categories_sales_accounts_bp,
    sales_accounts_bp,
    cog_categories_bp,
    cog_accounts_bp
]

for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)
