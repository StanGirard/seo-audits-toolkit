from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from toolkit.celery import make_celery
from config import Config
from celery import Celery
dbAlchemy = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,backend=Config.CELERY_RESULT_BACKEND, include=["toolkit.celery.tasks"])
def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    dbAlchemy.init_app(app)
    celery = make_celery(app)
    with app.app_context():
        import toolkit.routes  # Import routes
        dbAlchemy.create_all()  # Create sql tables for our data models
       
        return app, celery