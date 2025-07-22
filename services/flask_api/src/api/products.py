'''
answering @
/vendors
/ingredients_vendor_items
'''
from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    Vendor,
    IngredientVendorItem
)
from .config import CORE_PREFIX

tables_models = {
    'vendors': Vendor,
    'ingredients_vendor_items': IngredientVendorItem
}

vendors_bp = Blueprint('vendors', __name__, url_prefix=f'{CORE_PREFIX}/vendors')
vendor_items_bp = Blueprint('ingredients_vendor_items', __name__, url_prefix=f'{CORE_PREFIX}/ingredients_vendor_items')

# flat index table from any tablename in request
def index_any():
    if tables_models.get(request.blueprint):
        res = db.session.query(tables_models.get(request.blueprint)).all()
        return jsonify([r.serialize() for r in res])
    abort(404, description="model not found")

blueprints = [
    vendors_bp,
    vendor_items_bp
]

# index
for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)