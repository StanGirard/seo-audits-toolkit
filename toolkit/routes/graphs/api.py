from flask import current_app as app
from flask import request, render_template
from bokeh.embed import components
from datetime import datetime, timedelta
from toolkit import dbAlchemy as db
from toolkit.models import Graphs

import urllib
from urllib.parse import urlparse
from toolkit.controller.graphs.core import generate_graph_internal_link_interactive
from toolkit.lib.api_tools import generate_answer

from sqlalchemy import update



def update_or_insert_graph_in_db( urls, maximum, updating=False):
    plot, domain = generate_graph_internal_link_interactive(urls, maximum)
    script, div = components(plot)
    conn = db.engine.connect()
    smt = update(Graphs).where(Graphs.urls == urls).values(script= script, 
            div = div, begin_date=datetime.now(), status_job="FINISHED")
    conn.execute(smt)
    return render_template("graphs/bokeh.jinja2", script=script, div=div, domain=domain, template="Flask", time=datetime.now())

def generate_interactive_graph(urls, relaunch, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    urls_exists = Graphs.query.filter(Graphs.urls == urls).count()
    if urls_exists > 0:
        stopped = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
        if stopped.status_job == "FINISHED":
            query_result = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
            # ALREADY VISITED IN THE LAST 24 HOURS

            if query_result.begin_date + timedelta(hours=24) > datetime.now() and relaunch != "True":
                return render_template("graphs/bokeh.jinja2", script=query_result.script, div=query_result.div, domain=urllib.parse.urlparse(query_result.urls).netloc, template="Flask", time=query_result.begin_date)

            # More than 24 hours or parameter redo is True
            if query_result.begin_date + timedelta(hours=24) < datetime.now() or relaunch == "True":
                conn = db.engine.connect()
                smt = update(Graphs).where(Graphs.urls == urls).values(status_job="RUNNING")
                conn.execute(smt)
                return update_or_insert_graph_in_db(urls,  maximum_urls, True)

        else:
            return {"error": "You graph is being generated. Please wait"}

    else:
        new_graph = Graphs(
            urls = urls, script="", div="", status_job = "RUNNING", begin_date=datetime.now()
        )
        db.session.add(new_graph)
        db.session.commit()
        return update_or_insert_graph_in_db(urls, maximum_urls)


@app.route('/api/graphs', methods=["POST", "GET"])
def get_post_graphs():
    try:
        error = None
        if request.method == "POST":
            domain = request.form["domain"]
            if urlparse(domain).scheme not in ["https", "http"]:
                error = "Please input an url with https or http at the beginning"
            else:
                result = generate_interactive_graph(domain, False, 500)
                if "error" in result:
                    error = result
        results = Graphs.query.all()
        result_arr= {"results":[], "error": error}
        for i in results:
            result_arr["results"].append({"id": i.id, "urls": i.urls, "status_job": i.status_job, "begin_date": i.begin_date})
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
