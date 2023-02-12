from app.core.db import db
# from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date, time, timedelta
import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Enum
from app.utils.datetime import format_elapsed_time
from sqlalchemy import types
from typing_extensions import Annotated
from sqlalchemy.dialects.postgresql import INET
import enum

class BaseRole(enum.Enum):
    ADMIN = 0
    MANAGER_USER = 1
    SUPPORT = 2
    LOCAL_ADMIN = 3
    USER = 4
    REPORTS = 5
    COSTUMER = 6

    def __repr__(self) -> str:
        return super().__repr__()

str_10 = Annotated[str, 10]
str_32 = Annotated[str, 32]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]
str_1028 = Annotated[str, 1028]
str_5000 = Annotated[str, 5000]



class BaseModel(db.Model):
    __abstract__ = True
    type_annotation_map = {
        int: types.Integer(),
        datetime:  types.DateTime(timezone=True),
        date : types.Date(),
        time : types.Time(timezone=True),
        timedelta : types.Interval(),
        str: types.String(),
        str_10: types.String(10),
        str_32: types.String(32),
        str_64: types.String(64),
        str_128: types.String(128),
        str_512: types.String(512),
        str_1028: types.String(1028),
        str_5000: types.String(5000),
        uuid.UUID : types.UUID(as_uuid=True),
        float : types.Float(),
        INET : INET,
        BaseRole : Enum(BaseRole)

    }
    id : Mapped[uuid.UUID] = db.mapped_column(primary_key=True, default=uuid.uuid4)
    create_at : Mapped[datetime] = db.mapped_column(nullable=False, default=datetime.utcnow)
    update_at : Mapped[datetime] = db.mapped_column(nullable=True, onupdate=datetime.utcnow)

    @property
    def created_at_elapsed(self):
        return format_elapsed_time(self.create_at)

    @property
    def updated_at_elapsed(self):
        return format_elapsed_time(self.update_at)