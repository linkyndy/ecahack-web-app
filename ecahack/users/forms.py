from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Length, EqualTo

from ecahack.users.models import User


class LoginForm(Form):
    username_or_rfid = TextField('Username or RFID', [Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Log in')


class RefreshLoginForm(Form):
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Log in')

