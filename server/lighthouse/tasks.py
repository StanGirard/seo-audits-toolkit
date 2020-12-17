from celery import Celery
from celery.schedules import crontab
import subprocess
from django.utils import timezone
import pytz
import json

from .models import Lighthouse, Lighthouse_Result


app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(crontab(minute=0, hour='*/3'), lighthouse_crawler.s(), name='add every 10')

@app.task
def lighthouse_crawler():
    scheduled = Lighthouse.objects.filter(scheduled=True)
    for item in scheduled:
        print(item.url)
        result = json.loads(run_lighthouse(item.url))
        performance_score = result["categories"]["performance"]["score"]
        accessibility_score = result["categories"]["accessibility"]["score"]
        best_practices_score =result["categories"]["best-practices"]["score"]
        seo_score = result["categories"]["seo"]["score"]
        pwa_score = result["categories"]["pwa"]["score"]
        results_db = Lighthouse_Result(url=item,performance_score=performance_score,
            accessibility_score=accessibility_score, best_practices_score= best_practices_score,
            seo_score=seo_score, pwa_score=pwa_score, timestamp=timezone.now())
        results_db.save()
        Lighthouse.objects.filter(url=item.url).update(last_updated=timezone.now())
        print("Done")


def run_lighthouse(url):
    proc=subprocess.Popen("lighthouse --chrome-flags='--headless' "+ url + " --output json", stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().decode("utf-8") 
    return result