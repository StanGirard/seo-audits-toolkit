import json

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy
from toolkit.models import  Keywords
from toolkit.routes.keywords.api import get_query_results


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

@app.route('/keywords/delete', methods=["GET"])
def delete_keywords():
    id = request.args.get('id')
    Keywords.query.filter(Keywords.id == id).delete()
    dbAlchemy.session.commit()
    return redirect(url_for('get_all_keywords_dashboard'))


@app.route('/keywords/<id>')
def get_all_keywords_by_id(id):
    keyw = Keywords.query.filter(Keywords.id == id).first()
    results = json.loads(keyw.results)
    monogram = results["Monogram"]
    bigram = results["Bigram"]
    trigram = results["Trigram"]
    return render_template("keywords/keywords.jinja2",id=id, query=keyw.query_text,monogram=monogram, bigram=bigram, trigram=trigram)
