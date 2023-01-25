from flask import Flask
from flask.cli import with_appcontext

from logging.handlers import RotatingFileHandler
import logging
from datetime import datetime
from os.path import exists
from os import mkdir

from app.blueprints import register_blueprints
from app.core.extesions import csrf, login, migrate, security, socketio, uuid
# from app.models.network import Network
# from app.models.page import Page, Visit

# from app.models.client import Client
# from app.models.contact import Contact
from app.core.db import db, user_datastore
from app.models import get_class_models #dict of models


login.login_view = 'auth.login'
login.login_message = 'Faça login para acessar a página'
login.login_message_category = 'danger'
for k, v in get_class_models().items():
    globals()[k] = v # Add all models to globals # Force import, to initialize app

def init(app: Flask):
    security.init_app(app, datastore=user_datastore, register_blueprint=False)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    csrf.init_app(app)
    login.init_app(app)
    login.session_protection = 'strong'
    socketio.init_app(app)
    uuid.init_app(app)

    @app.shell_context_processor
    @with_appcontext
    def shell_context():
        app.config['SERVER_NAME'] = 'localhost'
        ctx = app.test_request_context()
        ctx.push()

        return dict(app=app, db=db, **get_class_models())

    print(f'{"*" * 25} Servidor iniciado: {datetime.utcnow()} {"*" * 25}')

    if app.debug is not True:
        if not exists('logs'):
            mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/erros.log', maxBytes=1024000, backupCount=100)
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"))
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    register_blueprints(app)
    @login.user_loader
    def load_user(session_token):
        try:
            from app.models.security import User
            user = User.query.filter_by(session_token=session_token).first()
        except Exception as e:
            db.session.rollback()
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            return None
        return user
        
    return app
