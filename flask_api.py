import urllib.parse
from datetime import datetime, timedelta
from seo import db
from bokeh.embed import components
from seo.core import generate_graph_internal_link_interactive, find_all_headers_url
from seo.rank import rank
from analysis.keywords import generate_results
from flask import Flask, render_template, request
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)



def initialize_db(conn):
    """Initialize the DB

    Arguments:
        conn {Connection} -- Connector
    """
    db.create_table(conn, db.sql_create_projects_table)
    db.create_table(conn, db.sql_create_running_table)
    db.update_running_db_stopped(conn)


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
        db.update_url_db(conn, (datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S"), script, div, urls))
    else:
        db.insert_url_db(conn, (urls, datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S"), script, div))
    update_running_status(conn, urls)
    return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask", time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


def update_running_status(conn, urls, status="STOPPED", already_exists=True):
    """Updates the status of the crawl

    Arguments:
        conn {Connection} -- DB Connection
        urls {string} -- Root url for crawling

    Keyword Arguments:
        status {str} -- Status string (default: {"STOPPED"})
        already_exists {bool} -- Is the url already in the database (default: {True})
    """
    if status == "RUNNING":
        if already_exists:
            db.update_running_db(conn, ("RUNNING", urls))
        else:
            db.insert_running_db(conn, (urls, "RUNNING"))
    else:
        db.update_running_db(conn, ("STOPPED", urls))


def generate_interactive_graph(conn, urls, relaunch, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    stopped, already_exists = db.check_status_url(conn, urls, "STOPPED")
    if stopped == True:

        # Set status to running
        update_running_status(conn, urls, "RUNNING", already_exists)
        # Check if urls aready in Status Table
        already_visited = db.select_visited(conn, urls)

        # If not first time
        if len(already_visited) == 1:

            # ALREADY VISITED IN THE LAST 5 HOURS
            if datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours=24) > datetime.now() and relaunch != "True":
                update_running_status(conn, urls)
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
    conn = db.create_connection("visited.db")
    with conn:
        urls = request.args.get('url')  # if key doesn't exist, returns None
        relaunch = request.args.get('redo')
        maxi_urls = request.args.get('max')
        return generate_interactive_graph(conn, urls, relaunch, maxi_urls)
    conn.close()

@app.route('/api/headers')
def find_headers():
    value = request.args.get('url')
    if value:
        return find_all_headers_url(value)
    else:
        return "Please input a valid value like this: /api/headers?url='https://primates.dev'"

@app.route('/api/serp')
def find_rank_query():
    query = request.args.get('query')
    domain = request.args.get('domain')
    tld = request.args.get('tld')
    lang = request.args.get('lang')
    print (lang)
    if query and domain:
        return rank(domain,query, lang=lang, tld=tld)
    else:
        return 'Please input a valid value like this: /api/serp?domain=primates.dev&query=parse api xml response&tld=com&lang=en'
@app.route('/api/analysis/keywords')
def find_keywords_query():
    query = request.args.get('query')
    if query:
        return generate_results(query)
    else:
        return 'Please input a valid value like this: /api/analysis/keywords?query=parse api xml response'




if __name__ == '__main__':

    conn = db.create_connection("visited.db")

    if conn is not None:
        # create projects table and set running status to stopped
        initialize_db(conn)
    else:
        logging.warning("Error! cannot create the database connection.")

    logging.info("DB running")
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
