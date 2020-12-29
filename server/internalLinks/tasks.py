import json
import time
from datetime import datetime

from celery import shared_task

from internalLinks.src.internal_links import generate_graph_internal_link_interactive

from .models import InternalLinks


@shared_task(bind=True, name="keywords_job")
def internal_links_job(self,url, maximum):
    time.sleep(0.2)
    InternalLinks.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = generate_graph_internal_link_interactive(url, maximum)
    InternalLinks.objects.filter(task_id=self.request.id).update(result=result, status_job="FINISHED")
    return "Hello World!"
