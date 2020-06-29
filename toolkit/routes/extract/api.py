from flask import current_app as app
from flask import  render_template, request
from toolkit.controller.seo.links import find_all_links
from toolkit.controller.seo.images import find_all_images
from toolkit.controller.seo.audit import get_all_links_website
from toolkit.controller.seo.headers import find_all_headers_url
from toolkit.controller.seo.audit import get_all_links_website


@app.route('/api/extract/headers')
def find_headers():
    value = request.args.get('url')
    if value:
        return find_all_headers_url(value)
    else:
        return "Please input a valid value like this: /api/extract/headers?url=https://primates.dev"


@app.route('/api/extract/links')
def find_all_links_page():
    value = request.args.get('url')
    if value:
        return find_all_links(value)
    else:
        return 'Please input a valid url like this: /api/extract/links?url=https://primates.dev'


@app.route('/api/extract/links/website')
def find_all_links_website():
    value = request.args.get('url')
    maxi = request.args.get('max')
    if value:
        if maxi:
            return get_all_links_website(value, int(maxi))
        return get_all_links_website(value)
    else:
        return 'Please input a valid url like this: /api/extract/links/website?url=https://primates.dev&max=50'


@app.route('/api/extract/images')
def find_all_images_page():
    value = request.args.get('url')
    if value:
        return find_all_images(value)
    else:
        return 'Please input a valid url like this: /api/extract/images?url=https://primates.dev'