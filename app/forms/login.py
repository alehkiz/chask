from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3,max=32, message='Usuário deve ter entre 3 e 32 caracteres')])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6,max=64, message='Senha deve ter entre 6 e 64 caracteres')])
    remember_me = BooleanField('Manter conectado', default=True, render_kw ={'checked':''})
    submit = SubmitField('Logar')