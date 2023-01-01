from app.models.base import BaseModel
from app.core.db import db

class Contact(BaseModel):
    email = db.Column(db.String(128), index=True, unique=True, nullable=True)
    phone_principal = db.Column(db.String(24), index=True, unique=True, nullable=True)
    phone_secondary = db.Column(db.String(24), index=True, unique=True, nullable=True)
