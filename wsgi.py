from app import create_app
from app.core.extesions import socketio

app = create_app(mode='development')

if __name__ == '__main__':
    socketio.run(app=app, debug=True) # Actually, the only way for SockeIO run over events