from flask import current_app as app
from flask import request, render_template
from bokeh.embed import components
from datetime import datetime, timedelta
from toolkit import dbAlchemy as db
from toolkit.models import Graphs
from sqlalchemy import update
import urllib
from toolkit.controller.graphs.core import generate_graph_internal_link_interactive

from sqlalchemy import update



def update_or_insert_graph_in_db( urls, maximum, updating=False):
    """Update or inserts html in the DB

    Arguments:
        conn {Connection} -- DB connector
        urls {string} -- Root Domain
        maximum {int} -- Maximum number of urls to crawl

    Keyword Arguments:
        update {bool} -- update or insert (default: {False})

    Returns:
        HTML Render -- Renders the Graph
    """
    plot, domain = generate_graph_internal_link_interactive(urls, maximum)
    script, div = components(plot)
    conn = db.engine.connect()
    smt = update(Graphs).where(Graphs.urls == urls).values(script= script, 
            div = div, begin_date=datetime.now(), status_job="FINISHED")
    conn.execute(smt)
    return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask", time=datetime.now())

def generate_interactive_graph(urls, relaunch, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    urls_exists = Graphs.query.filter(Graphs.urls == urls).count()
    if urls_exists > 0:
        stopped = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
        print(stopped)
        if stopped.status_job == "FINISHED":
            print("STOPPED")
            query_result = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
            # ALREADY VISITED IN THE LAST 24 HOURS

            if query_result.begin_date + timedelta(hours=24) > datetime.now() and relaunch != "True":
                return render_template("bokeh.html", script=query_result.script, div=query_result.div, domain=urllib.parse.urlparse(query_result.urls).netloc, template="Flask", time=query_result.begin_date)

            # More than 24 hours or parameter redo is True
            if query_result.begin_date + timedelta(hours=24) < datetime.now() or relaunch == "True":
                conn = db.engine.connect()
                smt = update(Graphs).where(Graphs.urls == urls).values(status_job="RUNNING")
                conn.execute(smt)
                return update_or_insert_graph_in_db(urls,  maximum_urls, True)

        else:
            return "JOB IS ALREADY RUNNING. PLEASE WAIT AND REFRESH."

    else:
        new_graph = Graphs(
            urls = urls, script="", div="", status_job = "RUNNING", begin_date=datetime.now()
        )
        db.session.add(new_graph)
        db.session.commit()
        return update_or_insert_graph_in_db(urls, maximum_urls)


@app.route('/api/graph')
def interactive_graph():
    urls = request.args.get('url')  # if key doesn't exist, returns None
    relaunch = request.args.get('redo')
    maxi_urls = request.args.get('max')
    return generate_interactive_graph( urls, relaunch, maxi_urls)

@app.route('/api/graph/all')
def interactive_graph_all():
    results = Graphs.query.all()
    result_arr={"results":[]}
    for i in results:
        result_arr["results"].append({"urls": i.urls, "status_job": i.status_job})
    return result_arr