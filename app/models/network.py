
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime
from app.core.db import db
from app.utils.kernel import convert_datetime_to_local

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(INET, nullable=False)
    create_at = db.Column(db.DateTime(timezone=True), default=convert_datetime_to_local(datetime.utcnow()))
    created_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_user = db.relationship('User', backref='created_network', lazy='dynamic', foreign_keys='[User.created_network_id]')
    confirmed_user = db.relationship('User', backref='confirmed_network', lazy='dynamic', foreign_keys='[User.confirmed_network_id]')