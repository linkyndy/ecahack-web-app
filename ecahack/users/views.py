from flask import Blueprint, render_template

from ecahack import db


user_blueprint = Blueprint('users', __name__, url_prefix='/users')


@user_blueprint.route('/')
def index():
    pass

@user_blueprint.route('/profile')
def profile():
    pass

@user_blueprint.route('/login')
def login():
    pass

@user_blueprint.route('/logout')
def logout():
    pass

@user_blueprint.route('/register')
def register():
    pass
