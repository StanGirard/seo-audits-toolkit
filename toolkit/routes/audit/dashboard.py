import json
from datetime import datetime

from flask import current_app as app
from flask import redirect, request, url_for

from toolkit import dbAlchemy as db
from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full
from toolkit.models import Audit


@app.route('/audit/lighthouse/full')
def dashboard_audit_lighthouse_full():
    results = Audit.query.filter(Audit.type_audit == "Lighthouse_Full").all()
    result_arr={"results": []}
    for i in results:
        result_arr["results"].append({"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
    return result_arr

@app.route('/audit/lighthouse/full', methods=["POST"])
def add_audit_lighthouse_full():
    url = request.form['url']
    count = Audit.query.filter(Audit.url == url).filter(Audit.type_audit=="Lighthouse_Full").count()
    if url and count == 0:
        value = audit_google_lighthouse_full(url)
        print(value)
        new_audit = Audit(
            url = url, result=json.dumps(value), type_audit="Lighthouse_Full", begin_date=datetime.now()
        )
        db.session.add(new_audit)
        db.session.commit()
    return redirect(url_for('dashboard_audit_lighthouse_full'))
