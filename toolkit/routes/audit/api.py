import json
import math
import time
from datetime import datetime

from flask import current_app as app
from flask import redirect, render_template, request, url_for
from sqlalchemy import func, update

from toolkit import celery
from toolkit import dbAlchemy as db
from toolkit.celeryapp.tasks import LighthouseAudit
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.lib.api_tools import generate_answer
from toolkit.models import Audit, LighthouseScore


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return json.dumps(response)

@app.route('/api/audit/lighthouse/score/test', methods=["GET"])
def testi_test():
    task = LighthouseAudit.delay("https://test.com")
    return {"id":task.id}

@app.route('/api/audit/lighthouse/score', methods=["POST"])
def post_audit_lighthouse_score():
    try:
        url = request.form['url']
        if url:
            task = LighthouseAudit.delay(url)
            return generate_answer(data={"id":task.id})
        else:
            return generate_answer(success=False)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/audit/lighthouse/score')
def get_all_audit_lighthouse_score():
    try:
        LS = LighthouseScore
        quer = db.session.query(LS.id,LS.url, LS.accessibility, LS.pwa, LS.seo, LS.best_practices, LS.performance,LS.status_job, func.max(LS.begin_date).label('begin_date')).group_by(LS.url)
        results = quer.all()
        result_arr={"results": [], "google_error":False}
        if app.config['GOOGLE_API_KEY'] == "None":
            result_arr["google_error"] = True
        for i in results:
            result_arr["results"].append({"id": i.id, "url": i.url, "accessibility": i.accessibility, "pwa": i.pwa, "seo": i.seo, "best_practices": i.best_practices, "performance": i.performance,"status_job": i.status_job, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)   
    
@app.route('/api/audit/lighthouse/score/<id>', methods=["GET"])
def get_audit_lighthouse_score_by_id(id):
    try:
        id_url = LighthouseScore.query.filter(LighthouseScore.id == id).first()
        results = LighthouseScore.query.filter(LighthouseScore.url == id_url.url).order_by(LighthouseScore.begin_date.desc()).all()
        result_arr={"results": []}
        seo_list = []
        accessibility_list = []
        pwa_list = []
        best_list = []
        performance_list = []
        labels = []
        for i in results:
            labels.append(i.begin_date.strftime("%m/%d/%Y, %H:%M:%S"))
            seo_list.append(i.seo)
            accessibility_list.append(i.accessibility)
            pwa_list.append(i.pwa)
            best_list.append(i.best_practices)
            performance_list.append(i.performance)
            result_arr["results"].append({"id": i.id, "url": i.url, "accessibility": i.accessibility, "pwa": i.pwa, "seo": i.seo, "best_practices": i.best_practices, "performance": i.performance, "begin_date": i.begin_date})
        result_arr["url"] = id_url.url
        result_arr["id"] = id
        result_arr["table"] = ({"labels": labels, "seo_list":seo_list, "accessibility_list": accessibility_list, "pwa_list": pwa_list, "best_list": best_list,"performance_list": performance_list })
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)   


@app.route('/api/audit/lighthouse/score/all')
def get_audit_lighthouse_score_all():
    try:
        LS = LighthouseScore
        results = LS.query.all()
        result_arr={"results": []}
        for i in results:
            result_arr["results"].append({"id": i.id, "url": i.url, "accessibility": i.accessibility, "pwa": i.pwa, "seo": i.seo, "best_practices": i.best_practices, "performance": i.performance, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)
