from flask import Blueprint, render_template, request, jsonify
from flask.ext.login import login_required, current_user

from ecahack import db
from ecahack.users.models import User


user_blueprint = Blueprint('users', __name__, url_prefix='/users')


@user_blueprint.route('/')
def index():
    pass

@user_blueprint.route('/profile')
@login_required
def profile():
    pass

@user_blueprint.route('/login')
def login():
    pass

@user_blueprint.route('/logout')
@login_required
def logout():
    pass

@user_blueprint.route('/register', methods=['POST'])
def register():
    json = request.get_json()

    if not json.get('rfid', None):
        return jsonify(type=u'error', message=u'No RFID parameter sent.')

    if len(json['rfid']) != 14:
        return jsonify(type=u'error', message=u'Invalid RFID parameter sent.')

    user = User.query.filter_by(rfid=json['rfid']).first()

    if user is not None:
        return jsonify(type=u'success', message=u'User already registered with'
                                                 ' RFID %s' % json['rfid'])

    user = User(rfid=json['rfid'])

    db.session.add(user)
    db.session.commit()

    return jsonify(type=u'success', message=u'Successfully registered user with'
                                             ' RFID %s' % json['rfid'])
