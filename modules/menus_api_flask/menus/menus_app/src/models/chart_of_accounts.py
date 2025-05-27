import datetime
from sqlalchemy.sql import text
from datetime import timezone

from . import db

__all__ = [
    'ChartOfAccounts',
    'chart_of_accounts_sales_account_categories',
    'chart_of_accounts_cog_account_categories',
    'SalesAccountCategory',
    'sales_account_categories_sales_accounts',
    'SalesAccount',
    'CogAccountCategory',
    'CogAccount'
]

class ChartOfAccounts(db.Model):
    __tablename__ = 'chart_of_accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, description: str):
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'date_created': self.date_created.isoformat()
        }

    # CREATE TABLE chart_of_accounts (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    # );



chart_of_accounts_sales_account_categories = db.Table(
    'chart_of_accounts_sales_account_categories',
    db.Column(
        'chart_of_accounts_id', db.Integer,
        db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'),
        primary_key=True
    ),
    db.Column(
        'sales_account_categories_id', db.Integer,
        db.ForeignKey('sales_account_categories.id', ondelete='CASCADE'),
        primary_key=True
    )

    # CREATE TABLE chart_of_accounts_sales_account_categories (
    #     chart_of_accounts_id INT,
    #     sales_account_categories_id INT,
    #     PRIMARY KEY (chart_of_accounts_id, sales_account_categories_id)

    #     -- chart_of_accounts_sales_account_categories
    #     -- CONSTRAINT fk_chart_of_accounts_sales_categories_chart
    #     -- FOREIGN KEY (chart_of_accounts_id)
    #     -- REFERENCS chart_of_accounts (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_chart_of_accounts_sales_account_categories_sales_account
    #     -- FOREIGN KEY (sales_account_categories_id)
    #     -- REFERENCS sales_account_categories (id) ON DELETE CASCADE
    # );

)

chart_of_accounts_cog_account_categories = db.Table(
    'chart_of_accounts_cog_account_categories',
    db.Column(
        'chart_of_accounts_id', db.Integer,
        db.ForeignKey('chart_of_accounts.id', ondelete='RESTRICT'),
        primary_key=True
    ),
    db.Column(
        'cog_account_categories_id', db.Integer,
        db.ForeignKey('cog_account_categories.id', ondelete='CASCADE'),
        primary_key=True
    )

    # CREATE TABLE chart_of_accounts_cog_account_categories (
    #     chart_of_accounts_id INT,
    #     cog_account_categories_id INT,
    #     PRIMARY KEY (chart_of_accounts_id, cog_account_categories_id)

    #     -- chart_of_accounts_cog_account_categories
    #     -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_chart
    #     -- FOREIGN KEY (chart_of_accounts_id)
    #     -- REFERENCES chart_of_accounts (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_chart_of_accounts_cog_account_categories_account_category
    #     -- FOREIGN KEY (cog_account_categories_id)
    #     -- REFERENCES cog_account_categories (id) ON DELETE CASCADE
    # );

)


class SalesAccountCategory(db.Model):
    __tablename__ = 'sales_account_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, description: str, account_number: str):
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number
        }

    # CREATE TABLE sales_account_categories (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     account_number TEXT NOT NULL UNIQUE
    # );



sales_account_categories_sales_accounts = db.Table(
    'sales_account_categories_sales_accounts',
    db.Column(
        'sales_account_categories_id', db.Integer,
        db.ForeignKey('sales_account_categories.id', ondelete='RESTRICT'),
        primary_key=True
    ),
    db.Column(
        'sales_accounts_id', db.Integer,
        db.ForeignKey('sales_accounts.id', ondelete='CASCADE'),
        primary_key=True
    )

    # CREATE TABLE sales_account_categories_sales_accounts (
    #     sales_account_categories_id INT,
    #     sales_accounts_id INT,
    #     PRIMARY KEY (sales_account_categories_id, sales_accounts_id)

    #     -- sales_account_categories_sales_accounts
    #     -- CONSTRAINT fk_sales_account_categories_sales_accounts_category
    #     -- FOREIGN KEY (sales_account_categories_id)
    #     -- REFERENCES sales_account_categories (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_sales_accounts_categories_sales_accounts_account
    #     -- FOREIGN KEY (sales_accounts_id)
    #     -- REFERENCES sales_accounts (id) ON DELETE CASCADE
    # );

)

class SalesAccount(db.Model):
    __tablename__ = 'sales_accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Numeric, unique=True, nullable=False)

    def __init__(self, description: str, account_number: str):
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number
        }

    # CREATE TABLE sales_accounts (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     account_number NUMERIC NOT NULL UNIQUE
    # );

class CogAccountCategory(db.Model):
    __tablename__ = 'cog_account_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Numeric, unique=True, nullable=False)

    def __init__(self, description: str, account_number: str):
        self.description = description
        self.account_number = account_number

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number
        }

    # CREATE TABLE cog_account_categories (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     account_number NUMERIC NOT NULL UNIQUE
    # );

class CogAccount(db.Model):
    __tablename__ = 'cog_accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    account_number = db.Column(db.Text, unique=True, nullable=False)
    cog_account_category_id = db.Column(db.Integer, db.ForeignKey('cog_account_categories.id'), nullable=False)

    def __init__(self, description: str, account_number: str, cog_account_category_id: int):
        self.description = description
        self.account_number = account_number
        self.cog_account_category_id = cog_account_category_id

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'account_number': self.account_number,
            'cog_account_category_id': self.cog_account_category_id
        }

    # CREATE TABLE cog_accounts (
    #     id SERIAL PRIMARY KEY,
    #     description TEXT NOT NULL UNIQUE,
    #     account_number TEXT NOT NULL UNIQUE,
    #     cog_account_category_id INT NOT NULL

    #     -- cog_accounts
    #     -- CONSTRAINT fk_cog_accounts_cog_account_category
    #     -- FOREIGN KEY (cog_account_category_id)
    #     -- REFERENCES cog_account_categories (id) ON DELETE RESTRICT
    # );