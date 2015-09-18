#import MySQLdb
from exceptions.exceptions import *
import backend

def get(customer_id):
    sql = """SELECT * FROM customers WHERE `id` = %s"""
    return backend._query_for_one(sql, customer_id)


def get_all():
    sql = """SELECT * FROM customers"""
    return backend._query(sql)


def delete_customer(customer_id):
    sql ="""DELETE FROM customers WHERE `id` = %s"""
    return backend._exec(sql, customer_id)


def create_customer(customer):
    return backend._exec("""INSERT INTO customers(`name`) VALUES(%s)""",
                        customer.get('name'))


def update(customer):
    sql = """UPDATE customers SET `name` = %s WHERE `id` = %s;"""
    return backend._exec(sql, customer.get('name'), customer.get('id'))
