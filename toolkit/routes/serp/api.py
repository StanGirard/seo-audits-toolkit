from datetime import datetime, timedelta
from urllib.parse import urlparse

from flask import current_app as app
from flask import request
from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.seo.rank import rank
from toolkit.lib.api_tools import generate_answer
from toolkit.models import Serp


def query_domain_serp( query, domain, lang, tld):
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
                result = rank(domain, query, lang=lang, tld=tld)
                update(Serp).where(Serp.query_text==query and Serp.domain==domain).values(begin_date=datetime.now(),url=result["url"], pos=result["pos"])
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
        
        result = rank(domain, query, lang=lang, tld=tld)
        new_result = Serp(query_text=result["query"],pos=result["pos"], domain=domain, url=result["url"], begin_date=datetime.now() )
        db.session.add(new_result)
        db.session.commit()
        return result


@app.route('/api/rank', methods=["POST", "GET"])
def get_post_rank():
    try:
        error = None
        if request.method == "POST":
            query = request.form["query"]
            domain = request.form["domain"]
            if not (domain.startswith('//') or domain.startswith('http://') or domain.startswith('https://')):
                domain = '//' + domain
            result = query_domain_serp( query, domain, "en", "com")
            
            if result and "limit" in result:
                error = result
        result = Serp.query.order_by(Serp.begin_date.desc()).all()
        result_list = {"results": [], "error": error}
        for i in result:
            result_list["results"].append({"id": i.id, "domain": i.domain, "pos": i.pos, "url": i.pos, "query": i.query_text, "time": i.begin_date})
        return generate_answer(data=result_list)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/rank/delete', methods=["POST"])
def post_delete_rank():
    try:
        id = request.form["id"]
        Serp.query.filter(Serp.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)
