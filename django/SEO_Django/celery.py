import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Django.settings')

app = Celery('SEO_Django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()