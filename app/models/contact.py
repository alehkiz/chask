from app.models.base import BaseModel, str_256, str_64
from app.core.db import db
from re import match as re_match
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.kernel import only_numbers
from sqlalchemy.orm import Mapped, mapped_column

class Contact(BaseModel):
    __abstract__ = False
    email : Mapped[str_256] = db.mapped_column(db.String(256), index=True, unique=True, nullable=True)
    _phone_principal : Mapped[str_64] = db.mapped_column(db.String(60), index=True, unique=True, nullable=True)
    _phone_secondary : Mapped[str_64] = db.mapped_column(db.String(60), index=True, unique=True, nullable=True)
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