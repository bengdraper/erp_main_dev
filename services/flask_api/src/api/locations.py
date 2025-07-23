'''
answering @
/organizations
/divisions
/companies
/stores
/orgs_members
/companies_members
/stores_members
'''

from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    Organization,
    Division,
    Company,
    Store,
    OrgsMembers,
    CompaniesMembers,
    StoresMembers
)
from .config import CORE_PREFIX

tables_models = {
    'organizations': Organization,
    'divisions': Division,
    'companies': Company,
    'stores': Store,
    'orgs_members': OrgsMembers,
    'companies_members': CompaniesMembers,
    'stores_members': StoresMembers
}

organizations_bp = Blueprint('organizations', __name__, url_prefix=f'{CORE_PREFIX}/organizations')
divisions_bp = Blueprint('divisions', __name__, url_prefix=f'{CORE_PREFIX}/divisions')
companies_bp = Blueprint('companies', __name__, url_prefix=f'{CORE_PREFIX}/companies')
stores_bp = Blueprint('stores', __name__, url_prefix=f'{CORE_PREFIX}/stores')
orgs_members_bp = Blueprint('orgs_members', __name__, url_prefix=f'{CORE_PREFIX}/orgs_members')
companies_members_bp = Blueprint('companies_members', __name__, url_prefix=f'{CORE_PREFIX}/companies_members')
stores_members_bp = Blueprint('stores_members', __name__, url_prefix=f'{CORE_PREFIX}/stores_members')

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
    stores_bp,
    orgs_members_bp,
    companies_members_bp,
    stores_members_bp
]

# index
for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)