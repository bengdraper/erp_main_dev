'''
User
users_stores
Roles
users_roles
Permissions
roles_permissions

'''


import datetime
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from datetime import timezone
from typing import Optional

from . import db

class User(db.Model):
    __tablename__ = 'users'

    # instantiate attributes matching user table columns
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    preferences = db.Column(JSONB, nullable=True)
    name = db.Column(db.String(128), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    # constraint fkey company id
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)

    # create here object from user instance
    def __init__(self, org_id: uuid.UUID, email: str, password: str, preferences: Optional[dict], name: str, company_id: int):
        self.org_id = org_id
        self.email = email
        self.password = password
        self.preferences = preferences
        self.name = name
        self.date_updated = datetime.now(datetime.timezone.utc)
        self.company_id = company_id

    # serialize this object instance to json for tranmssion
    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'preferences': self.preferences,
            'name': self.name,
            'date_updated': self.date_updated.isoformat(),
            'company_id': self.company_id
        }

users_stores = db.Table(
    'users_stores',
    db.Column(
        # 'user_id', db.Integer,
        'user_id', UUID(as_uuid=True),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        # 'store_id', db.Integer,
        'store_id', UUID(as_uuid=True),
        db.ForeignKey('stores.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'date_created', db.DateTime,
        default=datetime.datetime.utcnow,
        # default=datetime.now(datetime.timezone.utc)
        nullable=False
    )
)

# Roles
class Role(db.Model):
    __tablename__ = 'roles'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(128), nullable=False, )
    description = db.Column(db.Text, unique=True, nullable=False)

    # create here object from user instance
    def __init__(self, org_id: uuid.UUID, name: str, description: str):
        self.org_id = org_id
        self.name = name
        self.description = description

    # serialize this object instance to json for tranmssion
    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
# users_roles

# Permissions

# roles_permissions