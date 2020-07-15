import json
import urllib
from urllib.parse import urlparse

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy
from toolkit.models import Serp
from toolkit.routes.serp.api import query_domain_serp
from toolkit.lib.api_tools import post_request_api, get_request_api


@app.route('/rank', methods=["POST", "GET"])
def rank_get():
    results = None
    if request.method == "POST":
        results = post_request_api("/api/rank", request.form)
    else:
        results = get_request_api("/api/rank")
    return render_template("serp/rank.jinja2", result=results["results"], error=results["error"])

@app.route('/rank/delete', methods=["GET"])
def delete_rank():
    id = request.args.get('id')
    result = post_request_api("/api/rank/delete", {"id": id})
    dbAlchemy.session.commit()
    return redirect(url_for('rank_get'))
