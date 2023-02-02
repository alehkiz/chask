
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db
from sqlalchemy import event
from sqlalchemy.orm.interfaces import EXT_STOP



class Service(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('group_service.id'), nullable=False)
    tickets = db.relationship('Ticket', backref='service',  lazy='dynamic')


class GroupService(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(32), nullable=False, index=True, unique=True)
    services = db.relationship('Service',  backref='group', lazy='dynamic')
    

class GroupServiceTeam(BaseModel):
    __abstract__ = False
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('group_service.id'), nullable=False)
    team_id =  db.Column(UUID(as_uuid=True), db.ForeignKey('team.id'), nullable=False)