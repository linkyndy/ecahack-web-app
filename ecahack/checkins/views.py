from flask import Blueprint, render_template, request, jsonify
from flask.ext.login import login_required, current_user

from ecahack import db
from ecahack.checkins.models import Checkin
from ecahack.events.models import Event
from ecahack.users.models import User


checkin_blueprint = Blueprint('checkins', __name__, url_prefix='/checkins')
