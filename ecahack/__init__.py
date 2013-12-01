from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.init_app(app)

from ecahack.api.views import api_blueprint
from ecahack.checkins.views import checkin_blueprint
from ecahack.users.views import user_blueprint
app.register_blueprint(api_blueprint)
app.register_blueprint(checkin_blueprint)
app.register_blueprint(user_blueprint)
