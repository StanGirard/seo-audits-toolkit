import json
import time
from datetime import datetime

import yake
from celery import shared_task
from extractor.src.headers import find_all_headers_url
from extractor.src.images import find_all_images
from extractor.src.links import find_all_links

from .models import Yake

## Declaration of a task to be used with celery
@shared_task(bind=True, name="keywords_job")
def keywords_job(self,text,language, ngram, top):
    time.sleep(0.2)
    Yake.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    my_yake = yake.KeywordExtractor(lan=language,
                                        n=ngram,
                                        top=top,
                                        dedupLim=0.8,
                                        windowsSize=2
                                        )

    keywords = my_yake.extract_keywords(text)
    result  = [{"id":keywords.index(x), "ngram":x[0] ,"score":x[1]} for x in keywords]
    Yake.objects.filter(task_id=self.request.id).update(result=result, status_job="FINISHED")
    return "Hello World!"
