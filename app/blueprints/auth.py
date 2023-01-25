from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for, g, current_app as app
from flask_login import login_user, current_user
from flask_security import logout_user
from werkzeug.urls import url_parse
from app.forms.login import LoginForm
from app.models.security import LoginSession, User, Role
from app.core.db import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Usuário já logado', category='info')
        return redirect(url_for('main.index'))
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user is None or not user.check_password(login.password.data):
            # print(user.username)
            # print(user.check_password(login.password.data))
            print(login.password.data)
            flash('Senha ou usuário inválido', category='danger')
            return render_template('login.html', form=login, title='Login')
        if not user.is_active:
            flash('Usuário inativo', category='danger')
            return redirect(url_for('auth.login'))
        if user.is_temp_password:
            flash('É necessário alterar sua senha', category='warning')
            return redirect(url_for('auth.temp_password'))
        login_user(user, remember=login.remember_me.data)
        
        login_session = LoginSession()
        login_session.user_id = user.id
        user.login_count += 1
        user.session_token = session["_id"]
        if hasattr(g, 'ip_id'):
            login_session.network_id = g.ip_id
        else:
            return abort(500)
        user.last_seen = datetime.utcnow()
        db.session.add(login_session)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error(app.config.get('_ERRORS').get('DB_COMMIT_ERROR'))
            app.logger.error(e)
            logout_user()
            return redirect(url_for('auth.login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=login, title='Login')


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))