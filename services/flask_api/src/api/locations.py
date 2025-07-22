'''
answering @
/organizations
/divisions
/companies
/stores
'''
from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    Organization,
    Division,
    Company,
    Store
)
from .config import CORE_PREFIX

tables_models = {
    'organizations': Organization,
    'divisions': Division,
    'companies': Company,
    'stores': Store
}

organizations_bp = Blueprint('organizations', __name__, url_prefix=f'{CORE_PREFIX}/organizations')
divisions_bp = Blueprint('divisions', __name__, url_prefix=f'{CORE_PREFIX}/divisions')
companies_bp = Blueprint('companies', __name__, url_prefix=f'{CORE_PREFIX}/companies')
stores_bp = Blueprint('stores', __name__, url_prefix=f'{CORE_PREFIX}/stores')

# flat index table from any tablename in request
def index_any():
    if tables_models.get(request.blueprint):
        res = db.session.query(tables_models.get(request.blueprint)).all()
        return jsonify([r.serialize() for r in res])
    abort(404, description="model not found")

blueprints = [
    organizations_bp,
    divisions_bp,
    companies_bp,
    stores_bp
]

# index
for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)