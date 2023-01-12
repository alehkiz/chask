from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class Ticket(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(512), index=True, nullable=False)
    info = db.Column(db.String(1024), index=True, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket_type.id'), nullable=False)
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('network.id'), nullable=False)
    costumer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('costumer.id'), nullable=True)#Cidadão pode ficar vazio
    comments = db.relationship('Comment', backref='ticket', lazy='dynamic')
    costumer = db.relationship('Costumer', backref='tickets', uselist=False)

class TicketType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(512), index=True, nullable=False, unique=True)
    tickets = db.relationship('Ticket', backref='type', lazy='dynamic', single_parent=True)
