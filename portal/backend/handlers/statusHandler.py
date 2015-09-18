from dao import log_dao
from handlers import installationHandler, logHandler
from datetime import datetime
import time, config


def set_status_for_customers(customers):
    for customer in customers:
        set_status_for_customer(customer)


def set_status_for_customer(customer):
    # assume false
    customer['connected'] = False
    installations = installationHandler.get_by_customer(customer.get('id'))
    if installations:
        one_connected = set_status_for_installations(installations)
        customer['connected'] = one_connected
    customer['warnings'] = logHandler.get_warnings_customer(customer)
    customer['alarms'] = logHandler.get_alarms_customer(customer)


def set_status_for_installations(installations):
    one_connected = False
    for installation in installations:
        if set_status_for_installation(installation):
            one_connected = True
    return one_connected


def set_status_for_installation(installation):
    # assume false
    connected = installationHandler.get_connection_status_for(installation.get('serial_number'))
    installation['connected'] = connected
    installation['warnings'] = logHandler.get_warnings_installation(installation)
    installation['alarms'] = logHandler.get_alarms_installation(installation)
    return connected


def set_status_for_controllers(controllers):
    d2 = datetime.now()
    d2_ts = time.mktime(d2.timetuple())
    for controller in controllers:
        set_status_for_controller(controller, d2_ts)


def set_status_for_controller(controller, d2_ts=None):
    set_status_for_entity(controller, d2_ts)
    controller['warnings'] = logHandler.get_warnings_controller(controller)
    controller['alarms'] = logHandler.get_alarms_controller(controller)


def set_status_for_tags(tag_list):
    d2 = datetime.now()
    d2_ts = time.mktime(d2.timetuple())
    for tag in tag_list:
        set_status_for_entity(tag, d2_ts)
    return tag_list



def set_status_for_entity(entity, d2_ts=None):
    if not d2_ts:
        d2 = datetime.now()
        d2_ts = time.mktime(d2.timetuple())
    # assume false
    entity['connected'] = False
    d1 = entity.get('time')
    if d1:

        # convert to unix timestamp
        d1_ts = time.mktime(d1.timetuple())

        # they are now in seconds
        diff = int(d2_ts-d1_ts)

        # Two times the actual synch intervall
        if diff < config.RUN_SYNC_FREQUENCY * 3:
            entity['connected'] = True
