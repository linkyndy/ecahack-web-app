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
    """
    Response codes:
        0: success
        1: no rfid param
        2: invalid rfid param
        -1: already registered
    """

    json = request.get_json()

    if not json.get('rfid', None):
        return jsonify(code=1)

    if len(json['rfid']) != 14:
        return jsonify(code=2)

    user = User.query.filter_by(rfid=json['rfid']).first()

    if user is not None:
        return jsonify(code=-1)

    user = User(rfid=json['rfid'])

    db.session.add(user)
    db.session.commit()

    return jsonify(code=0)
