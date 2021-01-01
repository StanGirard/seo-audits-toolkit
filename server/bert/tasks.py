import json
import time
from datetime import datetime

from celery import shared_task

from bert.src.bertSummarizer import summarizer_bert

from .models import Bert


@shared_task(bind=True, name="bert_job")
def bert_job(self,text):
    time.sleep(0.2)
    Bert.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = summarizer_bert(text)
    Bert.objects.filter(task_id=self.request.id).update(result=result, status_job="FINISHED")
    return "Hello World!"
