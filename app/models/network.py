
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
from app.core.db import db
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Network(BaseModel):
    __abstract__ = False
    ip = db.Column(INET, nullable=False)
    # created_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    created_user = db.relationship('User', backref='created_network', lazy='dynamic', foreign_keys='[User.created_network_id]')
    confirmed_user = db.relationship('User', backref='confirmed_network', lazy='dynamic', foreign_keys='[User.confirmed_network_id]')
    coments_created = db.relationship('Comment', backref='created_network', lazy='dynamic', foreign_keys='[Comment.create_network_id]')
    coments_updated = db.relationship('Comment', backref='update_network', lazy='dynamic', foreign_keys='[Comment.update_network_id]')
    visits = db.relationship('Visit', backref='network', lazy='dynamic', single_parent=True)
    tickets = db.relationship('Ticket', backref='network', lazy='dynamic', single_parent=True)
    last_login_user = db.relationship('LoginSession', backref='login_network', lazy='dynamic')