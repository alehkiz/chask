from datetime import datetime
from flask import Blueprint, abort, redirect, render_template, session, url_for, request, g, current_app as app
from flask_login import current_user, login_required
from flask_security import roles_accepted
from uuid import uuid4
from app.models.ticket import Ticket

from app.core.db import db
from app.models.network import Network
from app.models.team import Team

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('/')
@bp.route('/index')
@login_required
@roles_accepted('support')
def index():
    return render_template('ticket.html')