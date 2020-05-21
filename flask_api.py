from flask import Flask, render_template, jsonify, request, render_template
app = Flask(__name__)
from core import generate_graph_internal_link_interactive_api
from bokeh.embed import components
import sqlite3

from datetime import datetime

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS visited (
                                        id integer PRIMARY KEY,
                                        urls text NOT NULL,
                                        begin_date text NOT NULL,
                                        script text,
                                        div text
                                        
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
    except Error as e:
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
    return cur.lastrowid

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

def select_visited(conn, urls):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM visited")

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


@app.route('/api/graph')
def interactive_graph():
    conn = create_connection("visited.db")
    urls = request.args.get('url') #if key doesn't exist, returns None
    if urls is None:
        return "Empty Url paramaters"
    hello = select_visited(conn, urls)
    if len(hello) == 1:
        print(hello)
    else:
        print(hello)
        print("BYEBEYBEYBYEBEYBE")
    plot, domain = generate_graph_internal_link_interactive_api(urls)
    script, div = components(plot)
   
    insert_url_db(conn,(urls, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), script, div))
    return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask")

if __name__ == '__main__':

    conn = create_connection("visited.db")

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")
    
    print ("Table created successfully")
    app.run(debug=True, port=5000) #run app in debug mode on port 5000