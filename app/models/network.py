
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class Network(BaseModel):
    __abstract__ = False
    ip : Mapped[INET] = db.mapped_column(INET, nullable=False)
    # created_user_id = db.mapped_column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    created_user = db.relationship('User', backref='created_network', lazy='dynamic', foreign_keys='[User.created_network_id]')
    confirmed_user = db.relationship('User', backref='confirmed_network', lazy='dynamic', foreign_keys='[User.confirmed_network_id]')
    comemnts_created = db.relationship('Comment', backref='created_network', lazy='dynamic', foreign_keys='[Comment.create_network_id]')
    comments_updated = db.relationship('Comment', backref='update_network', lazy='dynamic', foreign_keys='[Comment.update_network_id]')
    messages_created = db.relationship('Message', backref='creted_network', lazy='dynamic', foreign_keys='[Message.create_network_id]')
    visits = db.relationship('Visit', backref='network', lazy='dynamic', single_parent=True)
    tickets = db.relationship('Ticket', backref='network', lazy='dynamic', single_parent=True)
    sessions = db.relationship('LoginSession', backref='network', lazy='dynamic', single_parent=True)
    # last_login_user = db.relationship('LoginSession', backref='current_login_network', lazy='dynamic', foreign_keys='[User.current_login_network_id]')
    