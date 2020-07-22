from flask import Flask

from config import Config
from celery import Celery
from .celery_utils import init_celery
from toolkit import dbAlchemy



def create_app(**kwargs):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    dbAlchemy.init_app(app)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)
    with app.app_context():
        # Import routes
        import toolkit.routes
        dbAlchemy.create_all()  # Create sql tables for our data models
        return app