from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user
from github_loader import db
from github_loader.models import UserLogin
from github_loader.users.forms import LoginForm
from github import Github
from github.GithubException import BadCredentialsException, GithubException
import pickle
from github_loader import LOGGER
from sqlalchemy.exc import SQLAlchemyError, DatabaseError

users = Blueprint('users', __name__)


@users.route("/")
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            github = Github(form.user_name.data, form.password.data)
            github_user = github.get_user().raw_data
        except BadCredentialsException as e:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            LOGGER.error(f"Login to GitHub Failed, user: {form.user_name.data}, error {e}")
            return render_template('login.html', title='Login', form=form)
        except GithubException as e:
            LOGGER.error(f"An error occurred, error {e}")

        user = UserLogin(github_user=github_user)
        session['github_user'] = pickle.dumps(github.get_user())
        db.session.add(user)
        try:
            db.session.commit()
        except (SQLAlchemyError, DatabaseError) as e:
            LOGGER.error(f"DB error: {e} ")
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


