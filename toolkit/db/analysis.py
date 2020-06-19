import datetime
from toolkit.analysis import keywords
import json


def insert_query_db(conn, values):
    """Insert a query into the DB

    Arguments:
        conn {Connector} -- DB Connector
        result {[type]} -- [description]
    """
    sql = ''' INSERT INTO keywords(query,results,status_job,begin_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()


def select_query(conn, query):
    cur = conn.cursor()
    cur.execute("SELECT * FROM keywords WHERE query=?", (query,))

    row = cur.fetchall()
    return row


def update_running_db(conn, query, status):
    """Update running table where url = input

    Arguments:
        conn {Connector} -- DB Connector
        task {Array} -- Array of value: status, url
    """
    sql = ''' UPDATE keywords
              SET
                  status_job = ?
              WHERE urls = ?'''
    cur = conn.cursor()
    cur.execute(sql, (status, query))
    conn.commit()


def update_result_db(conn, task):
    sql = ''' UPDATE keywords
              SET
                  status_job = ? ,
                  begin_date = ?,
                  results = ?
              WHERE query = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def finished_all_jobs(conn):
    sql = ''' UPDATE keywords
              SET
                  status_job = ?
                  '''
    cur = conn.cursor()
    cur.execute(sql, "FINISHED")
    conn.commit()


def get_query_results(conn, query, redo=False):
    check_exist = select_query(conn, query)
    print
    if len(check_exist) > 0:
        if check_exist[0][3] == "RUNNING":
            return {"error": "query is already running, please wait and then refresh"}
        elif check_exist[0][3] == "FINISHED":
            return json.loads(check_exist[0][2])
        print(check_exist)
    else:
        insert_query_db(conn, (query, "", "RUNNING", datetime.datetime.now()))
        results = keywords.generate_results(query, 20)
        update_result_db(
            conn, ("FINISHED", datetime.datetime.now(), json.dumps(results), query))
        return results
    return "Blabla"
