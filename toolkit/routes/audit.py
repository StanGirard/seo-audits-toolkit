from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full, audit_google_lighthouse_seo
from flask import request, redirect, url_for
from flask import current_app as app
from toolkit.models import Audit
from datetime import datetime
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit import dbAlchemy as db
import json

@app.route('/api/audit/lighthouse/full')
def audit_lighthouse_full():
    value = request.args.get('url')
    if value:
        return audit_google_lighthouse_full(value)
    else:
        return "Please input a valid value like this: /api/audit/lighthouse/full?url=https://primates.dev"


@app.route('/api/audit/lighthouse/seo')
def audit_lighthouse_seo():
    value = request.args.get('url')
    if value:
        return audit_google_lighthouse_seo(value)
    else:
        return "Please input a valid value like this: /api/audit/lighthouse/seo?url=https://primates.dev"

@app.route('/extract/headers', methods=["POST"])
def add_headers():
    url = request.form['url']
    count = Audit.query.filter(Audit.url == url and Audit.type_audit=="Headers").count()
    if url and count == 0:
        value = find_all_headers_url(url)
        new_audit = Audit(
            url = url, result=json.dumps(value), type_audit="Headers", begin_date=datetime.now()
        )
        db.session.add(new_audit)
        db.session.commit()
    return redirect(url_for('get_all_headers'))
    