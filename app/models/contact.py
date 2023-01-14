from app.models.base import BaseModel
from app.core.db import db

class Contact(BaseModel):
    __abstract__ = False
    email = db.Column(db.String(256), index=True, unique=True, nullable=True)
    phone_principal = db.Column(db.String(24), index=True, unique=True, nullable=True)
    phone_secondary = db.Column(db.String(24), index=True, unique=True, nullable=True)
    costumer = db.relationship('Costumer', backref='contact', lazy='dynamic')
