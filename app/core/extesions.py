from flask_wtf.csrf import CSRFProtect
from flask_security import Security
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_uuid import FlaskUUID
csrf = CSRFProtect()
migrate = Migrate()
login = LoginManager()
security = Security()
socketio = SocketIO()
uuid = FlaskUUID()