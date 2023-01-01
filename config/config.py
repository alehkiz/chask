from os import environ
from os.path import abspath, dirname, join

import app

class BaseConfig(object):
    PROJECT_NAME = 'chask'
    SITE_TITLE = PROJECT_NAME
    SECRET_KEY = environ.get('SERVER_KEY')
    SECURITY_PASSWORD_SALT = environ.get('PASSWORD_SALT')
    APP_DIR = abspath(dirname(app.__file__))
    BASE_DIR = abspath(join(APP_DIR, '..'))
    BLUEPRINTS_DIR = join(APP_DIR, 'blueprints')

    _SQLALCHEMY_DATABASE_NAME = environ.get('DATABASE', False) or PROJECT_NAME.lower()
    _SQLALCHEMY_DATABASE_HOST = environ.get('DB_HOST')
    _SQLALCHEMY_DATABASE_USERNAME = environ.get('DB_USER')
    _SQLALCHEMY_DATABASE_PASSWORD = environ.get('DB_PASS')
    _SQLALCHEMY_DATABASE_PORT = environ.get('DB_PORT')
    _ERRORS = {'DB_COMMIT_ERROR': 'Não foi possível atualizar o banco de dados'}

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{BaseConfig._SQLALCHEMY_DATABASE_USERNAME}:{BaseConfig._SQLALCHEMY_DATABASE_PASSWORD}@{BaseConfig._SQLALCHEMY_DATABASE_HOST}:{BaseConfig._SQLALCHEMY_DATABASE_PORT}/{BaseConfig._SQLALCHEMY_DATABASE_NAME}_dev'
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{BaseConfig._SQLALCHEMY_DATABASE_USERNAME}:{BaseConfig._SQLALCHEMY_DATABASE_PASSWORD}@{BaseConfig._SQLALCHEMY_DATABASE_HOST}:{BaseConfig._SQLALCHEMY_DATABASE_PORT}/{BaseConfig._SQLALCHEMY_DATABASE_NAME}'

config = {'development': DevelopmentConfig,
          'production': ProductionConfig}