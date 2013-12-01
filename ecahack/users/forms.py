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


class RegisterForm(Form):
    rfid = TextField('RFID', [Required(), Length(14, 14)])
    username = TextField('Username', [Length(3, 64)])
    password = PasswordField('Password', [Required(), Length(3, 64)])
    confirm_password = PasswordField('Confirm password',
                                     [EqualTo('password',
                                              message='Passwords don\'t match')])
    submit = SubmitField('Register user')


    def validate_rfid(self, field):
        if User.query.filter_by(rfid=field.data).first():
            raise ValidationError('RFID already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')

