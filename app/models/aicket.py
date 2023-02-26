from datetime import datetime as dt, timedelta
from typing import List, Optional
from app.core.db import db
from app.models.base import BaseModel, str_512, str_32, str_64
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.security import User
from app.models.team import Team
from app.utils.datetime import format_elapsed_time
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, event
from flask import current_app as app
import pytz
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.schema import Sequence

utc = pytz.UTC


class ExceptionMessages:
    TICKET_STAGE_SEQUENCE = "Não é possível fazer essa ação, o estágio que está sendo adicionado não é subsequente ao existente no ticket"
    TRY_CHANGE_CLOSED_DATETIME = "Não é possível incluir ou alterar a data do fechamento por closed_at, altere o atributo closed"
    FUTURE_DEADLINE = "Deadline menor que a data/hora atual."
    TICKET_STAGE_EMPTY = "Os estágios de ticket estão vazios"


class Ticket(BaseModel):
    __abstract__ = False
    name: Mapped[str_512] = mapped_column(db.String(512), index=True)
    title: Mapped[str_512] = mapped_column(db.String(512), index=True)
    info: Mapped[str_512] = mapped_column(db.String(5000), index=True)
    _closed: Mapped[bool] = mapped_column(db.Boolean, default=False)
    deadline: Mapped[dt] = mapped_column(db.DateTime(timezone=True))
    _closed_at: Mapped[bool] = mapped_column(db.DateTime(timezone=True), nullable=True)
    type_id: Mapped[uuid.UUID] = mapped_column(db.ForeignKey("ticket_type.id"))
    create_network_id: Mapped[uuid.UUID] = mapped_column(db.ForeignKey("network.id"))
    create_user_id: Mapped[uuid.UUID] = mapped_column(db.ForeignKey("user.id"))
    costumer_id: Mapped[uuid.UUID] = mapped_column(
        db.ForeignKey("costumer.id")
    )  # Citizen is not nullable
    service_id: Mapped[uuid.UUID] = mapped_column(db.ForeignKey("service.id"))
    comments: Mapped[List["Comment"]] = db.relationship(
        primaryjoin="comment.c.ticket_stage_event_id==ticket_stage_event.c.id",
        secondary="ticket_stage_event",
        secondaryjoin="ticket_stage_event.c.ticket_id == ticket.c.id",
        backref=db.backref("ticket", order_by="desc(Comment.create_at)"),
        lazy="dynamic",
        order_by="desc(Comment.create_at)",
        viewonly=True,
    )
    costumer: Mapped["Costumer"] = db.relationship(backref="tickets", uselist=False)
    stage_events = db.relationship(
        "TicketStageEvent", back_populates="ticket", lazy="dynamic", viewonly=True
    )
    users: Mapped[List["User"]] = db.relationship(
        "User",
        secondary="ticket_stage_event",
        lazy="dynamic",
        back_populates="tickets",
        viewonly=True,
    )
    teams: Mapped[List["Team"]] = db.relationship(
        secondary="ticket_stage_event",
        back_populates="tickets",
        lazy="dynamic",
        viewonly=True,
    )
    costumer: Mapped["Costumer"] = db.relationship(
        backref=db.backref("tickets", lazy="dynamic")
    )
    service: Mapped["Service"] = db.relationship(back_populates="tickets")

    stages: Mapped["Stage"] = association_proxy("stage_events", "stage")

    @property
    def current_user(self):
        if self.current_stage_event != None:
            return self.current_stage_event.user
        return None

    @property
    def current_stage(self):
        if self.current_stage_event != None:
            return self.current_stage_event.stage
        return None

    @property
    def current_stage_event(self):
        return (
            db.session.query(TicketStageEvent)
            .filter(TicketStageEvent.ticket_id == self.id)
            .order_by(TicketStageEvent.create_at.desc())
            .limit(1)
            .first()
        )

    @property
    def last_stage(self):
        return (
            db.session.query(TicketStage)
            .join(TicketStageEvent.stage)
            .filter(TicketStageEvent.ticket_id == self.id)
            .order_by(TicketStage.level.desc())
            .first()
        )

    def has_stage_on_events(self, stage) -> bool:
        return stage in self.stages

    @property
    def is_out_of_date(self):
        now = dt.utcnow()
        if self.current_stage_event is None:
            return False
        return self.current_stage_event.deadline < now

    @hybrid_property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        match value:
            case True:
                self._closed = True
                self.closed_at = dt.utcnow()
            case False:
                self._closed = False

    @property
    def is_closed(self):
        if self._closed is True:
            return True
        else:
            return False

    @hybrid_property
    def closed_at(self):
        return self.closed_at

    @closed.setter
    def closed_at(self, value):
        raise Exception(ExceptionMessages.TRY_CHANGE_CLOSED_DATETIME)

    @property
    def closed_at_elapsed(self):
        return format_elapsed_time(self.closed_at)

    @property
    def deadline_elapsed(self):
        return format_elapsed_time(self.deadline)

    def add_stage(
        self,
        ticket_stage: "TicketStage",
        user: User,
        team: Optional[Team] = None,
        deadline: Optional[dt] = None,
        info: Optional[str] = None,
        closed : Optional[bool] = False
    ) -> "TicketStageEvent":
        
        if deadline is None:
            deadline = dt.now + timedelta(days=7)
        return TicketStageEvent(
            ticket_stage=ticket_stage,
            ticket=self,
            team=team,
            deadline=deadline,
            user=user,
            info=info,
            closed=closed
        )


