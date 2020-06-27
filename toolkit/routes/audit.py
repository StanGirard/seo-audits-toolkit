from toolkit.controller.seo.lighthouse import audit_google_lighthouse_full, audit_google_lighthouse_seo
from flask import request
from flask import current_app as app

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
