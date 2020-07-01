"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', "changeme")
    FLASK_APP = environ.get('FLASK_APP', "SEOToolkit")
    FLASK_ENV = environ.get('FLASK_ENV', 'development')
    GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY', "None")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False