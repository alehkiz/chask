from flask import Blueprint, redirect, session, url_for, request


bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/')
@bp.route('/index')
def index():
    return ''
