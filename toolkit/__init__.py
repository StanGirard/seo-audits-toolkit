from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from toolkit.celeryapp import make_celery
from config import Config
from celery import Celery
# from toolkit.extension import celery, dbAlchemy
dbAlchemy = SQLAlchemy()
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,backend=Config.CELERY_RESULT_BACKEND, include=["toolkit.celery.tasks"])



def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    celery = make_celery(app)
    dbAlchemy.init_app(app)
    celery.init_app(app)
    with app.app_context():
        # Import routes
        import toolkit.routes
        dbAlchemy.create_all()  # Create sql tables for our data models
        return app