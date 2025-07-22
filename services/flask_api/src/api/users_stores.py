# '''
# exposing routes 
# /users_stores
# /users/stores?user_id=X (GET with filter)
# '''

# from flask import Blueprint, jsonify, abort, request
# from ..models import db, UserStore

# bp = Blueprint('users_stores', __name__, url_prefix='/users_stores')

# @bp.route('', methods=['GET'])
# def index():
#     user_id = request.args.get('user_id')

#     query = db.session.query(UserStore)
#     if user_id:
#         query = query.filter(UserStore.user_id == user_id)
#     response = query.all()

#     result = []
#     for r in response:
#         result.append({
#             "user_id": r.user_id,
#             "store_id": r.store_id
#         })
#     return jsonify(result)