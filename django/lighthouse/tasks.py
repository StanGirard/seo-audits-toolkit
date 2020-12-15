from celery.task.schedules import crontab
from celery.decorators import periodic_task
import subprocess
from django.utils import timezone
import pytz
import json

from .models import Lighthouse, Lighthouse_Result

@periodic_task(run_every=(crontab(minute=0, hour='*/3')), name="lighthouse_crawler", ignore_result=True)
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