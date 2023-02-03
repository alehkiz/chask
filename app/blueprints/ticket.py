from datetime import datetime
from flask import Blueprint, abort, redirect, render_template, session, url_for, request, g, current_app as app
from flask_login import current_user, login_required
from flask_security import roles_accepted
from uuid import uuid4
from app.models.ticket import Ticket, TicketStageEvent

from app.core.db import db
from app.models.network import Network
from app.models.team import Team

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('/')
@bp.route('/index')
@login_required
@roles_accepted('support', 'admin')
def index():
    return render_template('ticket.html')


@bp.route('/view/<uuid:id>')
@login_required
def view(id:uuid4):
    ticket = Ticket.query.filter(Ticket.id == id).first_or_404()
    return str(ticket.id)


@bp.route('/delayed')
@login_required
@roles_accepted('support', 'ticket')
def delayed():
    tickets_events = current_user.tickets_datetime_deadline().order_by(TicketStageEvent.deadline.asc())
    return render_template('list_tickets.html', tickets_events=tickets_events)