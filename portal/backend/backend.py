#import MySQLdb
import mysql.connector, sqlite3, logging, config, re
from imp import reload
from utils.encoder import escape


config = reload(config)
LOG = logging.getLogger()
TEST = False

def set_test():
    global TEST
    TEST = True

def _get_connection():
    """Get a connection to the database"""
    if TEST:
        cfg = config.TESTDATABASE
    else:
        cfg = config.DATABASE
    return mysql.connector.connect(user=cfg['user'], password=cfg['password'], host=cfg['host'], database=cfg['dbname'])

def _exec(sql, *params):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        cur.execute("""SELECT ROW_COUNT();""")
        rows = cur.fetchall()[0][0]
        conn.commit()
        return rows
    except:
        LOG.error("Calling %s with params %s raised an exception " % (sql, params))
        raise
    finally:
        del cur

def _exec_with_return_id(sql, *params):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        last_row_id = cur.lastrowid
        conn.commit()
        return last_row_id
    except:
        LOG.error("Calling %s with params %s raised an exception " % (sql, params))
        raise
    finally:
        del cur

def _query(sql, *args):
    conn = _get_connection()
    try:
        c = conn.cursor()
        c.execute(sql, args)
        data = c.fetchall()
        data = [dict(zip(c.column_names, row))
                 for row in data]
        c.close() 
    finally:
        conn.close()
    return data

def _query_for_one(sql, *args):
    conn = _get_connection()
    try:
        c = conn.cursor()
        c.execute(sql, args)
        data = c.fetchone()
        if data is not None:
            data = dict(zip(c.column_names, data))
        c.close() 
    finally:
        conn.close()
    return data
