from datetime import datetime
from typing import Optional
from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.security import User
from app.utils.datetime import format_elapsed_time
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import event
from flask import current_app as app


class Ticket(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(512), index=True, nullable=False)
    title = db.Column(db.String(512), index=True, nullable=False)
    info = db.Column(db.String(5000), index=True, nullable=False)
    _closed = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime(timezone=True), nullable=False)
    _closed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket_type.id'), nullable=False)
    create_network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('network.id'), nullable=False)
    create_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    costumer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('costumer.id'), nullable=True)#Cidadão pode ficar vazio
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('service.id'), nullable=False)
    comments = db.relationship('Comment', backref=db.backref('ticket',  order_by='desc(Comment.create_at)'), lazy='dynamic', order_by='desc(Comment.create_at)')
    costumer = db.relationship('Costumer', backref='tickets', uselist=False)
    stage_event = db.relationship('TicketStageEvent',
                            primaryjoin='ticket_stage_event.c.ticket_id==ticket.c.id',
                            backref=db.backref('ticket'),
                            lazy='dynamic')
    users = db.relationship('User', secondary='ticket_stage_event', 
                primaryjoin=('ticket_stage_event.c.ticket_id==foreign(ticket.c.id)'),#foreign for overlap foreign key
                secondaryjoin=('ticket_stage_event.c.user_id==foreign(user.c.id)'),
                backref=db.backref('tickets', lazy='dynamic'), 
                lazy='dynamic'
                )

    stages =  association_proxy('stage_event', 'stage')

    @property
    def current_user(self):
        if self.current_stage_event != None:
            return self.current_stage_event.user
        return None

    @property
    def current_stage(self):
        if self.current_stage != None:
            return self.current_stage_event.stage
        return None
    
    @property
    def current_stage_event(self):
        return db.session.query(TicketStageEvent)\
            .filter(TicketStageEvent.ticket_id == self.id)\
                .order_by(TicketStageEvent.create_at.desc()).limit(1).first()

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


class TicketStage(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(28), index=True, nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False, unique=True)

class TicketStageEvent(BaseModel):
    __abstract__ = False
    ticket_stage_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket_stage.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    deadline = db.Column(db.DateTime(timezone=True), nullable=False)
    _closed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    _closed = db.Column(db.Boolean)
    info = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref('user_stage', lazy='dynamic'))
    stage = db.relationship('TicketStage', backref=db.backref('events', lazy='dynamic'))
    user_name = association_proxy('user', 'name')
    stage_name = association_proxy('stage', 'name')
    stage_level = association_proxy('stage', 'level')
    
    def __init__(self, ticket_stage_id, user_id, ticket_id, deadline, info=None) -> None:
        self.ticket_stage_id = ticket_stage_id
        self.user_id = user_id
        self.ticket_id = ticket_id
        if deadline < datetime.utcnow():
            raise Exception('Deadline menor que a data/hora atual.')
        self.deadline = deadline
        
        self.info = info
    @staticmethod
    def add(ticket_stage: TicketStage, user: User, ticket: Ticket, deadilne: datetime, info: Optional[str]=None, close_last: bool=False, force: bool=False):
        query = db.session.query(TicketStageEvent).filter(
            TicketStageEvent.ticket_stage_id==ticket_stage.id,
            TicketStageEvent.user_id == user.id,
            TicketStageEvent.ticket_id == ticket.id,
        ).order_by(TicketStageEvent.create_at.desc())#mais recente primeiro
        if query.count() > 0 and force is False:
            raise Exception('Não é possível adicionar o evento, já há um cadastro')
        else:
            tse = TicketStageEvent(
                user_id=user.id,
                ticket_id=ticket.id,
                ticket_stage_id=ticket_stage.id,
                deadline=deadilne, 
                info=info)
        if close_last is True:
            last_event = db.session.query(TicketStageEvent).filter(
                    TicketStageEvent.ticket_id == ticket.id,
                ).order_by(TicketStageEvent.create_at.desc()).first()
            if not last_event is None:
                last_event.closed = True
        try:
            db.session.add(tse)
            db.session.commit()
            return tse
        except Exception as e:
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            raise Exception('Não foi possível salvar o IP')

    @hybrid_property
    def closed(self):
        return self.closed
    
    @closed.setter
    def closed(self, value):
        match value:
            case True:
                self._closed = True
                self._closed_at = datetime.utcnow()
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

        


# @event.listens_for(TicketStage.collection, 'append', propagate=True)
# def my_append_listener(target, value, initiator):
#     print("received append event for target: %s" % target)
