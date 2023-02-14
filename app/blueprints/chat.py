from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, session, url_for, request, g, current_app as app, copy_current_request_context
from flask_login import current_user, login_required
from app.core.extesions import socketio
from uuid import uuid4
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app.models.chat import Message

from app.core.db import db
from app.models.network import Network
from app.models.team import Team
from app.utils.route import authenticated_only
from threading import Lock


thread = None
thread_lock = Lock()

bp = Blueprint('chat', __name__, url_prefix='/chat')

socketio = app.extensions.get('socketio')
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('chat.html')


@bp.route('/team/<uuid:id>')
@login_required
def team(id:uuid4):
    team = Team.query.filter(Team.id == id).first_or_404()
    if not team.has_user(current_user):
        flash('Você não participa desse grupo, solicite ao administrador.', category='warning')
        return redirect(url_for('chat.index'))
    session['room'] = str(team.id)
    session['name'] = current_user.name
    socketio.emit('join', { 'room': session['room']});
    team.add_view_message(current_user)
    return render_template('chat.html', team=team, async_mode=socketio.async_mode)




















