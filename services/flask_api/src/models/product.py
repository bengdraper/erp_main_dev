import datetime
from sqlalchemy.sql import text
from datetime import timezone

from . import db

class Ingredients_VendorItem(db.Model):
    __tablename__ = 'ingredients_vendor_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_item_id = db.Column(db.Numeric, nullable=False)
    vendor_item_description = db.Column(db.Text, unique=True, nullable=False)
    purchase_unit = db.Column(db.Text, nullable=False)
    purchase_unit_cost = db.Column(db.Numeric, nullable=False)
    split_case_count = db.Column(db.Integer, nullable=False)
    split_case_cost = db.Column(db.Numeric, nullable=False)
    split_case_uom = db.Column(db.Text, nullable=False)
    split_case_uom_cost = db.Column(db.Numeric, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)

    ingredients_type_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

    def __init__(self, vendor_item_id: float, vendor_item_description: str, purchase_unit: str,
                 purchase_unit_cost: float, split_case_count: int,
                 split_case_cost: float, split_case_uom: str,
                 split_case_uom_cost: float, notes: str,
                 ingredients_type_id: int, vendor_id: int):
        self.vendor_item_id = vendor_item_id
        self.vendor_item_description = vendor_item_description
        self.purchase_unit = purchase_unit
        self.purchase_unit_cost = purchase_unit_cost
        self.split_case_count = split_case_count
        self.split_case_cost = split_case_cost
        self.split_case_uom = split_case_uom
        self.split_case_uom_cost = split_case_uom_cost
        self.notes = notes
        self.ingredients_type_id = ingredients_type_id
        self.vendor_id = vendor_id

    def serialize(self):
        return {
            'id': self.id,
            'vendor_item_id': self.vendor_item_id,
            'vendor_item_description': self.vendor_item_description,
            'purchase_unit': self.purchase_unit,
            'purchase_unit_cost': self.purchase_unit_cost,
            'split_case_count': self.split_case_count,
            'split_case_cost': self.split_case_cost,
            'split_case_uom': self.split_case_uom,
            'split_case_uom_cost': self.split_case_uom_cost,
            'notes': self.notes,
            'date_created': self.date_created.isoformat(),
            'date_updated': self.date_updated.isoformat(),
            'ingredients_type_id': self.ingredients_type_id,
            'vendor_id': self.vendor_id
        }

    # CREATE TABLE ingredients_vendor_items (
    #     id SERIAL PRIMARY KEY,
    #     vendor_item_id NUMERIC NOT NULL,
    #     vendor_item_description TEXT NOT NULL UNIQUE,
    #     purchase_unit TEXT NOT NULL,
    #     purchase_unit_cost numeric NOT NULL,
    #     split_case_count INT NOT NULL,
    #     split_case_cost numeric NOT NULL,
    #     split_case_uom TEXT NOT NULL,
    #     split_case_uom_cost numeric NOT NULL,
    #     notes TEXT NOT NULL,
    #     date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #     date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    #     ingredients_type_id INT NOT NULL,
    #     vendor_id INT NOT NULL

    #     -- ingredients_vendor_items
    #     -- CONSTRAINT fk_ingredients_vendor_items_ingredients_type
    #     -- FOREIGN KEY (ingredients_type_id)
    #     -- REFERENCES ingredients_types (id) ON DELETE RESTRICT,

    #     -- CONSTRAINT fk_ingredients_vendor_items_vendor
    #     -- FOREIGN KEY (vendor_id)
    #     -- REFERENCES vendors (id) ON DELETE RESTRICT
    # );


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    contact_name = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.Text, nullable=False)
    contact_phone = db.Column(db.Text, nullable=False)
    delivery_days = db.Column(db.Text, nullable=False)
    order_days = db.Column(db.Text, nullable=False)
    order_cutoff_time = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, name: str, contact_name: str,
                 contact_email: str, contact_phone: str,
                 delivery_days: str, order_days: str,
                 order_cutoff_time: str, terms: str,
                 notes: str):
        self.name = name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.delivery_days = delivery_days
        self.order_days = order_days
        self.order_cutoff_time = order_cutoff_time
        self.terms = terms
        self.notes = notes

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'delivery_days': self.delivery_days,
            'order_days': self.order_days,
            'order_cutoff_time': self.order_cutoff_time,
            'terms': self.terms,
            'notes': self.notes,
            'date_updated': self.date_updated.isoformat()
        }

    # CREATE TABLE vendors (
    #     id SERIAL PRIMARY KEY,
    #     name TEXT NOT NULL UNIQUE,
    #     contact_name TEXT,
    #     contact_email TEXT,
    #     contact_phone TEXT,
    #     delivery_days TEXT,
    #     order_days TEXT,
    #     order_cutoff_time TEXT,
    #     terms TEXT,
    #     notes TEXT,
    #     date_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    # );