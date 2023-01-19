from datetime import datetime
from typing import Optional
from app.models.base import BaseModel
from app.core.db import db
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app as app
from app.models.security import User

comment_read_state = db.Table('comment_read_state',
        db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
        db.Column('comment_id', UUID(as_uuid=True), db.ForeignKey('comment.id')),
        db.Column('create_at', db.DateTime(timezone=True), default=datetime.utcnow)
        )


class Comment(BaseModel):
    __abstract__=False
    ticket_id=db.Column(UUID(as_uuid=True), db.ForeignKey(
        'ticket.id'), nullable = False)
    user_id=db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id'), nullable = False)
    text=db.Column(db.Text, nullable = False)
    create_network_id=db.Column(
        UUID(as_uuid=True), db.ForeignKey('network.id'), nullable = False)
    update_network_id=db.Column(
        UUID(as_uuid=True), db.ForeignKey('network.id'))
    comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('comment.id'))
    replies_to = db.relationship(
        'Comment', 
        remote_side='Comment.id',
        primaryjoin=('comment.c.id==comment.c.comment_id'),
        backref=db.backref('answers'),#lazy='dynamic' #TODO:Create a way to relationhip is lazy to query `answers`
        
        )
    user_read_state = db.relationship('User', secondary=comment_read_state,
            backref=db.backref('comments_readed',lazy='dynamic', order_by='desc(comment_read_state.c.create_at)'), lazy='dynamic',order_by='desc(comment_read_state.c.create_at)')


    def read_comment(self, user: User) -> None:
        if not user is None and hasattr(user, 'id'):
            self.user_read_state.append(user)
            try:
                db.session.commit()
            except Exception as e:
                app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
                app.logger.error(e)
                raise Exception('Não foi possível ler o comentário')