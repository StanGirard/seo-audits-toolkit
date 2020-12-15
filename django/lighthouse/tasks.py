from celery.task.schedules import crontab
from celery.decorators import periodic_task
import subprocess
from django.utils import timezone
import pytz

from .models import Lighthouse, Lighthouse_Result

@periodic_task(run_every=(crontab(hour='*/1')), name="lighthouse_crawler", ignore_result=True)
def lighthouse_crawler():
    scheduled = Lighthouse.objects.filter(scheduled=True)
    for item in scheduled:
        print(item.url)
        result = run_lighthouse(item.url)
        results_db = Lighthouse_Result(url=item,result=result,timestamp=timezone.now() )
        results_db.save()
        Lighthouse.objects.filter(url=item.url).update(last_updated=timezone.now())
        print("Done")


def run_lighthouse(url):
    proc=subprocess.Popen("lighthouse --chrome-flags='--headless' "+ url + " --output json", stdout=subprocess.PIPE, shell=True)
    result = proc.stdout.read().decode("utf-8") 
    return result