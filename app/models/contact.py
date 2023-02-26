from typing import List, Optional
from app.models.base import BaseModel, str_256, str_64
from app.core.db import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.kernel import only_numbers, validate_phone
from sqlalchemy.orm import Mapped, mapped_column

class Contact(BaseModel):
    __abstract__ = False
    email : Mapped[str_256] = db.mapped_column(db.String(256), index=True, unique=True)
    _phone_principal : Mapped[Optional[str_64]] = db.mapped_column(db.String(60), index=True, unique=True)
    _phone_secondary : Mapped[Optional[str_64]] = db.mapped_column(db.String(60), index=True, unique=True)
    costumer : Mapped[List['Costumer']]= db.relationship(backref='contact', lazy='dynamic')

    @staticmethod
    def validate_phone(value : str) -> bool:
        return validate_phone(value=value)
    
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