from app.core.db import db
from app.models.base import BaseModel, str_1028, str_128, str_32
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional
from re import match as re_match
from app.utils.kernel import only_numbers, validate_cpf
from app.models.ticket import Ticket
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Costumer(BaseModel):
    __abstract__ = False
    name : Mapped[str_1028]  = mapped_column(index=True, nullable=False)
    _identifier : Mapped[str_32]  = mapped_column(index=True, nullable=False, unique=True)
    identifier_type_id : Mapped[uuid.UUID]  = mapped_column(db.ForeignKey('costumer_identifier_type.id'), nullable=False)
    contact_id : Mapped[uuid.UUID]  = mapped_column(db.ForeignKey('contact.id'), nullable=False)
    address_id : Mapped[uuid.UUID]  = mapped_column(db.ForeignKey('address.id'), nullable=False)

    @hybrid_property
    def identifier(self) -> str:
        return self._identifier
    
    @identifier.setter
    def identifier(self, value: str)-> None:
        if len(only_numbers(value)) == 11:
            if validate_cpf(value):
                self._identifier = only_numbers(value)

    @property
    def opened_tickets(self):
        return self.tickets.filter(Ticket._closed != True).count()
    
    @property
    def closed_tickets(self):
        return self.tickets.filter(Ticket._closed == True).count()
    


class CostumerIdentifierType(BaseModel):
    __abstract__ = False
    type : Mapped[str_128] = mapped_column(db.String(128), index=True, unique=True, nullable=False)#CPF/CNPJ
    clients = db.relationship('Costumer', backref='identifier_type', lazy='dynamic')


