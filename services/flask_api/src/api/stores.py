'''
exposes
/stores
/stores?company_id=X (GET with filter)
'''

from flask import Blueprint, jsonify, abort, request
from ..models import db, Store

bp = Blueprint('stores', __name__, url_prefix='/stores')

@bp.route('', methods=['GET']) # decorate path and list of http verbs
def index():

    data = Store.query.all() # ORM performs select query

    result = []

    for d in data:
        result.append(d.serialize())

    return jsonify(result)