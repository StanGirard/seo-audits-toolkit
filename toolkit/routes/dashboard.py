from flask import current_app as app
from flask import  render_template, request, redirect, url_for
from toolkit import dbAlchemy
from toolkit.models import Serp, Graphs, Keywords, Audit
from toolkit.routes.keywords import get_query_results
from toolkit.routes.serp import query_domain_serp
from toolkit.routes.graphs import generate_interactive_graph
import urllib
from urllib.parse import urlparse
import json

@app.route('/')
def home():
    rank = Serp.query.count()
    graphs = Graphs.query.count()
    keywords = Keywords.query.count()
    return render_template("index.jinja2", rank=rank, graphs=graphs, keywords=keywords)

@app.route('/rank', methods=["POST", "GET"])
def rank_get():
    error = None
    if request.method == "POST":
        query = request.form["query"]
        domain = request.form["domain"]
        if not (domain.startswith('//') or domain.startswith('http://') or domain.startswith('https://')):
            domain = '//' + domain
        result = query_domain_serp( query, urlparse(domain).netloc, "en", "com")
        
        if result and "limit" in result:
            error = result
    result = Serp.query.order_by(Serp.begin_date.desc()).all()
    result_list = []
    for i in result:
        result_list.append({"id": i.id, "domain": i.domain, "pos": i.pos, "url": i.pos, "query": i.query_text, "time": i.begin_date})
    return render_template("serp/rank.jinja2", result=result_list, error=error)

@app.route('/rank/delete', methods=["GET"])
def delete_rank():
    id = request.args.get('id')
    Serp.query.filter(Serp.id == id).delete()
    dbAlchemy.session.commit()
    return redirect(url_for('rank_get'))

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
    return render_template("graphs/graphs_all.jinja2", result=result_arr)

@app.route('/graphs/<id>', methods=["GET"])
def graphs_get_by_id(id):
    results = Graphs.query.filter(Graphs.id == id).first()
    return render_template("graphs/bokeh.jinja2", script=results.script, div=results.div, domain=urllib.parse.urlparse(results.urls).netloc, template="Flask", time=results.begin_date)

@app.route('/graphs/delete', methods=["GET"])
def delete_graph():
    id = request.args.get('id')
    Graphs.query.filter(Graphs.id == id).delete()
    dbAlchemy.session.commit()
    return redirect(url_for('graphs_get'))

@app.route('/keywords', methods=["POST", "GET"])
def get_all_keywords_dashboard():
    if request.method == "POST":
        query = request.form["query"]
        get_query_results(query)
    keyw = Keywords.query.all()
    results = []
    for keyword in keyw:
        results.append({"id":keyword.id,"query": keyword.query_text, "status_job": keyword.status_job})
    return render_template("keywords/keywords_all.jinja2", result=results)

@app.route('/keywords/<id>')
def get_all_keywords_by_id(id):
    keyw = Keywords.query.filter(Keywords.id == id).first()
    results = json.loads(keyw.results)
    monogram = results["Monogram"]
    bigram = results["Bigram"]
    trigram = results["Trigram"]
    return render_template("keywords/keywords.jinja2", query=keyw.query_text,monogram=monogram, bigram=bigram, trigram=trigram)

@app.route('/extract', methods=["GET"])
def extract_page():
    return render_template("extract/extract.jinja2")

@app.route('/extract/headers', methods=["GET"])
def get_all_headers():
    results = Audit.query.filter(Audit.type_audit == "Headers")
    result_arr=[]
    for i in results:
        result_arr.append({"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
    return render_template("extract/extract_headers_all.jinja2", result=result_arr)

@app.route('/extract/headers/<id>', methods=["GET"])
def get_all_headers_by_id(id):
    audit = Audit.query.filter(Audit.id == id).first()
    print(audit.result)
    result = json.loads(audit.result)
    
    h1 = result["h1"]["values"]
    h2 = result["h2"]["values"]
    h3 = result["h3"]["values"]
    h4 = result["h4"]["values"]
    h5 = result["h5"]["values"]
    h6 = result["h6"]["values"]
    print(h1)
    return render_template("extract/extract_headers.jinja2",h1=h1,h2=h2,h3=h3, h4=h4, h5=h5, h6=h6 )

