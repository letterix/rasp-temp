import cherrypy
import authentication
from dao import Installations_dao, sync_queue_dao, settings_dao
from ws.sync_users import SYNC_INSTALLATIONS


def get_all():
    return Installations_dao.get_all()


def get_customerless():
    return Installations_dao.get_customerless()


def get_by_customer(customer_id):
    res = None
    if authentication.allow_viewing(customer_id):
        res = Installations_dao.get_all(customer_id)
    return res


def get(serial_number, internal=False):
    res = None
    installation = Installations_dao.get(serial_number)
    if installation:
        if internal or authentication.allow_viewing(installation.get('customer')):
            res = installation
    return res


def get_settings(serial_number):
    res = None
    if get(serial_number):
        res = Installations_dao.get_settings(serial_number)
    return res


def update_installation(installation):
    res = None
    if get(installation.get('serial_number')):
        res = Installations_dao.update(installation)
    return res


def update_settings(settingsToUpdate):
    msg = []
    if type(settingsToUpdate) == list:
        for setting in settingsToUpdate:
            installation = setting.get('installation')
            updated = update_setting(setting, installation)
            msg.append({setting.get('setting_name'): updated})

    elif type(settingsToUpdate) == dict:
        installation = settingsToUpdate.get('installation')
        updated = update_setting(settingsToUpdate, installation)
        msg.append({settingsToUpdate.get('setting_name'): updated})
    else:
       msg.append("ERROR")
    return msg


def update_setting(setting, installationValue, sync=True):
    print("update: ", setting)
    prev = Installations_dao.get_setting_by_name(installationValue, setting['setting_name'])
    updated = Installations_dao.update_setting(setting, installationValue)
    if updated and sync:
        sync = sync_queue_dao.insert_params(installationValue, 'settings', 'update', setting, prev)
    return updated

def get_setting(installationValue, setting_name):
    return Installations_dao.get_setting_by_name(installationValue, setting_name)



def factory_reset(installation_id,setting_name):
    if installation_id:
        setting = get_setting(installation_id, setting_name)
        default = Installations_dao.get_default_for(setting_name)
        setting['value'] = default
        update_setting(setting, installation_id)
    else:
        return NameError("Error factory reset")
    return installation_id

def factory_reset_all(installationId):
    settings = Installations_dao.get_settings(installationId)
    for setting in settings:
        setting['value'] = setting['default_value']
        update_setting(setting, setting['installation'])
    return installationId


def get_connection_status_for(serial_number):
    res = None
    if get(serial_number):
        res = serial_number in SYNC_INSTALLATIONS
    return res


def is_registered(serial_number):
    return Installations_dao.get(serial_number) is not None


def register(serial_number, model, name=""):
    new_installation = dict()
    new_installation['serial_number'] = serial_number
    new_installation['model'] = model
    new_installation['name'] = name
    return Installations_dao.register(new_installation)

def create(serial_number, model, name="", customer=1):
    new_installation = dict()
    new_installation['serial_number'] = serial_number
    new_installation['model'] = model
    new_installation['name'] = name
    new_installation['customer'] = customer
    installation = get(serial_number)
    if installation:
        installation['customer'] = customer
        installation['model'] = model
        installation['name'] = name
        return Installations_dao.update(installation)
    return Installations_dao.create(new_installation)


def delete_installation(serial_number):
    res = False
    installation = get(serial_number)
    if installation:
        res = Installations_dao.delete(serial_number)
    return res





