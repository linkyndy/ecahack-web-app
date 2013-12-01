from flask import json
from sqlalchemy.exc import IntegrityError

from ecahack import db
from ecahack.checkins.models import Checkin
from ecahack.events.models import Event
from ecahack.users.models import User

from tests import EcahackTestCase


class ApiEndpointsTests(EcahackTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://:memory:"

    def test_register_user_get_method(self):
        response = self.client.get('/users/register')
        self.assert405(response)

    def test_register_user_post_without_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=1))

    def test_register_user_post_with_invalid_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': 'tooshort'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=2))

    def test_register_user_post_with_valid_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=0))

        self.assertIsNotNone(User.query.get(1))

    def test_register_user_post_with_valid_existing_rfid(self):
        user = User(rfid='12345678901234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=-1))

        self.assertIsNotNone(User.query.get(1))

    def test_add_checkin_get_method(self):
        response = self.client.get('/checkins/add')
        self.assert405(response)

    def test_add_checkin_post_without_rfid(self):
        response = self.client.post('/checkins/add',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=1))

    def test_add_checkin_post_with_invalid_rfid(self):
        response = self.client.post('/checkins/add',
                                    data=json.dumps({'rfid': 'tooshort'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=2))

    def test_add_checkin_post_with_not_existing_valid_rfid(self):
        response = self.client.post('/checkins/add',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=-1))

        self.assertIsNone(User.query.get(1))
        self.assertIsNone(Checkin.query.get(1))

    def test_add_checkin_post_with_existing_valid_rfid_with_no_current_event(self):
        user = User(rfid='12345678901234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/checkins/add',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=3))

        self.assertIsNotNone(User.query.get(1))
        self.assertIsNone(Event.query.get(1))
        self.assertIsNone(Checkin.query.get(1))

    def test_add_checkin_post_with_existing_valid_rfid_with_existing_current_event(self):
        user = User(rfid='12345678901234')
        db.session.add(user)
        db.session.commit()

        event = Event()
        db.session.add(event)
        db.session.commit()

        response = self.client.post('/checkins/add',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=0))

        self.assertIsNotNone(User.query.get(1))
        self.assertIsNotNone(Event.query.get(1))
        self.assertIsNotNone(Checkin.query.get(1))

