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
        score = result["score"]
        results_db = Security_Result(org=item.org,url=item,score=score,result=result, timestamp=timezone.now())
        results_db.save()
        Security.objects.filter(org=item.org,url=item.url).update(last_updated=timezone.now())
        print("Done")

@shared_task()
def security_add_new_url_crawler(url):
    time.sleep(0.2)
    Security_Object = Security.objects.filter(url=url).first()
    result = json.loads(run_security(url))
    score = result["score"]
    results_db = Security_Result(org=Security_Object.org,url=Security_Object,result=result, score=score, timestamp=timezone.now())
    results_db.save()
    Security.objects.filter(org=Security_Object.org,url=url).update(score=score,last_updated=timezone.now())
    print("Done")


def run_security(url):
    proc=subprocess.Popen("httpobs-cli -d " + url, stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().decode("utf-8") 
    result = json.loads(result)
    computed = {}
    computed["score"] = result["scan"]["score"]
    computed["grade"] = result["scan"]["grade"]
    computed["status_code"] = result["scan"]["status_code"]
    computed["tests_failed"] = result["scan"]["tests_failed"]
    computed["tests_passed"] = result["scan"]["tests_passed"]
    computed["tests_quantity"] = result["scan"]["tests_quantity"]
    
    response_headers = []
    for headers in result["scan"]["response_headers"]:
        response_headers.append({"name": headers, "value": result["scan"]["response_headers"][headers]})
    computed["response_headers"] = response_headers
    
    tests = []
    for test in result["tests"]:
        tests.append({"name": result["tests"][test]["name"],
                       "pass": result["tests"][test]["pass"],
                       "result": result["tests"][test]["result"],
                       "expectation": result["tests"][test]["expectation"],
                       "score_description": result["tests"][test]["score_description"], })
    computed["tests"] = tests
    return json.dumps(computed)
