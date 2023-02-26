from datetime import datetime
from typing import List, Optional
from app.models.base import BaseModel, str_256
from app.core.db import db
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app as app
from app.models.security import User
import uuid
from sqlalchemy.orm import Mapped, mapped_column

comment_read_state = db.Table(
    "comment_read_state",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("user.id")),
    db.Column("comment_id", UUID(as_uuid=True), db.ForeignKey("comment.id")),
    db.Column("create_at", db.DateTime(timezone=True), default=datetime.utcnow),
)


class Comment(BaseModel):
    __abstract__ = False
    ticket_id: Mapped[uuid.UUID] = db.mapped_column(
        db.ForeignKey("ticket.id")
    )
    user_id: Mapped[uuid.UUID] = db.mapped_column(
        db.ForeignKey("user.id")
    )
    create_network_id: Mapped[uuid.UUID] = db.mapped_column(
        db.ForeignKey("network.id")
    )
    update_network_id: Mapped[Optional[uuid.UUID]] = db.mapped_column(db.ForeignKey("network.id"))
    ticket_stage_event_id: Mapped[Optional[uuid.UUID]] = db.mapped_column(
        db.ForeignKey("ticket_stage_event.id")
    )
    comment_id: Mapped[Optional[uuid.UUID]] = db.mapped_column(
        db.ForeignKey("comment.id")
    )
    text: Mapped[str_256]
    replies_to: Mapped[List["Comment"]] = db.relationship(
        remote_side="Comment.id",
        primaryjoin=("comment.c.id==comment.c.comment_id"),
        backref=db.backref(
            "answers"
        ),  # lazy='dynamic' #TODO:Create a way to relationhip is lazy to query `answers`
        viewonly=True,
    )
    # author = db.relationship('User', primaryjoin='comment.c.user_id==user.c.id')#, backref=db.backref('writed_comments', lazy='dynamic'))
    # author = db.relationship('User', back_populates='comments_writed',  lazy='dynamic')
    user_read_state: Mapped[List["User"]] = db.relationship(
        secondary=comment_read_state,
        backref=db.backref(
            "comments_readed",
            lazy="dynamic",
            order_by="desc(comment_read_state.c.create_at)",
        ),
        lazy="dynamic",
        order_by="desc(comment_read_state.c.create_at)",
    )
    # ticket = db.relationship('Ticket', backref=db.backref('comments', lazy='dynamic', order_by='desc(comment.create_at)'), lazy='dynamic', order_by='desc(comment.c.create_at)')
    ticket_event: Mapped["TicketStageEvent"] = db.relationship(
        backref=db.backref(
            "comments", lazy="dynamic", order_by="desc(Comment.create_at)"
        ),
        uselist=False,
        order_by="desc(Comment.create_at)",
        viewonly=True,
    )

    def read_comment(self, user: User) -> None:
        if not user is None and hasattr(user, "id"):
            self.user_read_state.append(user)
            try:
                db.session.commit()
            except Exception as e:
                app.logger.error(app.config.get("_ERRORS").get("DB_COMMIT_ERROR"))
                app.logger.error(e)
                raise Exception("Não foi possível ler o comentário")
