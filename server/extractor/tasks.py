import json
import time
from datetime import datetime

from celery import shared_task

from extractor.src.headers import find_all_headers_url
from extractor.src.images import find_all_images
from extractor.src.links import find_all_links
from extractor.src.sitemap import extract_urls

from .models import Extractor, Sitemap


@shared_task(bind=True, name="extractor_job")
def extractor_job(self,url, task_type):
    print(task_type)
    time.sleep(0.2)
    Extractor.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = None
    if (task_type == "HEADERS"):
        result = find_all_headers_url(url)
    elif (task_type == "IMAGES"):
        result = find_all_images(url)
    elif (task_type == "LINKS"):
        result = find_all_links(url)
    Extractor.objects.filter(task_id=self.request.id).update(result=json.dumps(result).replace("'", "\\'"), status_job="FINISHED")
    return "Hello World!"

@shared_task(bind=True, name="sitemap_job")
def sitemap_job(self,url, org_id):
    time.sleep(0.2)
    Sitemap.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = extract_urls(url, org_id)
    Sitemap.objects.filter(task_id=self.request.id).update(result=result, status_job="FINISHED")
    return "Hello World!"

