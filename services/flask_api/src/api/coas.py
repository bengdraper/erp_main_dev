'''
exposing following routes
/coas
/coas/sales_categories
/coas/sales_accounts
/coas/cog_categories
/coas/cog_accounts
'''

from flask import Blueprint, jsonify, abort, request
from ..models import db, ChartOfAccounts, SalesAccountCategory, SalesAccount, CogAccountCategory, CogAccount

bp = Blueprint('coas', __name__, url_prefix='/coas')

@bp.route('', methods=['GET'])
def index():
    # print('hello index route called')
    log = ['base url coas returns all main coas']

    coas = ChartOfAccounts.query.order_by(ChartOfAccounts.id).all()
    result = []

    for c in coas:
        result.append(c.serialize())

    return jsonify(result)

@bp.route('/sales_categories', methods=['GET'])
def index_sales_categories():

    response = SalesAccountCategory.query.order_by(SalesAccountCategory.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)

@bp.route('/sales_accounts', methods=['GET'])
def index_sales_accounts():

    response = SalesAccount.query.order_by(SalesAccount.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)


@bp.route('/cog_accounts', methods=['GET'])
def index_cog_accounts():

    response = CogAccount.query.order_by(CogAccount.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)

@bp.route('/cog_categories', methods=['GET'])
def index_cog_categories():

    response = CogAccountCategory.query.order_by(CogAccountCategory.id).all()
    result = []

    for r in response:
        result.append(r.serialize())

    return jsonify(result)