import json
import subprocess

import pytz
import time
from celery import shared_task
from celery.schedules import crontab
from django.utils import timezone

from .models import Security, Security_Result


@shared_task
def security_crawler():
    scheduled = Security.objects.filter(scheduled=True)
    for item in scheduled:
        print(item)
        print(item.url)
        result = json.loads(run_security(item.url))
        score = result["scan"]["score"]
        results_db = Security_Result(org=item.org,url=item,score=score,result=result, timestamp=timezone.now())
        results_db.save()
        Security.objects.filter(org=item.org,url=item.url).update(last_updated=timezone.now())
        print("Done")

@shared_task()
def security_add_new_url_crawler(url):
    time.sleep(0.2)
    Security_Object = Security.objects.filter(url=url).first()
    result = json.loads(run_security(url))
    score = result["scan"]["score"]
    results_db = Security_Result(org=Security_Object.org,url=Security_Object,result=result, score=score, timestamp=timezone.now())
    results_db.save()
    Security.objects.filter(org=Security_Object.org,url=url).update(last_updated=timezone.now(), score=score)
    print("Done")


def run_security(url):
    proc=subprocess.Popen("httpobs-cli -d " + url, stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().decode("utf-8") 
    return result
