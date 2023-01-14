from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional



class Address(BaseModel):
    __abstract__ = False
    code = db.Column(db.String(8), index=True, nullable=False)#CEP
    address_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('address_type.id'), nullable=False)#rua, avenida, estrada
    _number = db.Column(db.Integer, nullable=True)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey('city.id'), nullable=False)

    costumers = db.relationship('Costumer', backref='address', lazy='dynamic')

    @hybrid_property
    def number(self) -> Optional[int]:
        if self._number == 0:
            return None
        return self._number
    
    @number.setter
    def number(self, value:int) -> None:
        self._number = value

class AddressType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(32), index=True, nullable=False, unique=True)

class City(BaseModel):
    __abstract__ = False
    city = db.Column(db.String(256), index=True, nullable=False, unique=False)
    uf_id = db.Column(UUID(as_uuid=True), db.ForeignKey('state_location.id'), nullable=False)#rua, avenida, estrada
    adresses = db.relationship('Address', backref='city', lazy='dynamic')

class StateLocation(BaseModel):
    __abstract__ = False
    state = db.Column(db.String(60), index=True, nullable=False, unique=True)
    uf = db.Column(db.String(2), index=True, nullable=False, unique=True)
    cities = db.relationship('City', backref='state', lazy='dynamic')