import dao.UserDao as userDao
import re
from common import *

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

PASSWORD_KEY = 'password'

PASSWORD_PLACEHOLDER = 'hiddensecure'

def valid_name(name):
    return name and len(name) > 1

def valid_surname(surname):
    return surname and len(surname) > 1

def valid_phone(phone):
    return phone and len(phone) > 5

def valid_email(email):
    return email and EMAIL_REGEX.match(email)

def valid_user(user):
    msg = []
    if user:
        if not valid_phone(user.get('phone')):
            msg.append(KEY_INVALID_PHONE)
        if not valid_email(user.get('email')):
            msg.append(KEY_INVALID_EMAIL)
        if not valid_surname(user.get('surname')):
            msg.append(KEY_INVALID_SURNAME)
        if not valid_surname(user.get('name')):
            msg.append(KEY_INVALID_NAME)
    else:
        msg.append(KEY_MISSING_DATA)
    return msg

def new_user(user):
    msg = []
    username_exists = userDao.username_exists(user.get('username'))
    if username_exists:
        msg.append(KEY_USERNAME_TAKEN)

    if PASSWORD_KEY not in user:
        msg.append(KEY_INVALID_PASSWORD)

    error_msg = valid_user(user)
    if len(error_msg):
        msg += error_msg
    return msg

def updated_user(user):
    return valid_user(user)


def pellets_status(ps):
    return ps.get('current') > 0 and ps.get('max') > 0
