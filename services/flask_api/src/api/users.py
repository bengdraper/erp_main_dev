# api collection
from flask import Blueprint, jsonify, abort, request
from ..models import db, User
# import hashlib
# import secrets
import sqlalchemy
from sqlalchemy import insert


# def scramble(password: str):
    # """hash and salt"""
    # salt = secrets.token_hex(16)
    # return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')
@bp.route('', methods=['GET']) # decorate path and list of http verbs
def index():
    log = ['hello users']
    return jsonify(log)

    users = User.query.order_by(User.id).all() # order by for case update changes db record position query all return out of expected order
    result = []

    for u in users:
        result.append(u.serialize())

    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):

    u = User.query.get_or_404(id)

    return jsonify(u.serialize())


# # post a tweet from client
# @bp.route('', methods=['POST'])  # for POST requests @ /users/'' (ala blueprint)
# def create():

#     # for incoming post request from client
#     # confirm username and password exist, as json?

#     # check if client request body includes username and password
#     if 'username' not in request.json or 'password' not in request.json:
#         return abort(400)  # flask method abort() w/ status code 

#     # validate username => 3 char and password => 8 char or fail
#     if len(request.json['username']) < 3 or len(request.json['password']) < 8:
#         return abort(400)

#     # create new user in db from client request payload
#     u = User(
#         username=request.json['username'],
#         password=scramble(request.json['password'])
#     )

#     db.session.add(u)  # create this user migration at db; sqlalchemy .add()

#     db.session.commit()  # send it; sqlalchemy .commit()

#     return jsonify(u.serialize())


# delete a user from client
@bp.route('/<int:id>', methods=['DELETE'])  # for delete requests @ /users/'' (ala blueprint)
def delete(id: int):

    u = User.query.get_or_404(id)

    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


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
