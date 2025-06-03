'''
exposing routes
/vendors
/vendors/items
'''

from flask import Blueprint, jsonify, abort, request
from ..models import db, Vendor, IngredientsVendorItem

bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@bp.route('', methods=['GET']) # decorate path and list of http verbs
def index():

    response = Vendor.query.order_by(Vendor.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)

@bp.route('/items', methods=['GET']) # decorate path and list of http verbs
def index_vendor_items():

    response = IngredientsVendorItem.query.order_by(IngredientsVendorItem.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)