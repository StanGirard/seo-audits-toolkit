import json
from datetime import datetime
import time

from flask import current_app as app
from flask import request
from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.analysis.keywords import generate_results
from toolkit.models import Keywords
from toolkit.lib.api_tools import generate_answer
from toolkit.celeryapp.tasks import KeywordsGet


@app.route('/api/keywords', methods=["POST", "GET"])
def get_post_keywords():
    try:
        if request.method == "POST":
            query = request.form["query"]
            result = KeywordsGet.delay(query)
            time.sleep(.300)

        keyw = Keywords.query.all()
        results = {"results":[]}
        for keyword in keyw:
            results["results"].append({"id":keyword.id,"query": keyword.query_text, "status_job": keyword.status_job,"task_id": keyword.task_id})
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

@app.route('/api/keywords/status', methods=["POST"])
def get_keywords_status_by_task():
    try:
        task_id = request.form['task']
        result = Keywords.query.filter(Keywords.task_id == task_id).first()
        if result and result.status_job == "FINISHED":
            return generate_answer(success=True)
        else:
            return generate_answer(success=False)
    except Exception as e:
        print(e)
        return generate_answer(success=False)


