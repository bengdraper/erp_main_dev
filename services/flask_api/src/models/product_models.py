# 2025-07-21 up to date

import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from . import db

__all__ = [
    'Vendor',
    'IngredientVendorItem'
]

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

class IngredientVendorItem(db.Model):
    __tablename__ = 'ingredients_vendor_items'
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_item_id = db.Column(db.Numeric, nullable=False)
    vendor_item_description = db.Column(db.Text, unique=True, nullable=False)
    purchase_unit = db.Column(db.Text, nullable=False)
    purchase_unit_cost = db.Column(db.Numeric, nullable=False)
    split_case_count = db.Column(db.Integer, nullable=False)
    split_case_cost = db.Column(db.Numeric, nullable=False)
    split_case_uom = db.Column(db.Text, nullable=False)
    split_case_uom_cost = db.Column(db.Numeric, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredients_types.id', ondelete='RESTRICT'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id', ondelete='RESTRICT'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, org_id: uuid.UUID, vendor_item_id: float, vendor_item_description: str, purchase_unit: str, purchase_unit_cost: float, split_case_count: int, split_case_cost: float, split_case_uom: str, split_case_uom_cost: float, notes: str, ingredient_type_id: int, vendor_id: int):
        self.org_id = org_id
        self.vendor_item_id = vendor_item_id
        self.vendor_item_description = vendor_item_description
        self.purchase_unit = purchase_unit
        self.purchase_unit_cost = purchase_unit_cost
        self.split_case_count = split_case_count
        self.split_case_cost = split_case_cost
        self.split_case_uom = split_case_uom
        self.split_case_uom_cost = split_case_uom_cost
        self.notes = notes
        self.ingredient_type_id = ingredient_type_id
        self.vendor_id = vendor_id

    def serialize(self):
        return {
            'org_id': str(self.org_id),
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
            'ingredient_type_id': self.ingredient_type_id,
            'vendor_id': self.vendor_id,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None
        }