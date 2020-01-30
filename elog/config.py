import os

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

SECRET_KEY = os.getenv('SECRET_KEY')


class Config(object):
    # http://flask.pocoo.org/docs/config/#development-production
    DEBUG = True
    SECRET_KEY = SECRET_KEY
    MAX_WHOOSH_SEARCH_RESULTS = 20
    SHOW_ERROR_LOG = False

    # SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Use "if app.debug" anywhere in your code, that code will run in development code."""
    TESTING = False
    CONSOLE_ERROR_LOG = True

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///modelate.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

class LiveConfig(Config):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SHOW_ERROR_LOG = True
