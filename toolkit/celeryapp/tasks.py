import time
from datetime import datetime
import math

from flask import current_app as app
from toolkit import celery
from toolkit import dbAlchemy as db
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.controller.graphs.core import generate_interactive_graph
from toolkit.models import LighthouseScore
from celery.signals import worker_process_init, task_prerun
from sqlalchemy import update


# @task_prerun.connect
# def celery_prerun(*args, **kwargs):
#     #print g
#     print("Launching Celery App")

@celery.task(bind=True,name="Lighthouse")
def LighthouseAudit(self,url):
    new_score = LighthouseScore(
        url = url,status_job="RUNNING",task_id=str(self.request.id), accessibility=0,pwa=0,seo=0, best_practices=0,performance=0, begin_date=datetime.now()
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
    return {'url': url, 'status': 'Task completed!'}

@celery.task(bind=True,name="Graphs")
def GraphsGenerate(self,domain):
    result = generate_interactive_graph(domain,str(self.request.id), False, 500)
    return {'url': domain, 'status': 'Task completed!'}
