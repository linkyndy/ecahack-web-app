from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from ecahack.users.views import user_blueprint
app.register_blueprint(user_blueprint)
