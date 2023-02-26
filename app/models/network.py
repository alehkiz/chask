
from typing import List
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class Network(BaseModel):
    __abstract__ = False
    ip : Mapped[INET] = db.mapped_column(INET, nullable=False)
    # created_user_id = db.mapped_column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    created_user : Mapped[List['User']] = db.relationship(backref='created_network', lazy='dynamic', foreign_keys='[User.created_network_id]')
    confirmed_user : Mapped[List['User']] = db.relationship(backref='confirmed_network', lazy='dynamic', foreign_keys='[User.confirmed_network_id]')
    comemnts_created : Mapped[List['Comment']] = db.relationship(backref='created_network', lazy='dynamic', foreign_keys='[Comment.create_network_id]')
    comments_updated : Mapped[List['Comment']] = db.relationship(backref='update_network', lazy='dynamic', foreign_keys='[Comment.update_network_id]')
    messages_created : Mapped[List['Message']] = db.relationship(backref='creted_network', lazy='dynamic', foreign_keys='[Message.create_network_id]')
    visits : Mapped[List['Visit']] = db.relationship(backref='network', lazy='dynamic', single_parent=True)
    tickets : Mapped[List['Ticket']] = db.relationship(backref='network', lazy='dynamic', single_parent=True)
    sessions : Mapped[List['LoginSession']] = db.relationship(backref='network', lazy='dynamic', single_parent=True)
    # last_login_user = db.relationship('LoginSession', backref='current_login_network', lazy='dynamic', foreign_keys='[User.current_login_network_id]')
    