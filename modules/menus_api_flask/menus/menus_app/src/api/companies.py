# # api collection
from flask import Blueprint, jsonify, abort, request
from ..models import db, Company

bp = Blueprint('companies', __name__, url_prefix='/companies')

@bp.route('', methods=['GET']) # decorate path and list of http verbs
def index():
    print('hello companies')
    # log = ['hello companies']
    # return jsonify(log)

    data = Company.query.all() # ORM performs select query

    result = []

    for d in data:
        result.append(d.serialize())

    return jsonify(result)