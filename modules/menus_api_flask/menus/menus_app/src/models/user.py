import datetime
from sqlalchemy.sql import text
from datetime import timezone

from . import db

class User(db.Model):
    __tablename__ = 'users'

    # instantiate attributes matching user table columns
    # col id 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    permissions = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    # constraint fkey company id
    # company_id = db.Column(db.Integer(128), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)

    # relates to
    # -- users
    # -- CONSTRAINT fk_users_company
    # -- FOREIGN KEY (company_id)
    # -- REFERENCES companies (id) ON DELETE SET NULL

    # create here object from user instance
    def __init__(self, email: str, password: str, permissions: int, name: str, company_id: int):
        self.email = email
        self.password = password
        self.permissions = 0
        self.name = name
        # self.date_updated = datetime.now(datetime.timezone.utc)
        self.date_updated = datetime.datetime.utcnow()
        self.company_id = company_id

    # serialize this object instance to json for tranmssion
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'permissions': self.permissions,
            'name': self.name,
            'date_updated': self.date_updated.isoformat(),
            'company_id': self.company_id
        }

# bridge
# class UserStore(db.Model):
#     __tablename__ = 'users_stores'

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)

#     def __init__(self, user_id: int, store_id: int):
#         self.user_id = user_id
#         self.store_id = store_id

#     def serialize(self):
#         return {
#             'user_id': self.user_id,
#             'store_id': self.store_id
#         }

users_stores = db.Table(
    'users_stores',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'store_id', db.Integer,
        db.ForeignKey('stores.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'date_created', db.DateTime,
        default=datetime.datetime.utcnow,
        # default=datetime.now(datetime.timezone.utc)
        nullable=False
    )

    # CREATE TABLE users_stores (
    #     user_id INT,
    #     store_id INT,
    #     PRIMARY KEY (user_id, store_id)

    #     -- users_stores
    #     -- CONSTRAINT fk_users_stores_user
    #     -- FOREIGN KEY (user_id)
    #     -- REFERENCES users (id) ON DELETE CASCADE,

    #     -- CONSTRAINT fk_users_stores_store
    #     -- FOREIGN KEY (store_id)
    #     -- REFERENCES stores (id) ON DELETE CASCADE
    # );
)