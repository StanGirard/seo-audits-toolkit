from celery import shared_task,task
from .models import Extractor
from datetime import datetime
from extractor.src.headers import find_all_headers_url
from extractor.src.images import find_all_images
from extractor.src.links import find_all_links
import time

@task(bind=True, name="extractor_job")
def extractor_job(self,url, task_type):
    print(task_type)
    Extractor.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = None
    if (task_type == "HEADERS"):
        result = find_all_headers_url(url)
    elif (task_type == "IMAGES"):
        result = find_all_images(url)
    elif (task_type == "LINKS"):
        result = find_all_links(url)
    Extractor.objects.filter(task_id=self.request.id).update(result=str(result), status_job="FINISHED")
    return "Hello World!"