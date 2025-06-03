# from flask import Blueprint, jsonify, abort, request
# from ..models import db, ChartOfAccounts, SalesAccountCategory, SalesAccount, CogAccountCategory, CogAccount

# bp = Blueprint('products', __name__, url_prefix='/products')

# @bp.route('', methods=['GET']) # decorate path and list of http verbs
# def index():

#     response = ChartOfAccounts().query.order_by(ChartOfAccounts.id).all()
#     result = []

#     for r in response:
#         result.append(r.serialize())

#     return jsonify(result)