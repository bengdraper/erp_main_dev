# 2025-07-21 up to date

import datetime
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

__all__ = [
    'ChartOfAccounts',
    'ChartOfAccountsSalesAccountCategory',
    'ChartOfAccountsCogAccountCategory',
    'SalesAccountCategory',
    'SalesAccountCategorySalesAccount',
    'SalesAccount',
    'CogAccountCategory',
    'CogAccount'
]

# ChartOfAccounts
class ChartOfAccounts(db.Model):
    __tablename__ = 'chart_of_accounts'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str):
        self.org_id = org_id
        self.description = description

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# ChartOfAccountsSalesAccountCategory
class ChartOfAccountsSalesAccountCategory(db.Model):
    __tablename__ = 'chart_of_accounts_sales_account_categories'
    __table_args__ = (
        db.PrimaryKeyConstraint('chart_of_accounts_id', 'sales_account_category_id'),
    )
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    chart_of_accounts_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'), primary_key=True)
    sales_account_category_id = db.Column(db.Integer, db.ForeignKey('sales_account_categories.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, chart_of_accounts_id: int, sales_account_category_id: int):
        self.org_id = org_id
        self.chart_of_accounts_id = chart_of_accounts_id
        self.sales_account_category_id = sales_account_category_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'chart_of_accounts_id': self.chart_of_accounts_id,
            'sales_account_category_id': self.sales_account_category_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# ChartOfAccountsCogAccountCategory
class ChartOfAccountsCogAccountCategory(db.Model):
    __tablename__ = 'chart_of_accounts_cog_account_categories'
    __table_args__ = (
        db.PrimaryKeyConstraint('chart_of_accounts_id', 'cog_account_category_id'),
    )
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    chart_of_accounts_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'), primary_key=True)
    cog_account_category_id = db.Column(db.Integer, db.ForeignKey('cog_account_categories.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, chart_of_accounts_id: int, cog_account_category_id: int):
        self.org_id = org_id
        self.chart_of_accounts_id = chart_of_accounts_id
        self.cog_account_category_id = cog_account_category_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'chart_of_accounts_id': self.chart_of_accounts_id,
            'cog_account_category_id': self.cog_account_category_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# SalesAccountCategory
class SalesAccountCategory(db.Model):
    __tablename__ = 'sales_account_categories'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, account_number: str):
        self.org_id = org_id
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# SalesAccountCategorySalesAccount
class SalesAccountCategorySalesAccount(db.Model):
    __tablename__ = 'sales_account_categories_sales_accounts'
    __table_args__ = (
        db.PrimaryKeyConstraint('sales_account_category_id', 'sales_account_id'),
    )
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id'), nullable=False)
    sales_account_category_id = db.Column(db.Integer, db.ForeignKey('sales_account_categories.id', ondelete='RESTRICT'), primary_key=True)
    sales_account_id = db.Column(db.Integer, db.ForeignKey('sales_accounts.id', ondelete='CASCADE'), primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, sales_account_category_id: int, sales_account_id: int):
        self.org_id = org_id
        self.sales_account_category_id = sales_account_category_id
        self.sales_account_id = sales_account_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'sales_account_category_id': self.sales_account_category_id,
            'sales_account_id': self.sales_account_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# SalesAccount
class SalesAccount(db.Model):
    __tablename__ = 'sales_accounts'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Numeric, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, account_number: float):
        self.org_id = org_id
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# CogAccountCategory
class CogAccountCategory(db.Model):
    __tablename__ = 'cog_account_categories'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Numeric, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, account_number: float):
        self.org_id = org_id
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }

# CogAccount
class CogAccount(db.Model):
    __tablename__ = 'cog_accounts'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Text, unique=True, nullable=False)
    cog_account_category_id = db.Column(db.Integer, db.ForeignKey('cog_account_categories.id', ondelete='RESTRICT'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, description: str, account_number: str, cog_account_category_id: int):
        self.org_id = org_id
        self.description = description
        self.account_number = account_number
        self.cog_account_category_id = cog_account_category_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number,
            'cog_account_category_id': self.cog_account_category_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }
