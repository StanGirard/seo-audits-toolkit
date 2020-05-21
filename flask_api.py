from flask import Flask, render_template, jsonify, request, render_template
app = Flask(__name__)
from core import generate_graph_internal_link_interactive_api
from bokeh.embed import components
import sqlite3
import urllib.parse

from datetime import datetime, timedelta

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS visited (
                                        id integer PRIMARY KEY,
                                        urls text NOT NULL,
                                        begin_date text NOT NULL,
                                        script text,
                                        div text
                                        
                                    ); """
sql_create_running_table = """ CREATE TABLE IF NOT EXISTS running (
                                        id integer PRIMARY KEY,
                                        urls text NOT NULL,
                                        status_job text NOT NULL
                                        
                                    ); """

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_url_db(conn, result):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO visited(urls,begin_date,script,div)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    print(result)
    cur.execute(sql, result)
    con.commit()

def insert_running_db(conn, result):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO running(urls,status_job)
              VALUES(?,?) '''
    cur = conn.cursor()
    print(result)
    cur.execute(sql, result)
    conn.commit()

def update_url_db(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE visited
              SET
                  begin_date = ? ,
                  script = ?,
                  div = ?
              WHERE urls = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def update_running_db(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE running
              SET
                  status_job = ?
              WHERE urls = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def update_running_db_stopped(conn):
    task = ["STOPPED"]
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE running
              SET
                  status_job = ? '''
              
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def select_visited(conn, urls):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM visited WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row

def select_running(conn, urls):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM running WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("ERROR")

    return conn

def check_status_url(conn,urls, status):
    urls = select_running(conn,urls)
    if len(urls) != 0:
        if urls[0][2] == status:
            print("HAHAHAHAHAHHAHAAHAHAHAHAHAHAH")
            print(urls[0][2])
            return True, True
        else:
            return False, True
    else: 
        return True, False


@app.route('/api/graph')
def interactive_graph():
    conn = create_connection("visited.db")
    with conn:
        urls = request.args.get('url') #if key doesn't exist, returns None
        relaunch = request.args.get('redo')
        if urls is None:
            return "Empty Url paramaters"
        stopped, already_exists = check_status_url(conn,urls, "STOPPED")
        if stopped == True:
            print("STOP" + str(stopped))
            if already_exists:
                update_running_db(conn, ("RUNNING", urls))
            else:
                insert_running_db(conn, (urls, "RUNNING"))

            already_visited = select_visited(conn, urls)
            if len(already_visited) == 1 and datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours = 5) > datetime.now() and relaunch != "True":
                print("ALREADY VISITED IN THE LAST 5 HOURS")
                update_running_db(conn, ("STOPPED", urls))
                return render_template("bokeh.html", script=already_visited[0][3], div=already_visited[0][4], domain=urllib.parse.urlparse(already_visited[0][1]).netloc, template="Flask", time=datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S'))
            plot, domain = generate_graph_internal_link_interactive_api(urls)
            script, div = components(plot)

            if len(already_visited) == 1 and (datetime.strptime(already_visited[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours = 5) < datetime.now() or relaunch == "True") :
                print("ALREADY REGISTERED BUT UPDATING")
                update_url_db(conn,(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), script, div, urls))
            else:
                print("FIRST TIME")
                insert_url_db(conn,(urls, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), script, div))
            update_running_db(conn, ("STOPPED", urls))
            return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask" ,time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        else:
            return "JOB IS ALREADY RUNNING. PLEASE WAIT AND REFRESH"
if __name__ == '__main__':

    conn = create_connection("visited.db")

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        create_table(conn, sql_create_running_table)
        update_running_db_stopped(conn)
    else:
        print("Error! cannot create the database connection.")
    
    print ("Table created successfully")
    app.run(debug=True, port=5000) #run app in debug mode on port 5000