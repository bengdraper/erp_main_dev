# 2025-07-21 up to date

from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from typing import Optional

from . import db

__all__ = [
    'User',
    'UserStore',
    'Role',
    'UserRole',
    'Permission',
    'RolePermission',
    'UserAudit'
]

class User(db.Model):
    __tablename__ = 'users'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_metadata = db.Column('metadata', JSONB, nullable=True)
    last_name = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, email: str, password: str, user_metadata: Optional[dict], last_name: str, first_name: str, company_id: int):
        self.org_id = org_id
        self.email = email
        self.password = password
        self.user_metadata = user_metadata
        self.last_name = last_name
        self.first_name = first_name
        self.company_id = company_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'email': self.email,
            'password': self.password,
            'user_metadata': self.user_metadata,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'company_id': self.company_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class UserStore(db.Model):
    __tablename__ = 'users_stores'
    org_id = db.Column( 'org_id', UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), primary_key=True)
    user_id = db.Column( 'user_id', UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    store_id = db.Column( 'store_id', UUID(as_uuid=True), db.ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column('date_created', db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column('date_updated', db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, user_id: uuid.UUID, store_id: uuid.UUID):
        self.org_id = org_id
        self.user_id = user_id
        self.store_id = store_id

    def serialize(self):
        return {
        'org_id': str(self.org_id),
        'user_id': str(self.user_id),
        'store_id': str(self.store_id),
        'date_created': self.date_created.isoformat() if self.date_created else None,
        'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# Roles
class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = (
        db.UniqueConstraint('org_id', 'name', name='uq_org_name')
    ),

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(128), nullable=False, )
    description = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    # create here object from user instance
    def __init__(self, org_id: uuid.UUID, name: str, description: str):
        self.org_id = org_id
        self.name = name
        self.description = description

    # serialize this object instance to json for tranmssion
    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class UserRole(db.Model):
    __tablename__ = 'users_roles'

    org_id = db.Column( 'org_id', UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'))
    user_id = db.Column( 'user_id', UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column( 'role_id', UUID(as_uuid=True), db.ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)
    division_id = db.Column( 'division_id', UUID(as_uuid=True), db.ForeignKey('divisions.id', ondelete='CASCADE'), primary_key=True)
    company_id = db.Column( 'company_id', UUID(as_uuid=True), db.ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True)
    store_id = db.Column( 'store_id', UUID(as_uuid=True), db.ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column('date_created', db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column('date_updated', db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, user_id: uuid.UUID, role_id: uuid.UUID, division_id: uuid.UUID, company_id: uuid.UUID, store_id: uuid.UUID):
        self.org_id = org_id
        self.user_id = user_id
        self.role_id = role_id
        self.division_id = division_id
        self.company_id = company_id
        self.store_id = store_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'user_id': str(self.user_id),
            'role_id': str(self.role_id),
            'division_id': str(self.division_id),
            'company_id': str(self.company_id),
            'store_id': str(self.store_id),
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class Permission(db.Model):
    __tablename__ = 'permissions'
    __table_args__ = (
        db.UniqueConstraint('org_id', 'codename', name='uq_org_codename')
    ),

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codename = db.Column(db.String(128), nullable=False, )
    description = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, codename: str, description: str):
        self.org_id = org_id
        self.codename = codename
        self.description = description

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'codename': self.codename,
            'description': self.description,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'

    org_id = db.Column( 'org_id', UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=False)
    role_id = db.Column( 'role_id', UUID(as_uuid=True), db.ForeignKey('roles.id', ondelete='RESTRICT'), primary_key=True)
    permission_id = db.Column( 'permission_id', UUID(as_uuid=True), db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__ (self, org_id: uuid.UUID, role_id: uuid.UUID, permission_id: uuid.UUID):
        self.org_id = org_id
        self.role_id = role_id
        self.permission_id = permission_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'role_id': str(self.role_id),
            'permission_id': str(self.permission_id),
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class UserAudit(db.Model):
    __tablename__ = 'users_audit'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    audit_action = db.Column(db.String(16), nullable=False)
    audit_timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    audit_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    old_data = db.Column(db.JSON, nullable=True)
    new_data = db.Column(db.JSON, nullable=True)

    def __init__(self, org_id: uuid.UUID, id: int, user_id: uuid.UUID, audit_action: str, audit_timestamp, audit_user=None, old_data=None, new_data=None):
        self.org_id = org_id
        self.id = id
        self.user_id = user_id
        self.audit_action = audit_action
        self.audit_timestamp = audit_timestamp
        self.audit_user = audit_user
        self.old_data = old_data
        self.new_data = new_data

    def serialize(self):
        return {
            'org_id': str(self.org_id) if self.org_id else None,
            'id': self.id,
            'user_id': str(self.user_id) if self.user_id else None,
            'audit_action': self.audit_action,
            'audit_timestamp': self.audit_timestamp.isoformat() if self.audit_timestamp else None,
            'audit_user': str(self.audit_user) if self.audit_user else None,
            'old_data': self.old_data,
            'new_data': self.new_data
        }
