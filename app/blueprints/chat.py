from datetime import datetime
from flask import Blueprint, abort, redirect, render_template, session, url_for, request, g, current_app as app
from flask_login import current_user, login_required
from app.core.extesions import socketio
from uuid import uuid4
from flask_socketio import emit, join_room, leave_room
from app.models.chat import Message

from app.core.db import db
from app.models.network import Network
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
    session['room'] = team.id
    session['name'] = current_user.name
    team.add_view_message(current_user)
    return render_template('chat.html', team=team)

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    name = session.get('name')
    join_room(room)
    emit('status', {'name':name}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    if not hasattr(g, 'id_id'):
        ip = Network.query.filter(
            Network.ip == request.remote_addr).first()
        if ip is None:
            ip = Network()
            ip.ip = request.remote_addr
            db.session.add(ip)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                app.logger.error(app.config.get(
                    '_ERRORS').get('DB_COMMIT_ERROR'))
                app.logger.error(e)
                return abort(500)
            g.ip_id = ip.id
        else:
            g.ip_id = ip.id
    room = session.get('room')
    msg = Message()
    msg.message = message['msg']
    msg.create_network_id = g.ip_id
    msg.user_sender_id = current_user.id
    msg.team_id = session.get('room')
    try:
        db.session.add(msg)
        db.session.commit()
        print(msg.id)
    except Exception as e:
        app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
        app.logger.error(e)
        raise Exception('Não foi possível salvar a mensagem')
    msg_dict = {'username': current_user.username,
          'name': current_user.name,
          'timestamp': datetime.utcnow().isoformat(),
          'message_id': str(msg.id),
          'message': message['msg']}
    print(msg_dict)
    emit('message', msg_dict, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': f"{session.get('name')}  has left the room."}, room=room)