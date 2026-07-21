import time

from celery import shared_task
from django.conf import settings

from rankparse.errors import RankParseError

from .models import BacklinkAudit
from .rankparse_client import fetch_backlink_audit


## Declaration of a task to be used with celery
@shared_task(bind=True, name="backlinks_job")
def backlinks_job(self, domain):
    ## Not clean, but add some delay to wait for the object to exist in the DB before starting it.
    time.sleep(0.2)
    BacklinkAudit.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    try:
        result = fetch_backlink_audit(domain, settings.RANKPARSE_API_KEY)
    except RankParseError as e:
        BacklinkAudit.objects.filter(task_id=self.request.id).update(
            result={"error": str(e)}, status_job="FAILED"
        )
        return "FAILED"

    BacklinkAudit.objects.filter(task_id=self.request.id).update(
        result=result, status_job="FINISHED"
    )
    return "FINISHED"
