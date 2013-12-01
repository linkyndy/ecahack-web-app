import datetime

from ecahack import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, default='My event')
    start = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow()+datetime.timedelta(hours=-1))
    end = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow()+datetime.timedelta(days=1))
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)

    checkins = db.relationship('Checkin', backref='event')

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    @classmethod
    def get_current(cls):
        return cls.query.filter(cls.start < datetime.datetime.utcnow(),
                                cls.end > datetime.datetime.utcnow()).first()
