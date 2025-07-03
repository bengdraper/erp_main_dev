'''
exposing routes 
/users_stores
/users/stores?user_id=X (GET with filter)
'''

from flask import Blueprint, jsonify, abort, request
from ..models import db, users_stores

bp = Blueprint('users_stores', __name__, url_prefix='/users_stores')

@bp.route('', methods=['GET'])
def index():
    user_id = request.args.get('users_id')

    if user_id:
        response = db.session.query(users_stores).filter(users_stores.c.user_id == user_id).all()
    else:
        response = db.session.query(users_stores).all()

    result = []
    for r in response:
        result.append({
            "user_id": r.user_id,
            "store_id": r.store_id
        })
    return jsonify(result)