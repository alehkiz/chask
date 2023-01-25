from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional
from re import match as re_match
from app.utils.kernel import only_numbers, validate_cpf

class Costumer(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(1024), index=True, nullable=False)
    _identifier = db.Column(db.String(14), index=True, nullable=False, unique=True)
    identifier_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('costumer_identifier_type.id'), nullable=False)
    # location = db.Column(db.String(127), index=True)
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contact.id'), nullable=False)
    address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('address.id'), nullable=False)

    @hybrid_property
    def identifier(self) -> str:
        return self._identifier
    
    @identifier.setter
    def identifier(self, value: str)-> None:
        if len(only_numbers(value)) == 11:
            if validate_cpf(value):
                self._identifier = only_numbers(value)

    

        
            


class CostumerIdentifierType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(128), index=True, unique=True, nullable=False)#CPF/CNPJ
    clients = db.relationship('Costumer', backref='identifier_type', lazy='dynamic')


