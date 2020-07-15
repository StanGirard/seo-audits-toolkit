import json
from datetime import datetime

from flask import current_app as app
from flask import redirect, render_template, request, url_for

from toolkit import dbAlchemy as db
from toolkit.controller.seo.audit import get_all_links_website
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit.controller.seo.links import find_all_links
from toolkit.models import Audit
from toolkit.controller.seo.images import find_all_images


from toolkit.lib.api_tools import post_request_api, get_request_api


@app.route('/extract', methods=["GET"])
def extract_page():
    return render_template("extract/extract.jinja2")


@app.route('/extract/headers', methods=["GET"])
def get_all_headers():
    result = get_request_api('/api/extract/headers')
    return render_template("extract/headers/extract_headers_all.jinja2", result=result["results"])


@app.route('/extract/headers/<id>', methods=["GET"])
def get_all_headers_by_id(id):
    result = get_request_api('/api/extract/headers/' + id )
    h1 = result["h1"]["values"]
    h2 = result["h2"]["values"]
    h3 = result["h3"]["values"]
    h4 = result["h4"]["values"]
    h5 = result["h5"]["values"]
    h6 = result["h6"]["values"]
    return render_template("extract/headers/extract_headers.jinja2", id=id, h1=h1, h2=h2, h3=h3, h4=h4, h5=h5, h6=h6)


@app.route('/extract/links', methods=["GET"])
def get_all_links():
    result = get_request_api('/api/extract/links')
    return render_template("extract/links/links_all.jinja2", result=result["results"])


@app.route('/extract/links/<id>', methods=["GET"])
def get_all_links_by_id(id):
    result = get_request_api('/api/extract/links/' + id )
    return render_template("extract/links/links.jinja2", id=id, results=result["results"], links_status=result["link_status"])


@app.route('/extract/headers', methods=["POST"])
def add_headers():
    result = post_request_api('/api/extract/headers', request.form)
    return redirect(url_for('get_all_headers'))


@app.route('/extract/headers/delete', methods=["GET"])
def delete_extract_headers():
    id = request.args.get('id')
    result = post_request_api('/api/extract/headers/delete', {"id": id})
    return redirect(url_for('get_all_headers'))


@app.route('/extract/links', methods=["POST"])
def add_links():
    result = post_request_api('/api/extract/links', request.form)
    return redirect(url_for('get_all_links'))


@app.route('/extract/links/delete', methods=["GET"])
def delete_extract_links():
    id = request.args.get('id')
    result = post_request_api('/api/extract/links/delete', {"id": id})
    return redirect(url_for('get_all_links'))


@app.route('/extract/links/website', methods=["GET"])
def get_all_links_website_dashboard():
    result = get_request_api('/api/extract/links/website' )
    return render_template("extract/links_website/links_all_website.jinja2", result=result["results"])


@app.route('/extract/links/website', methods=["POST"])
def add_links_website():
    result = post_request_api('/api/extract/links/website', request.form)
    return redirect(url_for('get_all_links_website_dashboard'))


@app.route('/extract/links/website/<id>', methods=["GET"])
def get_all_links_website_by_id(id):
    results = get_request_api('/api/extract/links/website/' + id )
    result = results["results"]
    return render_template("extract/links_website/links_website.jinja2", id=id, internal=result["internal_urls"]["results"],
                           external=result["external_urls"]["results"], internal_number=result["internal_urls"]["total"],
                           external_number=result["external_urls"]["total"], page_visited=result["page_visited"],
                           crawl_time=result["time_crawl"])


@app.route('/extract/links/website/delete', methods=["GET"])
def delete_extract_links_website():
    id = request.args.get('id')
    result = post_request_api('/api/extract/links/website/delete', {"id": id})
    print(result)
    return redirect(url_for('get_all_links_website_dashboard'))


@app.route('/extract/images', methods=["GET"])
def get_all_images_dashboard():
    results = get_request_api('/api/extract/images' )
    return render_template("extract/images/images_all.jinja2", result=results["results"])


@app.route('/extract/images', methods=["POST"])
def add_images_dashboard():
    result = post_request_api('/api/extract/images', request.form)
    return redirect(url_for('get_all_images_dashboard'))


@app.route('/extract/images/<id>', methods=["GET"])
def get_all_images_by_id(id):
    results = get_request_api('/api/extract/images/' + id )
    result = results["results"]
    return render_template("extract/images/images.jinja2", id=id, images=result["images"], missing_title=result["summary"]["missing_title"],
                           missing_alt=result["summary"]["missing_alt"], duplicates=result["summary"]["duplicates"], total=result["summary"]["total"])


@app.route('/extract/images/delete', methods=["GET"])
def delete_extract_image():
    id = request.args.get('id')
    result = post_request_api('/api/extract/images/delete', {"id": id})
    return redirect(url_for('get_all_images_dashboard'))
