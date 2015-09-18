#import MySQLdb
from exceptions.exceptions import *
import backend

def get_assignees(customer_id):
    sql = """SELECT * FROM assignees WHERE customer = %s;"""
    return backend._query(sql, customer_id)

def get_customers(username):
    sql = """SELECT * FROM assignees WHERE `user` = %s;"""
    return backend._query(sql,  username)

def delete_assignee(username, customer_id):
    sql ="""DELETE FROM `assignees` WHERE `user` = %s AND customer = %s;"""
    return backend._exec(sql, username, customer_id)

def create_assignee(username, customer_id):
    return backend._exec("""INSERT INTO assignees(`user`, `customer`) VALUES(%s, %s);""",
                         username, customer_id)

