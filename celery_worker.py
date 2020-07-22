from toolkit import celery
from toolkit.factory import create_app
from toolkit.celery_utils import init_celery
app = create_app()
init_celery(celery, app)