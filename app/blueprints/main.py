from uuid import uuid4
from flask import Blueprint, abort, jsonify, redirect, render_template, session, url_for, request, current_app as app, g
from flask_login import login_required
from flask_security import roles_accepted
from app.core.db import db
from app.models.network import Network
from app.utils.route import counter
from app.core.extesions import login

bp = Blueprint('main', __name__, url_prefix='/')


# @bp.before_app_first_request
# def before_first_request():
#     print(f'First request at: {datetime.utcnow()}')

@bp.before_app_request
def before_app_request():
    if request.endpoint != 'static':
        if session.get('uuid', False) is False:
            session['uuid'] = app.login_manager._session_identifier_generator()
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
@bp.teardown_request
def teardown_request(exception):
    if not exception is None:
        try:
            db.session.close()
        except Exception as e:
            db.session.rollback()
            app.logger.error(app.config.get("_ERRORS").get("DB_COMMIT_ERROR"))
            app.logger.error(e)

@bp.route('/')
@bp.route('/index/')
@counter
def index():
    return render_template('base/base.html')




_security = app.extensions["security"]
@_security.unauthz_handler
def my_unauthz_handler(func, params):
#     print('aqui')
    print(request.is_json)
    if request.is_json:
        return jsonify(success=False,
                       data={'role_required': True},
                       message='Você não tem acesso ao conteudo.'), 401
    else:
        return render_template('errors/401.html'), 401

@bp.route('/unauthorized/')
@counter
def unauthorized():
    # print(login.unauthorized_callback())
    return render_template('errors/401.html')

@bp.route('/adm/')
@login_required
# @roles_accepted('admin', 'support')
def adm():
    return render_template('base/base.html')