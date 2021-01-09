import json
import subprocess

import pytz
import time
from celery import shared_task
from celery.schedules import crontab
from django.utils import timezone

from .models import Lighthouse, Lighthouse_Result


@shared_task
def lighthouse_crawler():
    scheduled = Lighthouse.objects.filter(scheduled=True)
    for item in scheduled:
        print(item)
        print(item.url)
        result = json.loads(run_lighthouse(item.url))
        performance_score = result["categories"]["performance"]["score"]
        accessibility_score = result["categories"]["accessibility"]["score"]
        best_practices_score =result["categories"]["best-practices"]["score"]
        seo_score = result["categories"]["seo"]["score"]
        pwa_score = result["categories"]["pwa"]["score"]
        results_db = Lighthouse_Result(org=item.org,url=item,performance_score=performance_score,
            accessibility_score=accessibility_score, best_practices_score= best_practices_score,
            seo_score=seo_score, pwa_score=pwa_score, timestamp=timezone.now())
        results_db.save()
        Lighthouse.objects.filter(org=item.org,url=item.url).update(last_updated=timezone.now())
        print("Done")

@shared_task()
def lighthouse_add_new_url_crawler(url):
    time.sleep(0.2)
    Lighthouse_Object = Lighthouse.objects.filter(url=url).first()
    result = json.loads(run_lighthouse(url))
    performance_score = result["categories"]["performance"]["score"]
    accessibility_score = result["categories"]["accessibility"]["score"]
    best_practices_score =result["categories"]["best-practices"]["score"]
    seo_score = result["categories"]["seo"]["score"]
    pwa_score = result["categories"]["pwa"]["score"]
    results_db = Lighthouse_Result(org=Lighthouse_Object.org,url=Lighthouse_Object,performance_score=performance_score,
        accessibility_score=accessibility_score, best_practices_score= best_practices_score,
        seo_score=seo_score, pwa_score=pwa_score, timestamp=timezone.now())
    results_db.save()
    Lighthouse.objects.filter(org=Lighthouse_Object.org,url=url).update(last_updated=timezone.now())
    print("Done")


def run_lighthouse(url):
    proc=subprocess.Popen("lighthouse --chrome-flags='--headless --no-sandbox --disable-dev-shm-usage ' "+ url + " --output json", stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().decode("utf-8") 
    return result
