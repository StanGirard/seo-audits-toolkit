import json
import time
from datetime import datetime

from celery import shared_task

from bert.src.bertSummarizer import summarizer_bert

from .models import Bert

## Declaration of a task to be used with celery
@shared_task(bind=True, name="bert_job")
def bert_job(self,text):
    ## Not clean, but add some delay to wait for the object to exist in the DB before starting it.
    time.sleep(0.2)
    Bert.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = summarizer_bert(text)
    Bert.objects.filter(task_id=self.request.id).update(result=result, status_job="FINISHED")
    return "Hello World!"
