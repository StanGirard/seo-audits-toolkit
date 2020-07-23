import math
import time
from datetime import datetime
import json

from celery.signals import task_prerun, worker_process_init
from flask import current_app as app
from sqlalchemy import update
from toolkit import celery
from toolkit import dbAlchemy as db
from toolkit.controller.graphs.core import generate_interactive_graph
from toolkit.controller.keywords.core import get_query_results
from toolkit.controller.seo.audit import get_all_links_website
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit.controller.seo.images import find_all_images
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.controller.seo.links import find_all_links
from toolkit.controller.serp.core import query_domain_serp
from toolkit.models import Audit, LighthouseScore

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

@celery.task(bind=True,name="SerpRank")
def SerpRank(self,query, domain, lang, tld):
    result = query_domain_serp(query, domain, lang, tld, str(self.request.id))
    return {'url': domain, 'status': 'Task completed!'}

@celery.task(bind=True,name="Keywords")
def KeywordsGet(self,query):
    result = get_query_results(query, str(self.request.id))
    return {'url': query, 'status': 'Task completed!'}

@celery.task(bind=True,name="Extract")
def Extractor(self,extract_type, url):
    new_audit = Audit(
        url=url, result=None, type_audit=extract_type,status_job="RUNNING",task_id=str(self.request.id), begin_date=datetime.now()
    )
    db.session.add(new_audit)
    db.session.commit()
    if extract_type == "Headers":
        value = find_all_headers_url(url)
        conn = db.engine.connect()
        smt = update(Audit).where(Audit.url == url).where(Audit.type_audit == extract_type).values(result=json.dumps(value), status_job="FINISHED")
        conn.execute(smt)
    if extract_type == "Links":
        value = find_all_links(url)
        conn = db.engine.connect()
        smt = update(Audit).where(Audit.url == url).where(Audit.type_audit == extract_type).values(result=json.dumps(value), status_job="FINISHED")
        conn.execute(smt)
    if extract_type == "Links_Website":
        value = get_all_links_website(url)
        conn = db.engine.connect()
        smt = update(Audit).where(Audit.url == url).where(Audit.type_audit == extract_type).values(result=json.dumps(value), status_job="FINISHED")
        conn.execute(smt)
    if extract_type == "Images":
        print("hello")
        value = find_all_images(url)
        conn = db.engine.connect()
        smt = update(Audit).where(Audit.url == url).where(Audit.type_audit == extract_type).values(result=json.dumps(value), status_job="FINISHED")
        conn.execute(smt)
           
    return {'url': url,"Extract": extract_type, 'status': 'Task completed!'}
