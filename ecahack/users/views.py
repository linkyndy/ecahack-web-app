from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash)
from flask.ext.login import login_required, current_user

from ecahack import db
from ecahack.users.models import User
from ecahack.users.forms import LoginForm, RefreshLoginForm


user_blueprint = Blueprint('users', __name__, url_prefix='/users')


@user_blueprint.route('/')
def index():
    pass

@user_blueprint.route('/profile')
@login_required
def profile():
    pass

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            if login_user(user):
                flash('Logged in!', 'success')
            return redirect(url_for('user.profile'))

        flash('Invalid login data', 'error')

    return render_template('users/login.html', form=form)

@user_blueprint.route('/refresh-login', methods=['GET', 'POST'])
@login_required
def refresh_login():
    form = RefreshLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(current_user.username, form.password.data)

        if user:
            confirm_login()
            flash('Refreshed login', 'success')
            return redirect(url_for('user.profile'))

        flash('Invalid password', 'error')

    return render_template('users/refresh_login.html', form=form)

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('users.index'))
