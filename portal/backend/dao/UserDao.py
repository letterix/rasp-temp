#import MySQLdb
from exceptions.exceptions import *
import backend

def get_all():
    return backend._query("SELECT * FROM users")

def username_exists(username):
    sql = """SELECT COUNT(username) `exists` FROM users WHERE username = %s"""
    return backend._query_for_one(sql, username)['exists']

def get_by_pi_mac(pi_mac):
    sql = """SELECT * FROM users WHERE pi_mac = %s"""
    return backend._query(sql, pi_mac)

def get_users_by_role(role = 'user'):
    sql = """SELECT * from users WHERE role = %s"""
    data =  backend._query(sql, role)
    return {'users': data}
 
def get_user(username):
    sql = """SELECT * from users WHERE username = %s"""
    data = backend._query_for_one(sql , username)
    return data

def get_user_by_id(userid):
    sql = """SELECT * from users WHERE id = %s"""
    data = backend._query_for_one(sql, userid)
    return data

def create_user(user):
    sql = """INSERT INTO users (username, surname, name, phone, password, salt,  email, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    created = backend._exec(sql, user.get('username'), user.get('surname'), user.get('name'), user.get('phone'), user.get('password'), user.get('salt'), user.get('email'), user.get('role'))
    if created:
        created = get_user(user.get('username'))
        print("CREATED USER: ", created)
    else:
        raise ResourceAlreadyExist("Cannot create user")
    return created

def delete_user(username):
    sql = """DELETE FROM users WHERE username = %s"""
    if not backend._exec(sql, username) == 1:
        raise ResourceNotFound("User not found")

def update_user_with_pw_and_salt(u):
    sql = """UPDATE users SET name = %s, surname = %s, phone = %s, email=%s, password = %s,  salt = %s, lang = %s, role = %s  WHERE username = %s"""
    updated = backend._exec(sql, u['name'], u['surname'], u['phone'], u['email'], u['password'], u['salt'], u['lang'], u['role'], u['username'])
    return u if updated else False

def update_user(u):
    sql = """UPDATE users SET name = %s, surname = %s, phone = %s, email=%s, lang = %s, role = %s WHERE username = %s"""
    updated = backend._exec(sql, u['name'], u['surname'], u['phone'], u['email'], u['lang'], u['role'], u['username'])
    return u if updated else False


def update_cookie_id(cookie_id, expire, username):
    sql = """UPDATE users SET cookie_id = %s, cookie_expire = %s WHERE username = %s"""
    return backend._exec(sql, cookie_id, expire, username)

def get_cookie_id(username):
    sql = "SELECT cookie_id, cookie_expire FROM users WHERE username = %s"
    return backend._query_for_one(sql, username)

def delete_cookie(username):
    sql = "UPDATE users SET cookie_id = NULL, cookie_expire = NULL WHERE username = %s"
    return backend._exec(sql, username)


