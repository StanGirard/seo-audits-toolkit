from toolkit.db import conf, analysis
from toolkit.db.conf import initialize_db, create_connection
from toolkit.graphs.core import generate_interactive_graph
from toolkit.seo.headers import find_all_headers_url
from toolkit.seo.rank import rank
from toolkit.seo.links import find_all_links
from toolkit.seo.images import find_all_images
from toolkit.seo.audit import get_all_links_website
from toolkit.seo.lighthouse import audit_google_lighthouse_full
from flask import Flask, request
import logging

#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
#                     level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__, template_folder='toolkit/templates')


@app.route('/api/audit/lighthouse/full')
def audit_lighthouse():
    value = request.args.get('url')
    if value:
        return audit_google_lighthouse_full(value)
    else:
        return "Please input a valid value like this: /api/audit/lighthouse/full?url=https://primates.dev"

@app.route('/api/graph')
def interactive_graph():
    conn = create_connection("visited.db")
    with conn:
        urls = request.args.get('url')  # if key doesn't exist, returns None
        relaunch = request.args.get('redo')
        maxi_urls = request.args.get('max')
        return generate_interactive_graph(conn, urls, relaunch, maxi_urls)
    conn.close()


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


@app.route('/api/serp')
def find_rank_query():
    query = request.args.get('query')
    domain = request.args.get('domain')
    tld = request.args.get('tld')
    lang = request.args.get('lang')
    print(lang)
    if query and domain:
        return rank(domain, query, lang=lang, tld=tld)
    else:
        return 'Please input a valid value like this: /api/serp?domain=primates.dev&query=parse api xml response&tld=com&lang=en'


@app.route('/api/analysis/keywords')
def find_keywords_query():
    conn = create_connection("visited.db")
    query = request.args.get('query')
    if query:
        return analysis.get_query_results(conn, query)

    else:
        return 'Please input a valid value like this: /api/analysis/keywords?query=parse api xml response'


if __name__ == '__main__':

    conn = create_connection("visited.db")

    if conn is not None:
        # create projects table and set running status to stopped
        initialize_db(conn)
    else:
        logging.warning("Error! cannot create the database connection.")

    logging.info("DB running")
    app.run(host='0.0.0.0')  # run app in debug mode on port 5000
