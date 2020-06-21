




def insert_url_db(conn, result):
    """Insert an url into the DB

    Arguments:
        conn {Connector} -- DB Connector
        result {[type]} -- [description]
    """
    sql = ''' INSERT INTO graphs(urls,begin_date,script,div,status_job)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, result)
    conn.commit()


def update_url_db(conn, task):
    """Update an URL data in the DB

    Arguments:
        conn {Connector} -- DB Connector
        task {Array} -- Array of parameters: begin_date, script, div, url
    """
    sql = ''' UPDATE graphs
              SET
                  begin_date = ? ,
                  script = ?,
                  div = ?,
                  status_job = ?
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
    sql = ''' UPDATE graphs
              SET
                  status_job = ?
              WHERE urls = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def select_visited(conn, urls):
    cur = conn.cursor()
    cur.execute("SELECT * FROM graphs WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row


def select_running(conn, urls):
    cur = conn.cursor()
    cur.execute("SELECT * FROM graphs WHERE urls=?", (urls,))

    row = cur.fetchall()

    return row


def check_status_url(conn, urls, status):
    urls = select_running(conn, urls)
    if len(urls) != 0:
        if urls[0][5] == status:
            return True, True
        else:
            return False, True
    else:
        return True, False
