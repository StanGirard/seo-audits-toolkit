import sqlite3
import logging
from toolkit.db import conf

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS graphs (
                                        id integer PRIMARY KEY,
                                        urls text NOT NULL,
                                        begin_date text NOT NULL,
                                        script text,
                                        div text,
                                        status_job text NOT NULL
                                        
                                    ); """
sql_create_running_table = """ CREATE TABLE IF NOT EXISTS running (
                                        id integer PRIMARY KEY,
                                        urls text NOT NULL,
                                        status_job text NOT NULL
                                        
                                    ); """

sql_create_keywords_table = """ CREATE TABLE IF NOT EXISTS keywords (
                                        id integer PRIMARY KEY,
                                        query text NOT NULL,
                                        results text NOT NULL,
                                        status_job text NOT NULL,
                                        begin_date text NOT NULL
                                );
                            """


def initialize_db(conn):
    """Initialize the DB

    Arguments:
        conn {Connection} -- Connector
    """
    conf.create_table(conn, conf.sql_create_projects_table)
    conf.create_table(conn, conf.sql_create_running_table)
    conf.create_table(conn, conf.sql_create_keywords_table)
    conf.update_running_db_stopped(conn)


def create_table(conn, create_table_sql):
    """Create a table in the database

    Arguments:
        conn {Connection} -- Connection to the db
        create_table_sql {String} -- Create script for the table
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        logging.warning(e)


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        logging.warning("ERROR")

    return conn


def update_running_db_stopped(conn):
    task = ["FINISHED"]
    sql = ''' UPDATE graphs
              SET
                  status_job = ? '''
    cur = conn.cursor()
    cur.execute(sql, task)

    sql = ''' UPDATE keywords
              SET
                  status_job = ? '''
    cur = conn.cursor()
    cur.execute(sql, ("FINISHED",))
    conn.commit()
