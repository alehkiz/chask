from app.models.base import BaseModel
from app.core.db import db
from sqlalchemy.dialects.postgresql import UUID



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
        UUID(as_uuid=True), db.ForeignKey('network.id'), nullable = False)
    comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', 
        remote_side='Comment.id',
        primaryjoin=('comment.c.id==comment.c.comment_id'),
        backref=db.backref('answer'),#lazy='dynamic'
        )

