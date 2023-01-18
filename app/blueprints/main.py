from flask import Blueprint, abort, redirect, render_template, session, url_for, request, current_app as app, g
from flask_login import login_required
from flask_security import roles_accepted
from app.core.db import db
from app.models.network import Network
from app.utils.route import counter

bp = Blueprint('main', __name__, url_prefix='/')

# @bp.before_app_first_request
# def before_first_request():
#     print(f'First request at: {datetime.utcnow()}')

@bp.before_app_request
def before_app_request():
    if request.endpoint != 'static':
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
        print(g.ip_id)
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


@bp.route('/adm/')
@login_required
# @roles_accepted('admin', 'support')
def adm():
    return render_template('base/base.html')