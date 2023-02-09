from app.core.db import db
# from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, date, time, timedelta
from uuid import uuid4, UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from app.utils.datetime import format_elapsed_time
from sqlalchemy import types
from typing_extensions import Annotated

from sqlalchemy.dialects.postgresql import INET

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
        str_10: types.String(),
        str_64: types.String(),
        UUID : types.UUID(as_uuid=True),
        float : types.Float(),
        INET : INET

    }
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    create_at : Mapped[datetime] = mapped_column(default=datetime.utcnow)
    update_at : Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)

    @property
    def created_at_elapsed(self):
        return format_elapsed_time(self.create_at)

    @property
    def updated_at_elapsed(self):
        return format_elapsed_time(self.update_at)