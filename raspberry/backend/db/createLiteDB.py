#!/usr/bin/python
# -*- coding: utf-8 -*-
import config, json, backend
import sqlite3 as lite
from dao import sync_queue_dao
from utils.encoder import simple_encoder
from sync.sync_methods import *
import sys

try:
    con = lite.connect(config.DATABASE['dbname'])

    cur = con.cursor()  

    cur.executescript("""
    DROP TABLE IF EXISTS `sync_queue`;
    CREATE TABLE  `sync_queue` (
        `id` INTEGER PRIMARY KEY,
        `installation` varchar(100) NOT NULL,
        `table` varchar(100) NOT NULL,
        `method` varchar(100) NOT NULL,
        `data` TEXT NOT NULL,
        `prev` TEXT,
        `last_sync_attempt` DATETIME)""")
    con.commit()

except lite.Error as e:
    
    if con:
        con.rollback()
        
    print("Error %s:" % e.args[0])
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 