from app.core.db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    update_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)