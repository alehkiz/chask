from datetime import datetime
from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.datetime import format_elapsed_time


class Ticket(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(512), index=True, nullable=False)
    title = db.Column(db.String(512), index=True, nullable=False)
    info = db.Column(db.String(5000), index=True, nullable=False)
    _closed = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime, nullable=False)
    _closed_at = db.Column(db.DateTime, nullable=True)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket_type.id'), nullable=False)
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('network.id'), nullable=False)
    costumer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('costumer.id'), nullable=True)#Cidadão pode ficar vazio
    comments = db.relationship('Comment', backref='ticket', lazy='dynamic')
    costumer = db.relationship('Costumer', backref='tickets', uselist=False)

    @hybrid_property
    def closed(self):
        return self.closed
    
    @closed.setter
    def closed(self, value):
        match value:
            case True:
                self._closed = True
                self.closed_at = datetime.utcnow()
            case False:
                self._closed = False
        
    @property
    def is_closed(self):
        if self._closed is True:
            return True
        else:
            return False

    @hybrid_property
    def closed_at(self):
        return self.closed_at
    
    @closed.setter
    def closed_at(self, value):
        raise Exception('Não é possível incluir ou alterar a data do fechamento por closed_at, altere o atributo closed')

    @property
    def closed_at_elapsed(self):
        return format_elapsed_time(self.closed_at)

    @property
    def deadline_elapsed(self):
        return format_elapsed_time(self.deadline)

        

class TicketType(BaseModel):
    __abstract__ = False
    type = db.Column(db.String(512), index=True, nullable=False, unique=True)
    tickets = db.relationship('Ticket', backref='type', lazy='dynamic', single_parent=True)
