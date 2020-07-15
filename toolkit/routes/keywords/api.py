import json
from datetime import datetime

from flask import current_app as app
from flask import request
from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.analysis.keywords import generate_results
from toolkit.models import Keywords
from toolkit.lib.api_tools import generate_answer


def get_query_results(query, redo=False):
    check_exist = Keywords.query.filter(Keywords.query_text==query).count()
    if check_exist > 0:
        result = Keywords.query.filter(Keywords.query_text==query).first()
        if result.status_job == "RUNNING":
            return {"error": "query is already running, please wait and then refresh"}
        elif result.status_job == "FINISHED":
            return json.loads(result.results)
    else:
        new_keywords = Keywords(query_text=query, results="",
                     status_job="RUNNING",begin_date=datetime.now())
        db.session.add(new_keywords)
        db.session.commit()
        results = generate_results(query, 20)
        conn = db.engine.connect()
        smt = update(Keywords).where(Keywords.query_text==query).values(results=json.dumps(results), status_job="FINISHED")
        conn.execute(smt)
        
        #Serp.update().where(query_text==query and domain==domain).values(begin_date=datetime.now(),url=result["url"], pos=result["pos"])
        return results
    return "error"


@app.route('/api/keywords', methods=["POST", "GET"])
def get_post_keywords():
    try:
        if request.method == "POST":
            query = request.form["query"]
            get_query_results(query)
        keyw = Keywords.query.all()
        results = {"results":[]}
        for keyword in keyw:
            results["results"].append({"id":keyword.id,"query": keyword.query_text, "status_job": keyword.status_job})
        return generate_answer(data=results)
    except Exception as e:
        print(e)
        return generate_answer(success=False)


@app.route('/api/keywords/delete', methods=["POST"])
def post_delete_keywords():
    try:
        id = request.form['id']
        Keywords.query.filter(Keywords.id == id).delete()
        db.session.commit()
        generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/keywords/<id>')
def get_keywords_by_id(id):
    try:
        keyw = Keywords.query.filter(Keywords.id == id).first()
        results = json.loads(keyw.results)
        results_arr = {"results": results, "query": keyw.query_text}
        return generate_answer(data=results_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)


