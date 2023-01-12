from flask import Blueprint, redirect, render_template, session, url_for, request


bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('base/base.html')
