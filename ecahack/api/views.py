from flask import Blueprint, request, jsonify

from ecahack import db
from ecahack.checkins.models import Checkin
from ecahack.events.models import Event
from ecahack.users.models import User


api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/register_user', methods=['GET'])
def register():
    """
    Response codes:
        0: success
        1: no rfid param
        2: invalid rfid param
        -1: already registered
    """

    rfid = request.args.get('rfid', None)

    if not rfid:
        return jsonify(code=1)

    if len(rfid) != 14:
        return jsonify(code=2)

    user = User.query.filter_by(rfid=rfid).first()

    if user is not None:
        return jsonify(code=-1)

    user = User(rfid=rfid)

    db.session.add(user)
    db.session.commit()

    return jsonify(code=0)


@api_blueprint.route('/add_checkin', methods=['GET'])
def add():
    """
    Response codes:
        0: success
        1: no rfid param
        2: invalid rfid param
        3: no current event
        -1: user not registered
    """

    rfid = request.args.get('rfid', None)

    if not rfid:
        return jsonify(code=1)

    if len(rfid) != 14:
        return jsonify(code=2)

    user = User.query.filter_by(rfid=rfid).first()

    if user:
        event = Event.get_current()

        if not event:
            return jsonify(code=3)

        checkin = Checkin(user_id=user.id, event_id=event.id)

        db.session.add(checkin)
        db.session.commit()

        return jsonify(code=0)

    return jsonify(code=-1)
