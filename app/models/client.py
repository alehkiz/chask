from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Client(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(1024), index=True, nullable=False)
    identifier = db.Column(db.String(127), index=True, nullable=False, unique=True)
    identifier_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client_identifier_type.id'), nullable=False)
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contact.id'), nullable=False)

    
class ClientIdentifierType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(128), index=True, unique=True, nullable=False)
    clients = db.relationship('Client', backref='identifier_type', lazy='dynamic')
