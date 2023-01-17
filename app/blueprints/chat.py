from flask import Blueprint, redirect, render_template, session, url_for, request
from flask_login import login_required
from app.core.extesions import socketio


bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))