class TicketType(BaseModel):
    __abstract__ = False
    type: Mapped[str_512] = mapped_column(index=True, nullable=False, unique=True)
    tickets: Mapped[List["Ticket"]] = db.relationship(
        backref="type", lazy="dynamic", single_parent=True
    )


class TicketStage(BaseModel):
    __abstract__ = False
    name: Mapped[str_32] = mapped_column(index=True, unique=True)
    level: Mapped[int] = mapped_column(
        Sequence("ticket_stage_level_seq", start=1, increment=1),
        unique=True,
        autoincrement=True,
    )


class TicketStageEvent(BaseModel):
    __abstract__ = False
    ticket_stage_id: Mapped[uuid.UUID] = mapped_column(
        db.ForeignKey("ticket_stage.id"), nullable=False
    )
    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(db.ForeignKey("team.id"))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(db.ForeignKey("user.id"))
    ticket_id: Mapped[uuid.UUID] = mapped_column(db.ForeignKey("ticket.id"))
    deadline: Mapped[Optional[dt]]
    _closed_at: Mapped[Optional[dt]]
    _closed: Mapped[bool] = mapped_column(default=False)
    info: Mapped[str_64]

    team: Mapped["Team"] = db.relationship(
        back_populates="tickets_stage_event", viewonly=True
    )
    ticket: Mapped["Ticket"] = db.relationship(
        back_populates="stage_events", viewonly=True
    )
    user: Mapped["User"] = db.relationship(
        back_populates="tickets_stage_event", viewonly=True
    )
    stage: Mapped["TicketStage"] = db.relationship(
        primaryjoin="ticket_stage_event.c.ticket_stage_id == ticket_stage.c.id",
        backref=db.backref("events", lazy="dynamic"),
        viewonly=True,
    )
    user_name: Mapped[str_512] = association_proxy("user", "name")
    stage_name: Mapped[str_32] = association_proxy("stage", "name")
    stage_level: Mapped[int] = association_proxy("stage", "level")

    def __init__(
        self,
        ticket_stage: TicketStage,
        ticket: Ticket,
        deadline: Optional[dt] = None,
        team: Optional[Team] = None,
        user: Optional[User] = None,
        info: Optional[str] = None,
        last_event : Optional['TicketStageEvent'] = None,
        closed: Optional[bool] = False,
    ) -> None:
        if isinstance(team, Team):
            self.team_id = team.id
        if deadline < dt.utcnow():
            raise Exception(ExceptionMessages.FUTURE_DEADLINE)
        if isinstance(user, User):
            if not team.has_user(user):
                app.logger.warning(f"O usuário {user.name} não está no {team.name}")
            else:
                self.user_id = user.id
        self.ticket_stage_id = ticket_stage.id
        self.ticket_id = ticket.id
        self.deadline = deadline
        self.info = info
        self.closed = closed
        if isinstance(last_event, TicketStageEvent):
            ticket.last_stage.closed = True
        # try:
        #     db.session.add(self)
        #     db.session.commit()
        # except Exception as e:
        #     app.logger.error(app.config.get("_ERRORS").get("DB_COMMIT_ERROR"))
        #     app.logger.error(e)
        #     raise Exception("Não foi possível salvar TicketStageEvent")

    @staticmethod
    def add(
        ticket_stage: TicketStage,
        user: User,
        ticket: Ticket,
        team: Team,
        deadline: dt,
        info: Optional[str] = None,
        close_last: bool = False,
        force: bool = False,
    ):
        if ticket.last_stage.level == 1 != ticket_stage.level:
            raise Exception(ExceptionMessages.TICKET_STAGE_SEQUENCE)
        query = (
            db.session.query(TicketStageEvent)
            .filter(
                TicketStageEvent.ticket_stage_id == ticket_stage.id,
                TicketStageEvent.user_id == user.id,
                TicketStageEvent.ticket_id == ticket.id,
                TicketStageEvent.team_id == team.id,
            )
            .order_by(TicketStageEvent.create_at.desc())
        )  # mais recente primeiro
        if query.count() > 0 and force is False:
            raise Exception("Não é possível adicionar o evento, já há um cadastro")
        else:
            tse = TicketStageEvent(
                user_id=user.id,
                ticket_id=ticket.id,
                ticket_stage_id=ticket_stage.id,
                deadline=deadline,
                info=info,
            )
        if close_last is True:
            last_event = (
                db.session.query(TicketStageEvent)
                .filter(
                    TicketStageEvent.ticket_id == ticket.id,
                )
                .order_by(TicketStageEvent.create_at.desc())
                .first()
            )
            if not last_event is None:
                last_event.closed = True
        try:
            db.session.add(tse)
            db.session.commit()
            return tse
        except Exception as e:
            app.logger.error(app.config.get("_ERRORS").get("DB_COMMIT_ERROR"))
            app.logger.error(e)
            raise Exception("Não foi possível salvar o IP")

    @hybrid_property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        match value:
            case True:
                self._closed = True
                self._closed_at = dt.utcnow()
            case False:
                self._closed = False

    @property
    def is_closed(self):
        if self._closed is True:
            return True
        else:
            return False

    @hybrid_property
    def closed_at(self):
        return self.closed_at

    @closed.setter
    def closed_at(self, value):
        raise Exception(ExceptionMessages.TRY_CHANGE_CLOSED_DATETIME)

    @property
    def closed_at_elapsed(self):
        return format_elapsed_time(self.closed_at)

    @property
    def deadline_elapsed(self):
        return format_elapsed_time(self.deadline)


# @event.listens_for(TicketStage.collection, 'append', propagate=True)
# def my_append_listener(target, value, initiator):
#     print("received append event for target: %s" % target)
@event.listens_for(Ticket, "after_insert")
def receive_after_create(mapper, connection, target):
    from flask_login import current_user
    deadline = dt.today() + timedelta(days=7)
    ts = TicketStage.query.filter(TicketStage.level == 0).first()
    if ts is None:
        raise Exception(ExceptionMessages.TICKET_STAGE_EMPTY)
    tse = target.add_stage(ticket_stage=ts, user=current_user, deadline=deadline, info='', closed=True)
    @event.listens_for(db.session, "after_flush", once=True)
    def after_flush(session, context):
        session.add(tse)
        # session.commit()
    # db.session.commit()
