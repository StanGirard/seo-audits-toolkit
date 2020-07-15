import json

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy
from toolkit.models import  Keywords
from toolkit.routes.keywords.api import get_query_results
from toolkit.lib.api_tools import post_request_api, get_request_api


@app.route('/keywords', methods=["POST", "GET"])
def get_all_keywords_dashboard():
    results = None
    if request.method == "POST":
        results = post_request_api("/api/keywords", request.form)
    else:
        results = get_request_api("/api/keywords")
    return render_template("keywords/keywords_all.jinja2", result=results["results"])

@app.route('/keywords/delete', methods=["GET"])
def delete_keywords():
    id = request.args.get('id')
    result = post_request_api("/api/keywords/delete", {"id": id})
    return redirect(url_for('get_all_keywords_dashboard'))


@app.route('/keywords/<id>')
def get_all_keywords_by_id(id):
    results = get_request_api("/api/keywords/" + id)
    monogram = results["results"]["Monogram"]
    bigram = results["results"]["Bigram"]
    trigram = results["results"]["Trigram"]
    return render_template("keywords/keywords.jinja2",id=id, query=results["query"],monogram=monogram, bigram=bigram, trigram=trigram)
