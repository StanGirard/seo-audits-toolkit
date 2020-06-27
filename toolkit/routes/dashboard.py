from flask import current_app as app
from flask import  render_template, request
from toolkit import dbAlchemy
from toolkit.models import Serp, Graphs
from toolkit.routes.serp import query_domain_serp
from toolkit.routes.graphs import generate_interactive_graph
import urllib

@app.route('/')
def home():
    return render_template("index.jinja2")

@app.route('/rank', methods=["POST", "GET"])
def rank_get():
    error = None
    if request.method == "POST":
        query = request.form["query"]
        domain = request.form["domain"]
        result = query_domain_serp( query, domain, "en", "com")
        if "limit" in result:
            error = result
    result = Serp.query.order_by(Serp.begin_date.desc()).all()
    result_list = []
    for i in result:
        result_list.append({"pos": i.pos, "url": i.pos, "query": i.query_text, "time": i.begin_date})
    return render_template("rank.jinja2", result=result_list, error=error)

@app.route('/graphs', methods=["POST", "GET"])
def graphs_get():
    error = None
    if request.method == "POST":
        domain = request.form["domain"]
        result = generate_interactive_graph(domain, False, 500)
        if "error" in result:
            error = result
    results = Graphs.query.all()
    result_arr=[]
    for i in results:
        result_arr.append({"id": i.id, "urls": i.urls, "status_job": i.status_job, "begin_date": i.begin_date})
    return render_template("graphs_all.jinja2", result=result_arr)

@app.route('/graphs/<id>', methods=["GET"])
def graphs_get_by_id(id):
    results = Graphs.query.filter(Graphs.id == id).first()
    return render_template("bokeh.jinja2", script=results.script, div=results.div, domain=urllib.parse.urlparse(results.urls).netloc, template="Flask", time=results.begin_date)