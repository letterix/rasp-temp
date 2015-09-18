from dao import log_dao
from handlers import installationHandler, tagHandler, mailHandler, controllerHandler, customerHandler


def get_log_items_for(installation, fromDate, toDate):
    return log_dao.get_log_for(installation, fromDate, toDate)


def get_latest_entry(installation, controller_ip):
    return log_dao.get_last_entry(installation, controller_ip)


def create_log_entry(data, installation):
    if data['type'] == 'alarm' and data['value'] == 1:
        #installation_obj = installationHandler.get(installation, True)
        #controller_obj = controllerHandler.get_controller(installation, data.get('controller_ip'), True)
        #customer_obj = customerHandler.get_customer(installation_obj.get('customer'))
        print("Sending alarm mail..")
        #mailHandler.send_alarm_mail(data, installation_obj, controller_obj, customer_obj)
    return log_dao.create_log_entry(data, installation)


def get_alarms_customer(customer):
    installations = installationHandler.get_by_customer(customer.get('id'))
    alarms = 0
    if installations:
        for installation in installations:
            alarms += get_alarms_installation(installation)
    return alarms


def get_warnings_customer(customer):
    installations = installationHandler.get_by_customer(customer.get('id'))
    warnings = 0
    if installations:
        for installation in installations:
            warnings += get_warnings_installation(installation)
    return warnings


def get_alarms_installation(installation):
    alarm_tags = tagHandler.get_tags_by_type(installation.get('serial_number'), 'alarm')
    if alarm_tags:
        return len(get_matching_values_for(alarm_tags, 1))
    return 0


def get_warnings_installation(installation):
    warning_tags = tagHandler.get_tags_by_type(installation.get('serial_number'), 'warning')
    if warning_tags:
        return len(get_matching_values_for(warning_tags, 1))
    return 0


def get_warnings_controller(controller):
    warning_tags = tagHandler.get_tags_by_type(controller.get('installation'), 'warning', controller.get('ip'))
    if warning_tags:
        return len(get_matching_values_for(warning_tags, 1))
    return 0


def get_alarms_controller(controller):
    alarm_tags = tagHandler.get_tags_by_type(controller.get('installation'), 'alarm', controller.get('ip'))
    if alarm_tags:
        return len(get_matching_values_for(alarm_tags, 1))
    return 0


def get_matching_values_for(tags, value):
    return [tag for tag in tags if tag.get('value') == str(value)]