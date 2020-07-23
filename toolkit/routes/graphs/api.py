from flask import current_app as app
from flask import request, render_template
from bokeh.embed import components
from datetime import datetime, timedelta
from toolkit import dbAlchemy as db
from toolkit.models import Graphs
import time

import urllib
from toolkit.controller.graphs.core import generate_graph_internal_link_interactive
from toolkit.lib.api_tools import generate_answer
from toolkit.celeryapp.tasks import GraphsGenerate

from sqlalchemy import update


@app.route('/api/graphs', methods=["POST", "GET"])
def get_post_graphs():
    try:
        error = None
        if request.method == "POST":
            domain = request.form["domain"]
            if domain.startswith("https://") or domain.startswith("http://"):
                result = GraphsGenerate.delay(domain)
            else:
                result = GraphsGenerate.delay("https://" + domain)
            time.sleep(0.3)
        results = Graphs.query.all()
        result_arr= {"results":[]}
        print(result_arr)
        for i in results:
            result_arr["results"].append({"id": i.id, "urls": i.urls, "status_job": i.status_job,"task_id": i.task_id, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/graphs/<id>', methods=["GET"])
def get_graphs_by_id(id):
    try:
        results = Graphs.query.filter(Graphs.id == id).first()
        result = {"id": id, "script": results.script, "div": results.div, "domain": urllib.parse.urlparse(results.urls).netloc,
                "template":"Flask", "time":results.begin_date}
        return generate_answer(data=result)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/graphs/delete', methods=["POST"])
def post_delete_graph():
    try:
        id = request.form['id']
        Graphs.query.filter(Graphs.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/graphs/status', methods=["POST"])
def get_graphs_status_by_task():
    try:
        task_id = request.form['task']
        result = Graphs.query.filter(Graphs.task_id == task_id).first()
        if result and result.status_job == "FINISHED":
            return generate_answer(success=True)
        else:
            return generate_answer(success=False)
    except Exception as e:
        print(e)
        return generate_answer(success=False)