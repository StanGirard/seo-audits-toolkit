from celery import Celery
from flask_sqlalchemy import SQLAlchemy
dbAlchemy = SQLAlchemy()

def make_celery(app_name=__name__):
    backend = "redis://localhost:6379/0"
    broker = backend.replace("0", "1")
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()