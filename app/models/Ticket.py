from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class Ticket(BaseModel):
    name = db.Column(db.String(512), index=True, nullable=False)
    info = db.Column(db.String(1024), index=True, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket_type'), nullable=False)

class TicketType(BaseModel):
    type = db.Column(db.String(512), index=True, nullable=False, unique=True)

