from flask import current_app as app
from flask import redirect, render_template, request, url_for
import urllib
from urllib.parse import urlparse

from toolkit import dbAlchemy
from toolkit.models import Graphs
from toolkit.routes.graphs.api import generate_interactive_graph


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
    return render_template("graphs/bokeh.jinja2", id=id,script=results.script, div=results.div, domain=urllib.parse.urlparse(results.urls).netloc, template="Flask", time=results.begin_date)

@app.route('/graphs/delete', methods=["GET"])
def delete_graph():
    id = request.args.get('id')
    Graphs.query.filter(Graphs.id == id).delete()
    dbAlchemy.session.commit()
    return redirect(url_for('graphs_get'))
