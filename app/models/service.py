from app.models.base import BaseModel, str_64, str_32
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db
from sqlalchemy import event
from sqlalchemy.orm.interfaces import EXT_STOP
from sqlalchemy.orm import mapped_column, Mapped
import uuid


class Service(BaseModel):
    __abstract__ = False
    name : Mapped[str_64] = mapped_column(nullable=False, index=True, unique=True)
    group_id : Mapped[uuid.UUID] = mapped_column(db.ForeignKey('group_service.id'), nullable=False)
    tickets = db.relationship('Ticket', back_populates='service',  lazy='dynamic')
    teams = db.relationship('Team', secondary='group_service_team',
                    primaryjoin='foreign(team.c.id)==group_service_team.c.team_id',
                    secondaryjoin='group_service_team.c.id==foreign(service.c.group_id)',
                    lazy='dynamic',
                    back_populates="services",
                    viewonly=True,
                    )
    groups = db.relationship('GroupService', back_populates="services")


class GroupService(BaseModel):
    __abstract__ = False
    name : Mapped[str_32] = mapped_column(db.String(32), nullable=False, index=True, unique=True)
    services = db.relationship('Service', 
                        # primaryjoin='group_service.c.id == service.c.group_id',
                        # backref=db.backref('group'), 
                        back_populates="groups",
                        lazy='dynamic')
    teams = db.relationship('Team', secondary='group_service_team', back_populates="groups")

class GroupServiceTeam(BaseModel):
    __abstract__ = False
    group_id : Mapped[uuid.UUID] = mapped_column(db.ForeignKey('group_service.id'), nullable=False)
    team_id : Mapped[uuid.UUID] =  mapped_column(db.ForeignKey('team.id'), nullable=False)