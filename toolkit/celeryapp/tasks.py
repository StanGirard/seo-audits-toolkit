import time
from datetime import datetime
import math

from flask import current_app as app
from toolkit import celery
from toolkit import dbAlchemy as db
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.models import LighthouseScore
from celery.signals import worker_process_init, task_prerun


@task_prerun.connect
def celery_prerun(*args, **kwargs):
    #print g
    print("HHHHHHHHHHHHHHHH")

@celery.task(bind=True,name="Lighthouse")
def LighthouseAudit(self,url):
    new_score = LighthouseScore(
        url = url,status_job="RUNNING", accessibility=0,pwa=0,seo=0, best_practices=0,performance=0, begin_date=datetime.now()
    )
    db.session.add(new_score)
    db.session.commit()
    value = audit_google_lighthouse_full(url)
    accessibility = int(math.floor(value["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
    seo = int(math.floor(value["lighthouseResult"]["categories"]["seo"]["score"] * 100))
    pwa = int(math.floor(value["lighthouseResult"]["categories"]["pwa"]["score"] * 100))
    best_practices = int(math.floor(value["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
    performance = int(math.floor(value["lighthouseResult"]["categories"]["performance"]["score"] * 100))
    conn = db.engine.connect()
    smt = update(LighthouseScore).where(LighthouseScore.url == url).values(accessibility=accessibility,pwa=pwa,seo=seo, best_practices=best_practices,performance=performance, status_job="FINISHED")
    conn.execute(smt)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
