from flask import json
from sqlalchemy.exc import IntegrityError

from ecahack import db
from ecahack.users.models import User

from tests import EcahackTestCase


class ApiEndpointsTests(EcahackTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://:memory:"

    def test_register_get_method(self):
        response = self.client.get('/users/register')
        self.assert405(response)

    def test_register_post_without_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=1))

    def test_register_post_with_invalid_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': 'tooshort'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=2))

    def test_register_post_with_valid_rfid(self):
        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=0))

        self.assertIsNotNone(User.query.get(1))

    def test_register_post_with_valid_existing_rfid(self):
        user = User(rfid='12345678901234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/users/register',
                                    data=json.dumps({'rfid': '12345678901234'}),
                                    content_type='application/json')
        self.assert200(response)
        self.assertEquals(response.json, dict(code=-1))

        self.assertIsNotNone(User.query.get(1))

