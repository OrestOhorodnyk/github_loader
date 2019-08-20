from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, DateTime, String, ForeignKey
from flask_login import LoginManager
from github_loader.config import Config, LOG_FILE_PATH
from github_loader.utils.get_logger import make_logger

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
LOGGER = make_logger(LOG_FILE_PATH, 'logger')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    from github_loader.users.routes import users
    from github_loader.repositories.routes import repositories
    from github_loader.main.routes import main
    from github_loader.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(repositories)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
