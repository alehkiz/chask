from flask_wtf.csrf import CSRFProtect
from flask_security import Security
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

csrf = CSRFProtect()
migrate = Migrate()
login = LoginManager()
security = Security()
socketio = SocketIO()