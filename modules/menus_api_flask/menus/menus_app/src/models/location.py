import datetime
from sqlalchemy.sql import text
from datetime import timezone

from . import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    # CREATE TABLE companies (
    #     id SERIAL PRIMARY KEY,
    #     name TEXT NOT NULL UNIQUE
    # );

class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='RESTRICT'), nullable=False)
    chart_of_accounts_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id', ondelete='SET DEFAULT'), nullable=False)

    def __init__(self, name: str, company_id: int, chart_of_accounts_id: int):
        self.name = name
        self.company_id = company_id
        self.chart_of_accounts_id = chart_of_accounts_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'chart_of_accounts_id': self.chart_of_accounts_id
        }

    # CREATE TABLE stores (
    #     id SERIAL PRIMARY KEY,
    #     name TEXT NOT NULL UNIQUE,
    #     company_id INT NOT NULL,
    #     chart_of_accounts_id INT NOT NULL DEFAULT 1

    #     -- stores
    #     -- CONSTRAINT fk_stores_companies
    #     -- FOREIGN KEY (company_id)
    #     #     REFERENCES companies (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_stores_chart_of_accounts
    #     -- FOREIGN KEY (chart_of_accounts_id)
    #     -- REFERENCES chart_of_accounts (id) ON DELETE SET DEFAULT
    # );


stores_menus = db.Table(
    'stores_menus',
    db.Column(
        'store_id', db.Integer,
        db.ForeignKey('stores.id', ondelete='RESTRICT'),
        primary_key=True
    ),
    db.Column(
        'menu_id', db.Integer,
        db.ForeignKey('menus.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'date_created', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    # CREATE TABLE stores_menus (
    #     store_id INT,
    #     menu_id INT,
    #     PRIMARY KEY (store_id, menu_id)

    #     -- stores_menus
    #     -- CONSTRAINT fk_stores_menus_store
    #     -- FOREIGN KEY (store_id)
    #     -- REFERENCES stores (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_stores_menus_menu
    #     -- FOREIGN KEY (menu_id)
    #     -- REFERENCES menus (id) ON DELETE CASCADE
    # );
)