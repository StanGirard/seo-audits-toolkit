from datetime import datetime, timedelta
from urllib.parse import urlparse
import time

from flask import current_app as app
from flask import request
from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.seo.rank import rank
from toolkit.lib.api_tools import generate_answer
from toolkit.models import Serp
from toolkit.celeryapp.tasks import SerpRank

@app.route('/api/rank', methods=["POST", "GET"])
def get_post_rank():
    try:
        error = None
        if request.method == "POST":
            query = request.form["query"]
            domain = request.form["domain"]
            if not (domain.startswith('//') or domain.startswith('http://') or domain.startswith('https://')):
                domain = '//' + domain
            result = SerpRank.delay(query, domain, "en", "com")
            time.sleep(.300)
        result = Serp.query.order_by(Serp.begin_date.desc()).all()
        result_list = {"results": [], "error": error}
        for i in result:
            result_list["results"].append({"id": i.id, "domain": i.domain, "pos": i.pos, "url": i.pos, "query": i.query_text, "time": i.begin_date, "status_job": i.status_job, "task_id": i.task_id})
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


@app.route('/api/rank/status', methods=["POST"])
def get_rank_status_by_task():
    try:
        task_id = request.form['task']
        result = Serp.query.filter(Serp.task_id == task_id).first()
        if result and result.status_job == "FINISHED":
            return generate_answer(success=True)
        else:
            return generate_answer(success=False)
    except Exception as e:
        print(e)
        return generate_answer(success=False)