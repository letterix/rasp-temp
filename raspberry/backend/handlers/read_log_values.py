from handlers import installationHandler
from handlers import modbus_connector
from dao import sync_queue_dao, tag_dao
import datetime
import json
import logging
import traceback


LOG = logging.getLogger()

def read_all_parameters():
    print("Reading log entries")
    try:
        _read_all_parameters_internal()
    except:
        LOG.error("Failed to read values from modbus device!")
        traceback.print_exc()

def _read_all_parameters_internal():
    current_installation = installationHandler.get_installation()
    now = datetime.datetime.now()
    tags = tag_dao.get_tags()
    num_logs_read = 0
    for tag in tags:
        #current_value = modbus_connector.get_value(tag)

        log_item = {
            'name': tag['name'],
            'controller_ip': tag['controller_ip'],
            'value': 666,
            'time': now,
            'address': tag['address'],
            'type': tag['type']
        }
        log_entries = sync_queue_dao.select_data_like(log_item.get('name'), log_item.get('controller_ip'))
        for log_entry in log_entries:
            data = json.loads(log_entry.get('data'))
            if data.get('name') == log_item.get('name'):
                if data.get('controller_ip') == log_item.get('controller_ip'):
                    sync_queue_dao.delete(log_entry.get('id'), current_installation.get('serial_number'))

        num_logs_read += sync_queue_dao.insert_params(current_installation.get('serial_number'), 'log', 'insert', log_item)

    print('Added %s tags to sync.' % (num_logs_read,))

if __name__ == "__main__":
    read_all_parameters()
