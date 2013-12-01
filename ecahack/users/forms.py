from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Length, EqualTo

from ecahack.users.models import User


class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Log in')
