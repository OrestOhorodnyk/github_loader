from datetime import datetime
from github_loader import db, login_manager
from flask_login import UserMixin
from sqlalchemy import DateTime


@login_manager.user_loader
def load_user(user_login_id):
    return UserLogin.query.get(int(user_login_id))


class UserLogin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    github_id = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_date = db.Column(DateTime, default=datetime.utcnow)

    def __init__(self, github_user):
        self.github_id = github_user['id']
        self.username = github_user['name']
        self.email = github_user['email']
        self.authenticated = True

    def __repr__(self):
        return f"User('{self.id}, {self.github_id}, {self.username}', '{self.email}, {self.created_date}'"


class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_login_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), nullable=False)

    def __repr__(self):
        return f"Load('{self.id}', '{self.date_posted}', {self.user_login_id})"
