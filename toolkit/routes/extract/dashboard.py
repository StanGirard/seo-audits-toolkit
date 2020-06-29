import json
import urllib
from datetime import datetime
from urllib.parse import urlparse

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy as db
from toolkit.controller.seo.audit import get_all_links_website
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit.controller.seo.links import find_all_links
from toolkit.models import Audit, Graphs, Keywords, Serp
from toolkit.routes.graphs import generate_interactive_graph
from toolkit.routes.keywords import get_query_results
from toolkit.routes.serp import query_domain_serp


@app.route('/extract', methods=["GET"])
def extract_page():
    return render_template("extract/extract.jinja2")

@app.route('/extract/headers', methods=["GET"])
def get_all_headers():
    results = Audit.query.filter(Audit.type_audit == "Headers")
    result_arr=[]
    for i in results:
        result_arr.append({"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
    return render_template("extract/extract_headers_all.jinja2",result=result_arr)

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
    return render_template("extract/extract_headers.jinja2",id=id,h1=h1,h2=h2,h3=h3, h4=h4, h5=h5, h6=h6 )

@app.route('/extract/links', methods=["GET"])
def get_all_links():
    results = Audit.query.filter(Audit.type_audit == "Links").all()
    result_arr=[]
    for i in results:
        result_arr.append({"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
    return render_template("extract/links_all.jinja2", result=result_arr)

@app.route('/extract/links/<id>', methods=["GET"])
def get_all_links_by_id(id):
    audit = Audit.query.filter(Audit.id == id).first()
    print(audit.result)
    result = json.loads(audit.result)
    return render_template("extract/links.jinja2",id=id,results=result["200"] )

@app.route('/extract/headers', methods=["POST"])
def add_headers():
    url = request.form['url']
    count = Audit.query.filter(Audit.url == url).filter(Audit.type_audit=="Headers").count()
    if url and count == 0:
        value = find_all_headers_url(url)
        new_audit = Audit(
            url = url, result=json.dumps(value), type_audit="Headers", begin_date=datetime.now()
        )
        db.session.add(new_audit)
        db.session.commit()
    return redirect(url_for('get_all_headers'))

@app.route('/extract/links', methods=["POST"])
def add_links():
    url = request.form['url']
    count = Audit.query.filter(Audit.url == url).filter(Audit.type_audit=="Links").count()
    print(url)
    print(count)
    if url and count == 0:
        value = find_all_links(url)
        new_audit = Audit(
            url = url, result=json.dumps(value), type_audit="Links", begin_date=datetime.now()
        )
        db.session.add(new_audit)
        db.session.commit()
        print("added")
    return redirect(url_for('get_all_links'))


@app.route('/extract/links/website', methods=["GET"])
def get_all_links_website_dashboard():
    results = Audit.query.filter(Audit.type_audit == "Links_Website").all()
    result_arr=[]
    for i in results:
        result_arr.append({"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
    return render_template("extract/links_all_website.jinja2", result=result_arr)

@app.route('/extract/links/website', methods=["POST"])
def add_links_website():
    url = request.form['url']
    count = Audit.query.filter(Audit.url == url).filter(Audit.type_audit=="Links_Website").count()
    print(url)
    print(count)
    if url and count == 0:
        value = get_all_links_website(url)
        new_audit = Audit(
            url = url, result=json.dumps(value), type_audit="Links_Website", begin_date=datetime.now()
        )
        db.session.add(new_audit)
        db.session.commit()
        print("added")
    return redirect(url_for('get_all_links_website_dashboard'))

@app.route('/extract/links/website/<id>', methods=["GET"])
def get_all_links_website_by_id(id):
    audit = Audit.query.filter(Audit.id == id).first()
    print(audit.result)
    result = json.loads(audit.result)
    return render_template("extract/links_website.jinja2",id=id,internal=result["internal_urls"]["results"],
                 external=result["external_urls"]["results"],internal_number=result["internal_urls"]["total"],
                 external_number=result["external_urls"]["total"], page_visited=result["page_visited"],
                 crawl_time=result["time_crawl"])