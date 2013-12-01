import datetime

from flask.ext.login import UserMixin
from flask.ext.scrypt import generate_random_salt, generate_password_hash, \
                             check_password_hash

from ecahack import db
from ecahack.users.constants import ADMIN, USER, ROLES


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rfid = db.Column(db.String(14), nullable=False)
    username = db.Column(db.String(64), nullable=True)
    _password = db.Column('password', db.String(64), nullable=False)
    _role = db.Column('role', db.SmallInteger, nullable=False, default=USER)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    checkins = db.relationship('Checkin', backref='user')

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(_get_password,
                                                           _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, username_or_rfid, password):
        user = cls.query.filter(db.or_(cls.username == username_or_rfid,
                                       cls.rfid == username_or_rfid)).first()

        if user and user.check_password(password):
            return user

        return False

    def _get_role(self):
        return ROLES[self._role]

    def _set_role(self, role):
        self._role = role

    role = db.synonym('_role', descriptor=property(_get_role, _set_role))

    def is_admin(self):
        return self.role == 'admin'

    def __init__(self, rfid, username=None, password=None):
        self.rfid = rfid
        self.username = username or rfid
        self._password = password or generate_random_salt()
