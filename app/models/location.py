from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional

from app.utils.kernel import only_numbers



class Address(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(256), index=True, nullable=False, unique=False)#CEP
    postcode_id = db.Column(UUID(as_uuid=True), db.ForeignKey('address_postcode.id'), nullable=False)
    address_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('address_type.id'), nullable=False)#rua, avenida, estrada
    _number = db.Column(db.Integer, nullable=True, default=0)
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

class AddressPostcode(BaseModel):
    __abstract__ = False
    _code = db.Column(db.String(8), index=True, nullable=False, unique=True)#CEP
    adresses = db.relationship('Address', backref='code', lazy='dynamic')

    @hybrid_property
    def code(self):
        self._code

    @code.setter
    def code(self, value: str) -> None:
        match len(value):
            case 9:
                self._code = only_numbers(value)
            case 8:
                self._code = only_numbers(value)
            case _:
                raise Exception('Houve um erro em atribuir `postcode`')



class AddressType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(32), index=True, nullable=False, unique=True)
    adresses = db.relationship('Address', backref='type', lazy='dynamic')

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