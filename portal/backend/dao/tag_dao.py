#import MySQLdb
from exceptions.exceptions import *
import backend

def get_all(serial_number, controller_ip):
    sql = """SELECT * FROM tags WHERE `installation` = %s AND `controller_ip` = %s"""
    return backend._query(sql, serial_number, controller_ip)

def get_by_installation_and_type(serial_number, type):
    sql = """SELECT * FROM tags WHERE `installation` = %s AND `type` = %s"""
    return backend._query(sql, serial_number, type)

def get_by_controller_and_type(serial_number, controller_ip, type):
    sql = """SELECT * FROM tags WHERE `installation` = %s AND `controller_ip` = %s AND `type` = %s"""
    return backend._query(sql, serial_number, controller_ip, type)


def get(serial_number, controller_ip, name):
    sql = """SELECT * FROM tags WHERE `installation` = %s AND `controller_ip` = %s AND `name` = %s"""
    return backend._query_for_one(sql, serial_number, controller_ip, name)

def update_tag(tag):
    sql = """UPDATE tags SET `address` = %s, `type` = %s WHERE `name` = %s AND `installation` = %s AND `controller_ip` = %s"""
    return backend._exec(sql, tag.get('address'), tag.get('type'), tag.get('name'), tag.get('installation'), tag.get('controller_ip'))


def delete_tag(serial_number, controller_ip, name):
    sql = """DELETE FROM tags WHERE `installation` = %s AND `controller_ip` = %s AND `name` = %s"""
    return backend._exec(sql, serial_number, controller_ip, name)


def create_tag(tag):
    return backend._exec("""INSERT INTO tags(`installation`, `controller_ip`, `name`, `address`, `type`) VALUES(%s, %s, %s, %s, %s)""",
                         tag.get('installation'), tag.get('controller_ip'), tag.get('name'), tag.get('address'), tag.get('type'))

