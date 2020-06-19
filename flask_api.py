import urllib.parse
from datetime import datetime, timedelta
from toolkit.db import conf, analysis, seo
from toolkit.analysis import keywords
from bokeh.embed import components
from toolkit.seo.core import generate_graph_internal_link_interactive
from toolkit.seo.headers import find_all_headers_url
from toolkit.seo.rank import rank
from toolkit.analysis.keywords import generate_results
from toolkit.seo.links import find_all_links
from flask import Flask, render_template, request
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__, template_folder='toolkit/templates')


def initialize_db(conn):
    """Initialize the DB

    Arguments:
        conn {Connection} -- Connector
    """
    conf.create_table(conn, conf.sql_create_projects_table)
    conf.create_table(conn, conf.sql_create_running_table)
    conf.create_table(conn, conf.sql_create_keywords_table)
    conf.update_running_db_stopped(conn)


def update_or_insert_graph_in_db(conn, urls, maximum, update=False):
    """Update or inserts html in the DB

    Arguments:
        conn {Connection} -- DB connector
        urls {string} -- Root Domain
        maximum {int} -- Maximum number of urls to crawl

    Keyword Arguments:
        update {bool} -- update or insert (default: {False})

    Returns:
        HTML Render -- Renders the Graph
    """
    plot, domain = generate_graph_internal_link_interactive(urls, maximum)
    script, div = components(plot)
    if update:
        seo.update_url_db(conn, (datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S"), script, div, urls))
    else:
        seo.insert_url_db(conn, (urls, datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S"), script, div))
    seo.update_running_status(conn, urls)
    return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask", time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


def generate_interactive_graph(conn, urls, relaunch, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    stopped, already_exists = seo.check_status_url(conn, urls, "STOPPED")
    if stopped == True:

        # Set status to running
        seo.update_running_status(conn, urls, "RUNNING", already_exists)
        # Check if urls aready in Status Table
        already_visited = seo.select_visited(conn, urls)

        # If not first time
        if len(already_visited) == 1:

            # ALREADY VISITED IN THE LAST 24 HOURS
            if datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours=24) > datetime.now() and relaunch != "True":
                seo.update_running_status(conn, urls)
                return render_template("bokeh.html", script=already_visited[0][3], div=already_visited[0][4], domain=urllib.parse.urlparse(already_visited[0][1]).netloc, template="Flask", time=datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S'))

            # More than 24 hours or parameter redo is True
            if (datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours=24) < datetime.now() or relaunch == "True"):
                return update_or_insert_graph_in_db(conn, urls,  maximum_urls, True)

        # If first time
        else:
            return update_or_insert_graph_in_db(conn, urls, maximum_urls)
    else:
        return "JOB IS ALREADY RUNNING. PLEASE WAIT AND REFRESH."


@app.route('/api/graph')
def interactive_graph():
    conn = conf.create_connection("visited.db")
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
    conn = conf.create_connection("visited.db")
    query = request.args.get('query')
    if query:
        return analysis.get_query_results(conn, query)

    else:
        return 'Please input a valid value like this: /api/analysis/keywords?query=parse api xml response'



if __name__ == '__main__':

    conn = conf.create_connection("visited.db")

    if conn is not None:
        # create projects table and set running status to stopped
        initialize_db(conn)
    else:
        logging.warning("Error! cannot create the database connection.")

    logging.info("DB running")
    app.run(port=5000)  # run app in debug mode on port 5000
