from flask import current_app as app
from flask import  render_template, request
from toolkit import dbAlchemy
from toolkit.models import Serp, Graphs, Keywords
from toolkit.routes.keywords import get_query_results
from toolkit.routes.serp import query_domain_serp
from toolkit.routes.graphs import generate_interactive_graph
import urllib
import json

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

@app.route('/keywords', methods=["POST", "GET"])
def get_all_keywords_dashboard():
    if request.method == "POST":
        query = request.form["query"]
        get_query_results(query)
    keyw = Keywords.query.all()
    results = []
    for keyword in keyw:
        results.append({"id":keyword.id,"query": keyword.query_text, "status_job": keyword.status_job})
    return render_template("keywords_all.jinja2", result=results)

@app.route('/keywords/<id>')
def get_all_keywords_by_id(id):
    keyw = Keywords.query.filter(Keywords.id == id).first()
    results = json.loads(keyw.results)
    monogram = results["Monogram"]
    bigram = results["Bigram"]
    trigram = results["Trigram"]
    return render_template("keywords.jinja2", query=keyw.query_text,monogram=monogram, bigram=bigram, trigram=trigram)