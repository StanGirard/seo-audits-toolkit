import sqlite3
import logging


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
            update_running_db(conn, ("RUNNING", urls))
        else:
            insert_running_db(conn, (urls, "RUNNING"))
    else:
        update_running_db(conn, ("STOPPED", urls))

def insert_url_db(conn, result):
    """Insert an url into the DB

    Arguments:
        conn {Connector} -- DB Connector
        result {[type]} -- [description]
    """
    sql = ''' INSERT INTO visited(urls,begin_date,script,div)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, result)
    conn.commit()


def insert_running_db(conn, status):
    """Insert line in table Running

    Arguments:
        conn {Connector} -- DB Connector
        status {String} -- Status Job
    """
    sql = ''' INSERT INTO running(urls,status_job)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, status)
    conn.commit()


def update_url_db(conn, task):
    """Update an URL data in the DB

    Arguments:
        conn {Connector} -- DB Connector
        task {Array} -- Array of parameters: begin_date, script, div, url
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
    """Update running table where url = input

    Arguments:
        conn {Connector} -- DB Connector
        task {Array} -- Array of value: status, url
    """
    sql = ''' UPDATE running
              SET
                  status_job = ?
              WHERE urls = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()




def select_visited(conn, urls):
    cur = conn.cursor()
    cur.execute("SELECT * FROM visited WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row


def select_running(conn, urls):
    cur = conn.cursor()
    cur.execute("SELECT * FROM running WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row


def check_status_url(conn, urls, status):
    urls = select_running(conn, urls)
    if len(urls) != 0:
        if urls[0][2] == status:
            return True, True
        else:
            return False, True
    else:
        return True, False
