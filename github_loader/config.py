import os

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOG_FILE_PATH = os.path.join(BASEDIR, 'logs/log.txt')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sfvmkldkfmlmkasdlmcaslkdmclsdc'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    DEBUG_MODE = os.environ.get('DEBUG_MODE') or False

