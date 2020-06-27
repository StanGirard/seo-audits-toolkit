from flask import current_app as app
from flask import  render_template, request
from toolkit import dbAlchemy
from toolkit.models import Serp
from toolkit.routes.serp import query_domain_serp

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
    print("hello")
    result = Serp.query.order_by(Serp.begin_date.desc()).all()
    print("hello1")
    result_list = []
    print(result)
    for i in result:
        result_list.append({"pos": i.pos, "url": i.pos, "query": i.query_text, "time": i.begin_date})
    return render_template("rank.jinja2", result=result_list, error=error)