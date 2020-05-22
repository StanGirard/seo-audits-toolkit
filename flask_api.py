import urllib.parse
from datetime import datetime, timedelta
from seo import db
from bokeh.embed import components
from seo.core import generate_graph_internal_link_interactive
from flask import Flask, render_template, request
app = Flask(__name__)


def initialize_db(conn):
    db.create_table(conn, db.sql_create_projects_table)
    db.create_table(conn, db.sql_create_running_table)
    db.update_running_db_stopped(conn)


def update_or_insert_graph_in_db(conn, urls, maximum, update=False):
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
        print(maxi_urls)
        print("HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA")
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


@app.route('/')
def interactive_graph():
    conn = db.create_connection("visited.db")
    with conn:
        urls = request.args.get('url')  # if key doesn't exist, returns None
        relaunch = request.args.get('redo')
        maxi_urls = request.args.get('max')
        return generate_interactive_graph(conn, urls, relaunch, maxi_urls)
    conn.close()


if __name__ == '__main__':

    conn = db.create_connection("visited.db")

    if conn is not None:
        # create projects table and set running status to stopped
        initialize_db(conn)
    else:
        print("Error! cannot create the database connection.")

    print("DB running")
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
