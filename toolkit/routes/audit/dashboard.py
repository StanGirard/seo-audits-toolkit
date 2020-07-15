import json
import math
from datetime import datetime

from flask import current_app as app
from flask import redirect, request, url_for, render_template
from sqlalchemy import func

from toolkit import dbAlchemy as db
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.models import Audit, LighthouseScore

from toolkit.lib.api_tools import post_request_api, get_request_api


@app.route('/audit', methods=["GET"])
def audit_home():
    return render_template("audit/audit.jinja2")


@app.route('/audit/lighthouse/score', methods=["POST"])
def add_audit_lighthouse_score():
    result = post_request_api('/api/audit/lighthouse/score', request.form)
    return redirect(url_for('dashboard_audit_lighthouse_score'))

@app.route('/audit/lighthouse/score')
def dashboard_audit_lighthouse_score():
    
    result = get_request_api('/api/audit/lighthouse/score')
    return render_template("audit/lighthouse/lighthouse_all.jinja2", result=result["results"],
             error=result["google_error"])

@app.route('/audit/lighthouse/score/<id>', methods=["GET"])
def dashboard_audit_lighthouse_score_get_id(id):
    result = get_request_api('/api/audit/lighthouse/score/' + id)
    return render_template("audit/lighthouse/lighthouse.jinja2", url=result["url"], id=result["id"], result=result["results"], seo_list=result["table"]["seo_list"], accessibility_list=result["table"]["accessibility_list"],pwa_list=result["table"]["pwa_list"],
             best_list=result["table"]["best_list"], performance_list=result["table"]["performance_list"], labels=result["table"]["labels"])



@app.route('/audit/lighthouse/score/all')
def dashboard_audit_lighthouse_score_all():
    result = get_request_api('/api//audit/lighthouse/score/all')
    return result
