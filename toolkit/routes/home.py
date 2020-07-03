from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy
from toolkit.models import Audit, Graphs, Keywords, Serp


@app.route('/')
def home():
    rank = Serp.query.count()
    graphs = Graphs.query.count()
    keywords = Keywords.query.count()
    audit = Audit.query.count()
    return render_template("index.jinja2", rank=rank, graphs=graphs, keywords=keywords,audit=audit)
