#import MySQLdb
from exceptions.exceptions import *
import backend

def get_settings(installation, role):

    if role == 'admin':
        sql =  """SELECT * FROM settings INNER JOIN setting_types ON settings.setting_name = setting_types.setting_name WHERE installation = %s ORDER BY `group`"""
        return backend._query(sql, installation)
    else:
        sql = """SELECT * FROM settings INNER JOIN setting_types ON settings.setting_name = setting_types.setting_name WHERE installation = %s AND `role` = %s ORDER BY `group`"""
        return backend._query(sql, installation, role)

def get_setting_by_name(installation, setting_name):
    sql = """SELECT * FROM settings WHERE setting_name = %s AND installation = %s"""
    data = backend._query_for_one(sql, setting_name, installation)
    return data

def get_pellets_settings(installation):
    sql = """SELECT * FROM settings WHERE installation = %s AND setting_name IN ('internal_pelletslevel_warning', 'external_pelletslevel_warning', 'consumption_rate')"""
    data = backend._query(sql, installation)
    return data

def update_setting(setting, installation):
    sql = """UPDATE settings SET value = %s WHERE setting_name = %s AND installation = %s"""
    res = backend._exec(sql, setting.get('value'), setting.get('setting_name'), installation)
    return res

def get_default_for(setting_name):
    sql = """SELECT default_value FROM setting_types WHERE setting_name = %s"""
    data = backend._query_for_one(sql, setting_name)
    return data['default_value']

def get_all_setting_types():
    sql = """SELECT * FROM setting_types"""
    data = backend._query(sql)
    return data

def create_setting_with(setting_type, installation):
    return backend._exec("""INSERT INTO settings(`installation`, `setting_name`, `value`) VALUES(%s, %s, %s)""", installation['serial_number'], setting_type['setting_name'], setting_type['default_value'])
