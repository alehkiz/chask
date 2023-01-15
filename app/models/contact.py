from app.models.base import BaseModel
from app.core.db import db
from re import match as re_match
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.kernel import only_numbers

class Contact(BaseModel):
    __abstract__ = False
    email = db.Column(db.String(256), index=True, unique=True, nullable=True)
    _phone_principal = db.Column(db.String(60), index=True, unique=True, nullable=True)
    _phone_secondary = db.Column(db.String(60), index=True, unique=True, nullable=True)
    costumer = db.relationship('Costumer', backref='contact', lazy='dynamic')

    @staticmethod
    def validate_phone(value):
        pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
        _rematch = re_match(pattern, value)
        if _rematch is None:
            return False
        return True
    
    @hybrid_property
    def phone_principal(self) -> str:
        return self._phone_principal
    
    @phone_principal.setter
    def phone_principal(self, value:str) -> None:
        if self.validate_phone(value=value):
            self._phone_principal = only_numbers(value)
        
    @hybrid_property
    def phone_secondary(self) -> str:
        return self._phone_secondary
    
    @phone_secondary.setter
    def phone_secondary(self, value:str) -> None:
        if self.validate_phone(value=value):
            self._phone_secondary = only_numbers(value)