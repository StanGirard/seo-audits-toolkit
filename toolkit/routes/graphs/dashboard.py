from flask import current_app as app
from flask import redirect, render_template, request, url_for
import urllib
from urllib.parse import urlparse

from toolkit import dbAlchemy
from toolkit.models import Graphs
from toolkit.routes.graphs.api import generate_interactive_graph
from toolkit.lib.api_tools import post_request_api, get_request_api


@app.route('/graphs', methods=["POST", "GET"])
def graphs_get():
    results = None
    if request.method == "POST":
        results = post_request_api("/api/graphs", request.form) 
    else:
        results = get_request_api("/api/graphs")
    return render_template("graphs/graphs_all.jinja2", result=results["results"], error=results["error"])

@app.route('/graphs/<id>', methods=["GET"])
def graphs_get_by_id(id):
    results = get_request_api("/api/graphs/" + id)
    return render_template("graphs/bokeh.jinja2", id=id,script=results["script"], div=results["div"], domain=results["domain"], template=results["template"], time=results["time"])

@app.route('/graphs/delete', methods=["GET"])
def delete_graph():
    id = request.args.get('id')
    result = post_request_api("/api/graphs/delete", {"id":id})
    return redirect(url_for('graphs_get'))
