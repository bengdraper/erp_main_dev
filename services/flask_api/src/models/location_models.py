# 2025-07-21 up to date

from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from typing import Optional

from . import db

__all__ = [
    'Company',
    'Store',
    'Organization',
    'Division'
]

class Company(db.Model):
    __tablename__ = 'companies'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, unique=True, nullable=False)
    company_metadata = db.Column('metadata', JSONB, nullable=True, default=dict)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, name: str, company_metadata: Optional[dict] = None):
        self.org_id = org_id
        self.name = name
        self.company_metadata = company_metadata or {}

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'name': self.name,
            'company_metadata': self.company_metadata,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class Store(db.Model):
    __tablename__ = 'stores'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, unique=True, nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id', ondelete='RESTRICT'), nullable=False)
    chart_of_accounts_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'), nullable=False, default=1)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, name: str, company_id: uuid.UUID, chart_of_accounts_id: int):
        self.org_id = org_id
        self.name = name
        self.company_id = company_id
        self.chart_of_accounts_id = chart_of_accounts_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'name': self.name,
            'company_id': str(self.company_id),
            'chart_of_accounts_id': self.chart_of_accounts_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    org_metadata = db.Column('metadata', JSONB, nullable=True, default=dict)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, name: str, description: Optional[str] = None, org_metadata: Optional[dict] = None):
        self.name = name
        self.description = description
        self.org_metadata = org_metadata or {}

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'org_metadata': self.org_metadata,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

class Division(db.Model):
    __tablename__ = 'divisions'

    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, name: str, description: Optional[str] = None):
        self.org_id = org_id
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }