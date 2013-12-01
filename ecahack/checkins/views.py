from flask import Blueprint, render_template, request, jsonify
from flask.ext.login import login_required, current_user

from ecahack import db
from ecahack.checkins.models import Checkin
from ecahack.events.models import Event
from ecahack.users.models import User


checkin_blueprint = Blueprint('checkins', __name__, url_prefix='/checkins')


@checkin_blueprint.route('/add', methods=['POST'])
def add():
    """
    Response codes:
        0: success
        1: no rfid param
        2: invalid rfid param
        3: no current event
        -1: user not registered
    """

    json = request.get_json()

    if not json.get('rfid', None):
        return jsonify(code=1)

    if len(json['rfid']) != 14:
        return jsonify(code=2)

    user = User.query.filter_by(rfid=json['rfid']).first()

    if user:
        event = Event.get_current()

        if not event:
            return jsonify(code=3)

        checkin = Checkin(user_id=user.id, event_id=event.id)

        db.session.add(checkin)
        db.session.commit()

        return jsonify(code=0)

    return jsonify(code=-1)
