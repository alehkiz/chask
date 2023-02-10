from typing import Optional
import uuid
from sqlalchemy import asc, desc
from app.models.base import BaseModel, str_512
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db
from datetime import datetime
from flask import current_app as app
from app.models.chat import Message
from sqlalchemy.orm import mapped_column, Mapped

from app.models.security import User
from app.utils.datetime import format_elapsed_time

team_administrators = db.Table('team_administrators',
                            db.Column('team_id', UUID(as_uuid=True), db.ForeignKey('team.id')),
                            db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
                            db.Column("administrator_at", db.DateTime(timezone=True), default=datetime.utcnow)
                            )

class Team(BaseModel):
    __abstract__ = False
    name : Mapped[str_512] = mapped_column(db.String(512), index=True, nullable=False)
    active : Mapped[bool] = mapped_column(db.Boolean, default=False)
    administrators = db.relationship(
        "User",
        secondary=team_administrators,
        backref=db.backref(
            "teams_administrated", lazy="dynamic", order_by="desc(team_administrators.c.administrator_at)"
        ),
        lazy="dynamic",
        order_by="desc(team_administrators.c.administrator_at)",
    )

    users = db.relationship(
        'User',
        secondary='user_team',
        primaryjoin=("user_team.c.team_id==foreign(team.c.id)"),
        secondaryjoin=('user_team.c.user_id==foreign(user.c.id)'),
        backref=db.backref(
            "teams", lazy='dynamic', #order_by="desc(team_administrators.c.administrator_at)"
        ),
        lazy='dynamic',
        #order_by="desc(team_administrators.c.administrator_at)",
        viewonly=True
    )
    tickets = db.relationship('Ticket', 
                secondary='ticket_stage_event', 
                back_populates='teams',
                lazy='dynamic',
                viewonly=True
                )
    tickets_stage_event = db.relationship('TicketStageEvent', back_populates='team', viewonly=True)

    services = db.relationship('Service', secondary='group_service_team',
                    primaryjoin='team.c.id==foreign(group_service_team.c.team_id)',
                    secondaryjoin='foreign(group_service_team.c.id)==service.c.group_id',
                    lazy='dynamic',
                    back_populates="teams",
                    viewonly=True,
                    )
    groups = db.relationship('GroupService', secondary='group_service_team',
                    lazy='dynamic',
                    back_populates="teams",
                    viewonly=True,
                    )
    messages = db.relationship('Message', backref='team', lazy='dynamic', order_by='asc(Message.create_at)')

    def remove_user(self, user:User) -> None:
        if isinstance(user, User):
            self.users.remove(user)
            try:
                db.session.commit()
            except Exception as e:
                app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
                app.logger.error(e)
                raise Exception('Não foi possível remover usuário do time')

    def add_user(self, user:User) -> None:
        if isinstance(user, User):
            self.users.add(user)
            try:
                db.session.commit()
            except Exception as e:
                app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
                app.logger.error(e)
                raise Exception('Não foi possível adicionar usuário ao time')


    def unreaded_messages(self, user):
        from app.models.chat import Message
        from app.models.security import User
        # received_messages = db.session.query(db.func.count(Message.id).label('cnt')).join(User.received_messages)\
        #         .filter(User.id == user.id, Message.team_id == self.id).subquery()
        team_messages = db.session.query(db.func.count(Message.id).label('cnt')).filter(Message.team_id == self.id).subquery()
        read_msg = db.session.query(db.func.count(Message.id).label('cnt'))\
                        .join(User.readed_messages)\
                                .filter(User.id == user.id, Message.team_id == self.id)\
                                        .subquery()
        count_unread = db.session.query(team_messages.c.cnt - read_msg.c.cnt).scalar()
        return count_unread

    @property
    def last_message(self):
        return db.session.query(Message).filter(Message.team == self).order_by(desc(Message.create_at)).first()

    @property
    def time_last_message(self):
        message =  db.session.query(Message).filter(Message.team == self).order_by(desc(Message.create_at)).first()
        if message is None:
            return self.create_at
        return message.create_at

    @property
    def time_elapsed_last_message(self):
        return format_elapsed_time(self.time_last_message)

    def add_view_message(self, user:User, messages:Optional[list[Message]]=None):
        if not isinstance(messages, list):
            messages = self.messages
        
        for message in messages:
            if message.user_can_read(user) and user not in message.users_readed:
                message.users_readed.append(user)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            raise Exception('Não foi possível adicionar a leitura às mesagens')
        
    def has_user(self, user : User):
        return user in self.users

class UserTeam(BaseModel):
    __abstract__ = False
    user_id = mapped_column(db.ForeignKey("user.id"), nullable=False)
    team_id : Mapped[uuid.UUID] = mapped_column(db.ForeignKey("team.id"), nullable=False)

    
        

    
