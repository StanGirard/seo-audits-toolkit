from flask import request
from flask import current_app as app
from toolkit import dbAlchemy as db
from toolkit.models import Keywords
from toolkit.controller.analysis.keywords import generate_results
import json
from datetime import datetime
from sqlalchemy import update


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


@app.route('/api/analysis/keywords')
def find_keywords_query():
    query = request.args.get('query')
    if query:
        return get_query_results(query)

    else:
        return 'Please input a valid value like this: /api/analysis/keywords?query=parse api xml response'
