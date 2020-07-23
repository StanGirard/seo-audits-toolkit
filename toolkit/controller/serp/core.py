from datetime import datetime, timedelta
from urllib.parse import urlparse

from flask import current_app as app
from flask import request
from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.seo.rank import rank
from toolkit.lib.api_tools import generate_answer
from toolkit.models import Serp


def query_domain_serp( query, domain, lang, tld,task):
    domain = urlparse(domain).netloc + urlparse(domain).path
    if query and domain:
        existing_serp_count= Serp.query.filter(
            Serp.query_text == query and Serp.domain == domain
        ).count()
        
        if existing_serp_count > 0:
            existing_serp = Serp.query.filter(
            Serp.query_text == query and Serp.domain == domain
        ).all()
            if existing_serp[0].begin_date + timedelta(hours=24) < datetime.now():
                conn = db.engine.connect()
                smt = update(Serp).where(Serp.query_text==query and Serp.domain==domain).values(begin_date=datetime.now(),url=result["url"], status_job="RUNNING", pos=result["pos"], task_id=task)
                conn.execute(smt)
                result = rank(domain, query, lang=lang, tld=tld)
                smt = update(Serp).where(Serp.query_text==query and Serp.domain==domain).values(begin_date=datetime.now(),url=result["url"], status_job="FINISHED", pos=result["pos"])
                conn.execute(smt)
                return result
            else:
                return {"pos": existing_serp[0].pos, "url": existing_serp[0].url, "query": existing_serp[0].query_text}
        
        all_results_count = Serp.query.order_by(Serp.begin_date.desc()).count()
        if all_results_count >= 5:
            all_results = Serp.query.order_by(Serp.begin_date.desc()).all()
            if all_results[4].begin_date+ timedelta(hours=1) > datetime.now():
                waiting = datetime.now() - all_results[4].begin_date
                secs = 3600 - int(waiting.total_seconds())
                minutes = int(secs / 60) % 60
                return {"limit": "Imposing a limit of 5 query per hour to avoid Google Ban", "waiting_time": str(minutes) + "m " + str(int(secs % 60)) + "s" }   
        
        new_result = Serp(query_text=query,pos=-20, domain=domain, url=None, begin_date=datetime.now(), task_id=task, status_job="RUNNING" )
        db.session.add(new_result)
        db.session.commit()
        result = rank(domain, query, lang=lang, tld=tld)
        conn = db.engine.connect()     
        smt = update(Serp).where(Serp.query_text==query and Serp.domain==domain).values(begin_date=datetime.now(),url=result["url"], status_job="FINISHED", pos=result["pos"])
        conn.execute(smt)
        return result