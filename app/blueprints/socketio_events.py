from datetime import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import abort, copy_current_request_context, current_app as app, g, session, request, url_for
from flask_login import current_user
from app.models.chat import Message
from app.models.network import Network
from app.core.db import db

from app.utils.route import authenticated_only
from threading import Lock
thread = None
thread_lock = Lock()
socketio = app.extensions.get('socketio')
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})



@socketio.on('joined', namespace='/chat')
@authenticated_only
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    if current_user.is_authenticated:
        room = session.get('room')
        name = session.get('name')
        join_room(room)
        emit('status', {'name':name}, room=room)
    else:
        print("erro")
        return False


@socketio.on('message_team', namespace='/chat')
@authenticated_only
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    print(message)
    if current_user.is_authenticated:
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
        msg.message = message['data']
        msg.create_network_id = g.ip_id
        msg.user_sender_id = current_user.id
        msg.team_id = session.get('room')
        try:
            db.session.add(msg)
            db.session.commit()
        except Exception as e:
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            raise Exception('Não foi possível salvar a mensagem')
        msg_dict = {'username': current_user.username,
            'name': current_user.name,
            'timestamp': datetime.utcnow().isoformat(),
            'message_id': str(msg.id),
            'message': message['data'],
            'avatar': url_for("static", filename="images/profile.png")
            }
        emit('message', msg_dict, room=room)
    else:
        return False


@socketio.on('left', namespace='/chat')
# @authenticated_only
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    if current_user.is_authenticated:
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': f"{session.get('name')}  has left the room."}, room=room)
    else:
        return False















# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0})

# @socketio.event
# def my_event(message):
#     print(message)
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     socketio.emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
    


# @socketio.event
# def my_broadcast_event(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)


# @socketio.event
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})


# @socketio.on('close_room')
# def on_close_room(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          to=message['room'])
#     close_room(message['room'])


# @socketio.event
# def my_room_event(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          to=message['room'])


# @socketio.event
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     session['receive_count'] = session.get('receive_count', 0) + 1
#     # for this emit we use a callback function
#     # when the callback function is invoked we know that the message has been
#     # received and it is safe to disconnect
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)


# @socketio.event
# def my_ping():
#     emit('my_pong')


# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     print("aqui")
#     emit('my_response', {'data': 'Connected', 'count': 0})


# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected', request.sid)


# @socketio.event
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
