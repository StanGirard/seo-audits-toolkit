"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', "changeme")
    URL_APP = environ.get('URL_APP', "http://localhost:5000")
    FLASK_APP = environ.get('FLASK_APP', "SEOToolkit")
    FLASK_ENV = environ.get('FLASK_ENV', 'development')
    GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY', "None")
    
    # Celery
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL','redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND','redis://localhost:6379/0')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False