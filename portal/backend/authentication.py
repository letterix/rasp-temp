from dao import UserDao
import logging
import os
import cherrypy

from functools import wraps
from common import *
from handlers import assigneesHandler, customerHandler, userHandler
import hashlib
import uuid

SUPER_USER = 'super_user'
MASTER_ADMIN = 'master_admin'
MASTER_USER = 'master_user'
ADMIN = 'admin'
USER = 'user'

LOG = logging.getLogger()
current_dir = os.path.dirname(os.path.abspath(__file__))

def check_password(username, password):
    user = UserDao.get_user(username)
    if user is None:
        LOG.warning("Failed logon attempt fort " + str(username))
        return False
    salt = user['salt']
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    if user and username == user['username'] and hashed_password == user['password']:
        return user
    else:
        LOG.warning("Failed logon attempt for " + str(username))
        return False


def login(session, user):
    id_for_deletion = None
    for id, existing_session in session.cache.items():
        if existing_session[0] and existing_session[0].get("user") and existing_session[0]["user"] == user:
            print("user already logged in, deleting old session")
            id_for_deletion = id
    if id_for_deletion:
        del session.cache[id_for_deletion]

    set_user_in_session(session, user)
    return user


def logout(session):
    session['user'] = None
    session['roles'] = []
    del session['user']


def set_user_in_session(session, user):
    session['user'] = user


def is_logged_in(session):
    return 'user' in session


def is_master(user):
    if user['role'] in master_roles():
        return True
    else:
        return False


def is_master_logged_in(session):
    user = session['user']
    if user:
        if is_master(user):
            return True
    return False


def get_current_user():
    return cherrypy.session['user']


def get_salt_and_password_for(clear_text_password):
    salt = uuid.uuid4().hex
    password = hashlib.sha512(clear_text_password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return {'salt': salt, 'password': password}


def accepted_roles(roles):
    def true_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if user.get('role') in roles:
                response = f(*args, **kwargs)
            else:
                response = UnauthorizedResponse("Not Authorized")
                # response = ConflictResponse(KEY_NOT_AUTHORIZED) # Could be used instead of UnauthorizedResponse("Not Authorized")
            return response
        return wrapped
    return true_decorator


def has_full_access(user):
    return user['role'] in super_roles()


def user_is_assigned_customer(customer, user):
    return customer['id'] in [d['customer'] for d in assigneesHandler.get_customers(user.get('username'))]


def user_is_assigned_master(user):
    return user['username'] in [d['user'] for d in assigneesHandler.get_assignees(1)]



def user_can_view_customer(user, customer):
    return user_is_assigned_customer(customer, user) or user_is_assigned_master(user)


def user_is_admin(user):
    return user.get('role') in admin_roles()

def user_is_master(user):
    return user.get('role') in master_roles()



#to check if user can view customer
def allow_viewing(customer_id):
    result = False
    user = cherrypy.session.get('user')
    customer = customerHandler.get_customer(customer_id)
    if customer:
        if user_can_view_customer(user, customer):
            result = True
    if has_full_access(user):
        result = True
    return result


#To check if user can edit customer
def allow_changes(customer_id):
    user = cherrypy.session.get('user')
    customer = customerHandler.get_customer(customer_id)
    if has_full_access(user):
        return True
    if user_is_master(user) and not user_is_admin(user):
        # master_user, check if customer can be edited
        if user_can_view_customer(user, customer):
            return True
    if user_can_view_customer(user, customer) and user_is_admin(user):
        return True
    return False


#To check if the current user can edit basic info of the given user
def allow_semi_user_changes(user):
    current_user = userHandler.get_current_user()
    if user.get('username') == current_user.get('username') or has_full_access(current_user):
        # same user or the current user has full access
        return True
    if user_is_master(current_user):
        # can only edit lower access levels
        if compare_access_level(current_user, user) > 0:
            if user_is_assigned_master(current_user):
                return True
            # need to be able to be able to be able to edit all customers of the user
            customers = user.get('customers')
            result = True
            for customer_id in customers:
                if not allow_changes(customer_id):
                    result = False
            return result
    if not user_is_master(current_user):
        if compare_access_level(current_user, user) > -1:
             # need to be able to be able to be able to edit all customers of the user
            customers = user.get('customers')
            result = True
            for customer_id in customers:
                if not allow_changes(customer_id):
                    result = False
            return result
    return False


#To check if the current user can edit full info of the given user
def allow_full_user_changes(user):
    current_user = userHandler.get_current_user()
    if has_full_access(current_user):
        # current user has full access
        return True
    # need to be able to be able to be able to edit all customers of the user
    customers = user.get('customers')
    result = True
    for customer_id in customers:
        if not allow_changes(customer_id):
                result = False
    if user_is_master(current_user) and not user_is_admin(current_user):
        if user_is_master(user):
            result = False
            # master user trying to update another master user or higher.
    return result


def compare_access_level(user_1, user_2):
    levels = all_roles()
    l1 = levels.index(user_1.get('role'))
    l2 = levels.index(user_2.get('role'))
    if l1 > l2:
        return 1
    if l1 < l2:
        return -1
    else:
        return 0

def admin_roles():
    return [SUPER_USER,
            MASTER_ADMIN,
            ADMIN]


def master_roles():
    return [SUPER_USER,
            MASTER_ADMIN,
            MASTER_USER]


def super_roles():
    return [SUPER_USER,
            MASTER_ADMIN]

def semi_admin_roles():
    return[ADMIN,
           MASTER_USER,
           MASTER_ADMIN,
           SUPER_USER]

def all_roles():
    return[USER,
           ADMIN,
           MASTER_USER,
           MASTER_ADMIN,
           SUPER_USER]