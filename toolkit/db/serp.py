

def insert_query_db(conn, values):
    """Insert a query into the DB

    Arguments:
        conn {Connector} -- DB Connector
        result {[type]} -- [description]
    """
    sql = ''' INSERT INTO serp(query,pos, result,begin_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

def select_query(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM serp ORDER BY begin_date ASC")

    row = cur.fetchall()
    return row