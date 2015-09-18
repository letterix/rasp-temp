#import MySQLdb
import backend, json
from utils.encoder import simple_encoder

def get_by_installation(installation):
    sql = """SELECT * FROM sync_queue WHERE installation = %s"""
    return backend._query(sql, installation)

def get_by_id(id):
    return backend._query_for_one("""SELECT * FROM sync_queue WHERE id = %s""", id)

def get_all():
    return backend._query("""SELECT * FROM sync_queue WHERE NOW() > DATE_ADD(last_sync_attempt, INTERVAL 10 MINUTE) OR last_sync_attempt IS NULL""")

def delete(id, installation):
    return backend._exec("""DELETE FROM sync_queue WHERE id = %s AND installation = %s""", id, installation)

def insert(sync):
    return backend._exec("""INSERT INTO sync_queue(`installation`, `method`, `table`, `data`, `prev`) VALUES(%s,%s,%s,%s,%s)""", sync['installation'], sync['method'], sync['table'], json.dumps(sync['data'], default=simple_encoder), json.dumps(sync['prev'], default=simple_encoder))

def set_attempt_time(id, installation):
    return backend._exec("UPDATE sync_queue SET last_sync_attempt = NOW() WHERE id = %s AND installation = %s", id, installation)

def insert_params(installation, table, method, data, prev = None):
    return insert({
        'installation': installation,
        'method': method,
        'table': table,
        'data': data,
        'prev': prev
    })
