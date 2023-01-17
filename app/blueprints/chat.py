from flask import Blueprint, redirect, render_template, session, url_for, request
from flask_login import login_required
from app.core.extesions import socketio
from uuid import uuid4

from app.models.team import Team

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('chat.html')


@bp.route('/team/<uuid:id>')
@login_required
def team(id):
    team = Team.query.filter(Team.id == id).first_or_404()
    return render_template('chat.html', team=team)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))