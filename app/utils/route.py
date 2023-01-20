from functools import wraps
from flask import abort, request, g, current_app as app
from flask_login import current_user
from werkzeug.urls import url_parse
from app.models.network import Network
from app.models.page import Page
from app.core.db import db


def counter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = None
        if current_user.is_authenticated:
            user_id = current_user.id
        page = Page.query.filter(Page.endpoint == request.endpoint).first()
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
        if page is None:
            page = Page()
            page.endpoint = request.endpoint
            page.route = request.url_rule.rule.split('<')[0]
            db.session.add(page)
        try:
            db.session.commit()
            page.add_view(user_id, g.ip_id)
        except Exception as e:
            db.session.rollback()
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            return abort(500)
        return f(*args, **kwargs)
    return decorated_function


def url_in_host(url):
    if url_parse(url).netloc == url_parse(request.base_url).netloc:
        return True
    return False