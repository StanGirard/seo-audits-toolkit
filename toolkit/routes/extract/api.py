import json
from datetime import datetime

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy as db
from toolkit.controller.seo.audit import get_all_links_website
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit.controller.seo.images import find_all_images
from toolkit.controller.seo.links import find_all_links
from toolkit.lib.api_tools import generate_answer
from toolkit.models import Audit


@app.route('/api/extract/headers', methods=["GET"])
def get_extract_headers_all():
    try:
        results = Audit.query.filter(Audit.type_audit == "Headers")
        result_arr = {"results": []}
        for i in results:
            result_arr["results"].append(
                {"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/headers/<id>', methods=["GET"])
def get_extract_headers_by_id(id):
    try:
        audit = Audit.query.filter(Audit.id == id).first()
        result = json.loads(audit.result)
        return generate_answer(data=result)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links', methods=["GET"])
def get_extract_links_status_all():
    try:
        results = Audit.query.filter(Audit.type_audit == "Links").all()
        result_arr = {"results": []}
        for i in results:
            result_arr["results"].append(
                {"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)
    
@app.route('/api/extract/links/<id>', methods=["GET"])
def get_extract_links_status_by_id(id):
    try:
        audit = Audit.query.filter(Audit.id == id).first()
        result = json.loads(audit.result)
        links_status = [x for x in result]
        results = {"results": result, "link_status": links_status}
        return generate_answer(data=results)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/headers', methods=["POST"])
def post_extract_headers():
    try:
        url = request.form['url']
        count = Audit.query.filter(Audit.url == url).filter(
            Audit.type_audit == "Headers").count()
        if url and count == 0:
            value = find_all_headers_url(url)
            new_audit = Audit(
                url=url, result=json.dumps(value), type_audit="Headers", begin_date=datetime.now()
            )
            db.session.add(new_audit)
            db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/headers/delete', methods=["POST"])
def post_delete_extract_headers():
    try:
        id = request.form['id']
        Audit.query.filter(Audit.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links', methods=["POST"])
def post_extract_add_links():
    try:
        url = request.form['url']
        count = Audit.query.filter(Audit.url == url).filter(
            Audit.type_audit == "Links").count()
        if url and count == 0:
            value = find_all_links(url)
            new_audit = Audit(
                url=url, result=json.dumps(value), type_audit="Links", begin_date=datetime.now()
            )
            db.session.add(new_audit)
            db.session.commit()
            return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links/delete', methods=["POST"])
def post_extract_links_delete():
    try:
        id = request.form['id']
        Audit.query.filter(Audit.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)
    
@app.route('/api/extract/links/website', methods=["GET"])
def get_extract_all_links_website():
    try:
        results = Audit.query.filter(Audit.type_audit == "Links_Website").all()
        result_arr = {"results": []}
        for i in results:
            result_arr["results"].append(
                {"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links/website', methods=["POST"])
def post_extract_add_links_website():
    try:
        url = request.form['url']
        count = Audit.query.filter(Audit.url == url).filter(
            Audit.type_audit == "Links_Website").count()
        if url and count == 0:
            value = get_all_links_website(url)
            new_audit = Audit(
                url=url, result=json.dumps(value), type_audit="Links_Website", begin_date=datetime.now()
            )
            db.session.add(new_audit)
            db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links/website/<id>', methods=["GET"])
def get_extract_links_website_by_id(id):
    try:
        audit = Audit.query.filter(Audit.id == id).first()
        result = json.loads(audit.result)
        results={"results": result}
        return generate_answer(data=results)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/links/website/delete', methods=["POST"])
def post_extract_delete_links_website():
    try:
        id = request.form('id')
        Audit.query.filter(Audit.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/images', methods=["GET"])
def get_extract_images_all():
    try:
        results = Audit.query.filter(Audit.type_audit == "Images").all()
        result_arr = {"results":[]}
        for i in results:
            result_arr["results"].append(
                {"id": i.id, "url": i.url, "result": i.result, "begin_date": i.begin_date})
        return generate_answer(data=result_arr)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/images', methods=["POST"])
def post_extract_add_images():
    try:
        url = request.form['url']
        count = Audit.query.filter(Audit.url == url).filter(
            Audit.type_audit == "Images").count()
        if url and count == 0:
            value = find_all_images(url)
            new_audit = Audit(
                url=url, result=json.dumps(value), type_audit="Images", begin_date=datetime.now()
            )
            db.session.add(new_audit)
            db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/images/<id>', methods=["GET"])
def get_extract_all_images_by_id(id):
    try:
        audit = Audit.query.filter(Audit.id == id).first()
        result = json.loads(audit.result)
        results = {"results": result}
        return generate_answer(data=results)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

@app.route('/api/extract/images/delete', methods=["POST"])
def post_delete_extract_image():
    try:
        id = request.form['id']
        Audit.query.filter(Audit.id == id).delete()
        db.session.commit()
        return generate_answer(success=True)
    except Exception as e:
        print(e)
        return generate_answer(success=False)

