import json
import urllib
from urllib.parse import urlparse

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy
from toolkit.models import Serp
from toolkit.routes.serp.api import query_domain_serp


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
