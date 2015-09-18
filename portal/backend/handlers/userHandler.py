from dao import UserDao
from handlers import assigneesHandler
import authentication
from utils import validator
from common import *


def get_users():
    current_user = get_current_user()
    result = []
    customers = assigneesHandler.get_customers(current_user.get('username'))
    if authentication.has_full_access(current_user):
        # super user, master admin
        result = [_set_customers(u) for u in UserDao.get_all()]
    elif authentication.user_is_master(current_user):
        if authentication.user_is_assigned_master(current_user):
            # master user (assigned master customer)
            users = [_set_customers(u) for u in UserDao.get_all()]
            result = [u for u in users if authentication.allow_semi_user_changes(u)]
        else:
            # master user (not assigned master customer)
            for customer in customers:
                assigned_users = assigneesHandler.get_assignees(customer.get('customer'))
                users = [get_user(a['user']) for a in assigned_users]
                result = result + [u for u in users if authentication.allow_semi_user_changes(u)]
    else:
        # can only be assigned to one..
        customer = customers[0]
        assigned_users = assigneesHandler.get_assignees(customer.get('customer'))
        users = [get_user(a['user']) for a in assigned_users]
        result = [u for u in users if u and authentication.allow_semi_user_changes(u)]
    return result


def create_user(user):
    customers = user.get('customers')
    result = True
    for customer_id in customers:
        if not authentication.allow_changes(customer_id):
            result = False
            break
    if result:
        msg = validator.new_user(user)
        if not msg:
            set_password_salt(user)
            res = UserDao.create_user(user)
            res = assigneesHandler.update_assignee(user)
            return True
        else:
            return msg

def get_current_user():
    user = cherrypy.session.get('user')
    return _set_customers(user)

def _set_customers(user):
    if authentication.has_full_access(user) or authentication.user_is_assigned_master(user):
        user['customers'] = [1]
        return user
    user['customers'] = [a['customer'] for a in assigneesHandler.get_customers(user.get('username'))]
    return user

def get_user(username=None):
    current_user = get_current_user()
    if not username:
        return current_user
    else:
        user = UserDao.get_user(username)
        if user:
            user = _set_customers(user)
            if authentication.allow_semi_user_changes(user):
                return user


def update_user(user):
    if authentication.allow_full_user_changes(user):
        return full_update_user(user)
    if authentication.allow_semi_user_changes(user):
        return semi_update_user(user)
    return False


def semi_update_user(user):
    password = user.get('password')
    old_user = get_user(user.get('username'))
    user['role'] = old_user.get('role')
    if password and password != validator.PASSWORD_PLACEHOLDER:
        set_password_salt(user)
        UserDao.update_user_with_pw_and_salt(user)
    else:
        UserDao.update_user(user)
    return True


def full_update_user(user):
    password = user.get('password')
    if password and password != validator.PASSWORD_PLACEHOLDER:
        set_password_salt(user)
        UserDao.update_user_with_pw_and_salt(user)
    else:
        UserDao.update_user(user)
    assigneesHandler.update_assignee(user)
    return True


def delete_user(username):
    user = UserDao.get_user(username)
    if user and authentication.allow_full_user_changes(username):
        UserDao.delete_user(username)
    user = UserDao.get_user(username)
    if not user:
        assignees = assigneesHandler.get_customers(username)
        for assignee in assignees:
            assigneesHandler.delete(assignee.get('user'), assignee.get('customer'))
        assignees = assigneesHandler.get_customers('username')
        if not assignees or len(assignees) == 0:
            return True
    return False


def set_password_salt(user):
    salt_and_password = authentication.get_salt_and_password_for(user.get('password'))
    user['password'] = salt_and_password['password']
    user['salt'] = salt_and_password['salt']

def safe_fields(user):
    user['password'] = validator.PASSWORD_PLACEHOLDER
    user['confirmPassword'] = validator.PASSWORD_PLACEHOLDER
    user['salt'] = ""
    return user