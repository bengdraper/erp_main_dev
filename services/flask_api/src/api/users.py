'''
answers @:
/users
/users/id (GET)
/users/id (PUT)
/users/id/stores (GET)

/users_stores
/roles
/users_roles
/permissions
/roles_permissions
/users_audit
'''

from flask import Blueprint, jsonify, abort, request
from ..models import (
    db,
    User,
    UserStore,
    Role,
    UserRole,
    Permission,
    RolePermission,
    UserAudit
)
from .config import CORE_PREFIX

# import hashlib
# import secrets
# import sqlalchemy
# from sqlalchemy import insert

# def scramble(password: str):
#     """hash and salt"""
#     salt = secrets.token_hex(16)
#     return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

tables_models = {
    'users': User,
    'users_stores': UserStore,
    'roles': Role,
    'users_roles': UserRole,
    'permissions': Permission,
    'roles_permissions': RolePermission,
    'users_audit': UserAudit
}

# bluprints here used
users_bp = Blueprint('users', __name__, url_prefix=f'{CORE_PREFIX}/users')
users_stores_bp = Blueprint('users_stores', __name__, url_prefix=f'{CORE_PREFIX}/users_stores')
roles_bp = Blueprint('roles', __name__, url_prefix=f'{CORE_PREFIX}/roles')
users_roles_bp = Blueprint('users_roles', __name__, url_prefix=f'{CORE_PREFIX}/users_roles')
permissions_bp = Blueprint('permissions', __name__, url_prefix=f'{CORE_PREFIX}/permissions')
roles_permissions_bp = Blueprint('roles_permissions', __name__, url_prefix=f'{CORE_PREFIX}/roles_permissions')
user_audit_bp = Blueprint('users_audit', __name__, url_prefix=f'{CORE_PREFIX}/users_audit')

# flat index table from any tablename in request
def index_any():
    if tables_models.get(request.blueprint):
        res = db.session.query(tables_models.get(request.blueprint)).all()
        return jsonify([r.serialize() for r in res])
    abort(404, description="model not found")

@users_bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())

# delete a user from client
@users_bp.route('/<int:id>', methods=['DELETE'])  # for delete requests @ /users/'' (ala blueprint)
def delete(id: int):

    u = User.query.get_or_404(id)

    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

# create a user
@users_bp.route('/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    """Update user profile fields"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # find user
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if 'name' in data:
            user.name = data['name']
            
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        
        return jsonify(user.serialize())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


blueprints = [
    users_bp,
    users_stores_bp,
    roles_bp,
    users_roles_bp,
    permissions_bp,
    roles_permissions_bp,
    user_audit_bp
    ]

# dynamic index
for bp in blueprints:
    bp.route('', methods=['GET'])(index_any)


# keeping this because I like it...
# @users_stores_bp.route('', methods=['GET'])
# def index():
#     res = db.session.query(UserStore).all()
#     return jsonify([r.serialize() for r in res])


# may still want to ref this later...
# @bp.route('/<int:id>', methods=['PATCH','PUT'])
# def update(id: int):

#     u = User.query.get_or_404(id)
#     # log.append(f'initial user object state: {u.serialize()}')

#     if 'username' not in request.json and 'password' not in request.json:
#     #     log.append('no key in request')
#         return abort(400)

#     if 'username' in request.json:
#         if len(request.json['username']) < 3:
#             # log.append('username short, exit')
#             return abort(400)

#         else:
#             # log.extend(['username length pass', f'set u.usernam {u.username} to {request.json['username']}'])
#             u.username = request.json['username']
#             # log.append(f'u.username = {u.username}')

#     if 'password' in request.json:
#         if len(request.json['password']) < 8:
#             # log.append('pword short, exit')
#             return abort(400)

#         else:
#             u.password = scramble(request.json['password'])

#     try:
#         # log.append('commit user updates')
#         db.session.commit()
#         # log.append(f'@ try: db.session.commit() user state: {u.serialize()}')
#         return jsonify(u.serialize())
#     except:
#         # log.append('failover @ commit, user should not be changed')
#         return jsonify(False)

#     # debug/
#     # log.append(f'end user object state: {u.serialize()}')
#     # log.append(f'end db record state: {u.query.get(id).serialize()}')
#     # return jsonify(log)


# @bp.route('/<int:id>/liked_tweets', methods=['GET'])
# def liked_tweets(id: int):

#     u = User.query.get_or_404(id)

#     result = []

#     for t in u.liked_tweets:
#         result.append(t.serialize())

#     return jsonify(result)


# @bp.route('/<int:id>/likes', methods=['POST'])
# def like(id: int):
#     log = []

#     # check that any tweet_id exists in payload or 400
#     if 'tweet_id' not in request.json:
#         # log.append('abort @ confirm tweet_id key exists')
#         return abort(400)

#     # check that user @ url exists in users
#     u = User.query.get_or_404(id)
#     # log.append(f'found user: {u.query.get(id).serialize()}')

#     # check that tweet @ payload exists in tweets
#     t = Tweet.query.get_or_404(request.json['tweet_id'])
#     # log.append(f'tweet found at id {request.json['tweet_id']}: {t.serialize()}')

#     # no double liking
#     # like = likes_table.select().where((likes_table.c.user_id == u.id) & (likes_table.c.tweet_id == t.id))
#     like = (
#         sqlalchemy.select(likes_table)
#         .where(likes_table.c.user_id == u.id)
#         .where(likes_table.c.tweet_id == t.id)
#         )
#     like = db.session.execute(like).fetchone()
#     if like:
#         return abort(400, description="already liked")
#         # log.append(f'like = {like}')
#     # log.append(f'like = {like}')

#     # prepare insert statement
#     stmt = insert(likes_table).values(user_id = u.id, tweet_id = t.id)
#     # compiled = stmt.compile()
#     # log.append(f'stmt: {compiled}')

#     try:
#         db.session.execute(stmt)
#         db.session.commit()
#         return jsonify(True)
#     except:
#         return jsonify(False)
#         # return jsonify(log)


# @bp.route('/<int:user_id>/likes/<int:tweet_id>', methods=['DELETE'])
# def unlike(user_id: int, tweet_id: int):

#     u = User.query.get_or_404(user_id)
#     # log = {'1': f'found user id: {u.id}'}
#     t = Tweet.query.get_or_404(tweet_id)
#     # log['2'] = f'found tweet id: {t.id}'

#     # no double un-liking
#     like = (
#         sqlalchemy.select(likes_table)
#         .where(likes_table.c.user_id == u.id)
#         .where(likes_table.c.tweet_id == t.id)
#         )
#     like = db.session.execute(like).fetchone()
#     if not like:
#         abort(400, description='sorry can\'t unlike what isn\'t liked')
#     # log['3'] = f'found matching reference {like}'

#     delete_stmt = (
#         sqlalchemy.delete(likes_table)
#         .where(likes_table.c.user_id == u.id)
#         .where(likes_table.c.tweet_id == t.id)
#         )

#     try:

#         db.session.execute(delete_stmt)
#         db.session.commit()
#         # log['Remove Like'] = True
#         # return jsonify(log)
#         return jsonify(True)

#     except:
#         return jsonify(False)
