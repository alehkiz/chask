from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db
from datetime import datetime
from flask import current_app as app

from app.models.security import User

team_administrators = db.Table('team_administrators',
                            db.Column('team_id', UUID(as_uuid=True), db.ForeignKey('team.id')),
                            db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
                            db.Column("administrator_at", db.DateTime(timezone=True), default=datetime.utcnow)
                            )

class Team(BaseModel):
    __abstract__ = False
    name = db.Column(db.String(512), index=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
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
        primaryjoin=("user_team.c.team_id==team.c.id"),
        secondaryjoin=('user_team.c.user_id==user.c.id'),
        backref=db.backref(
            "teams", lazy='dynamic', #order_by="desc(team_administrators.c.administrator_at)"
        ),
        lazy='dynamic',
        #order_by="desc(team_administrators.c.administrator_at)",
    )
    messages = db.relationship('Message', backref='team', lazy='dynamic')

    def remove_user(self, user:User) -> None:
        if isinstance(user, User):
            self.users.remove(user)
            try:

                db.session.commit()
            except Exception as e:
                app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
                app.logger.error(e)
                raise Exception('Não foi possível remover usuário do time')

class UserTeam(BaseModel):
    __abstract__ = False
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("team.id"), nullable=False)

    
        

    