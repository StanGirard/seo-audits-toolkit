import json
from datetime import datetime

from sqlalchemy import update

from toolkit import dbAlchemy as db
from toolkit.controller.analysis.keywords import generate_results
from toolkit.models import Keywords
from toolkit.lib.api_tools import generate_answer


def get_query_results(query,task, redo=False):
    check_exist = Keywords.query.filter(Keywords.query_text==query).count()
    if check_exist > 0:
        result = Keywords.query.filter(Keywords.query_text==query).first()
        if result.status_job == "RUNNING":
            return {"error": "query is already running, please wait and then refresh"}
        elif result.status_job == "FINISHED":
            return json.loads(result.results)
    else:
        new_keywords = Keywords(query_text=query, results="",
                     status_job="RUNNING",task_id=task,begin_date=datetime.now())
        db.session.add(new_keywords)
        db.session.commit()
        results = generate_results(query, 20)
        conn = db.engine.connect()
        smt = update(Keywords).where(Keywords.query_text==query).values(results=json.dumps(results), status_job="FINISHED")
        conn.execute(smt)    
        return results
    return "error"
