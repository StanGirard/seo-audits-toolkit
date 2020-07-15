import json
import math
from datetime import datetime

from flask import current_app as app
from flask import redirect, request, url_for, render_template
from sqlalchemy import func

from toolkit import dbAlchemy as db
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.models import Audit, LighthouseScore

from toolkit.lib.api_tools import generate_answer

@app.route('/api/audit/lighthouse/score', methods=["POST"])
def post_audit_lighthouse_score():
    try:
        url = request.form['url']
        if url:
            value = audit_google_lighthouse_full(url)
            accessibility = int(math.floor(value["lighthouseResult"]["categories"]["accessibility"]["score"] * 100))
            seo = int(math.floor(value["lighthouseResult"]["categories"]["seo"]["score"] * 100))
            pwa = int(math.floor(value["lighthouseResult"]["categories"]["pwa"]["score"] * 100))
            best_practices = int(math.floor(value["lighthouseResult"]["categories"]["best-practices"]["score"] * 100))
            performance = int(math.floor(value["lighthouseResult"]["categories"]["performance"]["score"] * 100))
            new_score = LighthouseScore(
                url = url, accessibility=accessibility,pwa=pwa,seo=seo, best_practices=best_practices,performance=performance, begin_date=datetime.now()
            )
            db.session.add(new_score)
            db.session.commit()
            print("Good")
            return generate_answer()
        else:
            return generate_answer(success=False)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/audit/lighthouse/score')
def get_all_audit_lighthouse_score():
    try:
        LS = LighthouseScore
        quer = db.session.query(LS.id,LS.url, LS.accessibility, LS.pwa, LS.seo, LS.best_practices, LS.performance, func.max(LS.begin_date).label('begin_date')).group_by(LS.url)
        results = quer.all()
        result_arr={"results": [], "google_error":False}
        if app.config['GOOGLE_API_KEY'] == "None":
            result_arr["google_error"] = True
        for i in results:
            result_arr["results"].append({"id": i.id, "url": i.url, "accessibility": i.accessibility, "pwa": i.pwa, "seo": i.seo, "best_practices": i.best_practices, "performance": i.performance, "begin_date": i.begin_date})
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