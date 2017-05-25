import time


def query_db(db, query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_proxy_id(proxy_ip, proxy_port):
    """Convenience method to look up the id of a proxy."""
    rv = query_db('select proxy_id from proxy_table where proxy_ip = ? and proxy_port = ?',
                  proxy_ip, proxy_port, one=True)
    return rv[0] if rv else None


def insert_proxy_db(db, proxy_ip, proxy_port, provider, anonymity=None):
    db.execute(
        '''INSERT OR REPLACE INTO proxy (ip, port, provider, anonymity_level, add_date) VALUES (?, ?, ?, ?, ?)''',
        (proxy_ip, proxy_port, provider, anonymity, int(time.time())))
    db.commit()


def query_db_jsonified(db, query, args=()):
    cursor = db.cursor()
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r