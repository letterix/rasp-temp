import os, os.path
import sys
sys.path.append('..')
import backend

current_dir = os.path.dirname(os.path.abspath(__file__))

def setup():
    drop_tables()
    create_tables()
    create_triggers()
    populate_testdata()
        
def populate_testdata():
    with open (os.path.join(current_dir, "../testdata/testdata.sql"), "r") as sqlfile:
        sql=sqlfile.read().replace('\n', '')
        for line in sql.split(';'):
            if line.strip():
                _exec(line)

def create_tables():
    with open (os.path.join(current_dir, "../db/createDB.sql"), "r") as sqlfile:
        sql=sqlfile.read().replace('\n', '')
        for line in sql.split(';'):
            if line.strip():
                _exec(line)

def create_triggers():
    with open (os.path.join(current_dir, "../db/triggers.sql"), "r") as sqlfile:
        sql=sqlfile.read()
        for line in sql.split('\n\n'):
            if line.strip():
                line = line.replace('/// DELIMITER ;', '').replace('DELIMITER ///', '')
                _exec(line)
        
def drop_tables():
    sql = """SELECT concat('SET foreign_key_checks = 0; DROP TABLE IF EXISTS ', table_name, ';')
            FROM information_schema.tables
            WHERE table_schema = 'aritermtest';"""

    drop_sqls = _query(sql)
    for drop_sql in drop_sqls:
        _exec(drop_sql[0])
        
def _exec(sql):
    conn = backend._get_connection()
    try:
        c = conn.cursor()
        for result in c.execute(sql, multi=True):
            pass
        conn.commit()
        c.close() 
    finally:
        conn.close()
        
def _query(sql, *args):
    conn = backend._get_connection()
    try:
        c = conn.cursor()
        c.execute(sql)
        data = c.fetchall()
        c.close() 
    finally:
        conn.close()
    return data
