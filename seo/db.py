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
    cur.execute(sql, result)
    conn.commit()

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
            return True, True
        else:
            return False, True
    else: 
        return True, False