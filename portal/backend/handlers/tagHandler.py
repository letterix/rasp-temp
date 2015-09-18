
from sync import sync_methods
from handlers import syncHandler, controllerHandler
from dao import tag_dao


def delete(serial_number, controller_ip, name):
    res = None
    tag = get_tag_by_name(serial_number, controller_ip, name)
    if tag:
        res = tag_dao.delete_tag(serial_number, controller_ip, name)
    if res:
        print('Deleted a tag with name: ' + name)
        sync = {}
        sync['installation'] = tag['installation']
        sync['method'] = sync_methods.DELETE
        sync['table'] = 'tags'
        sync['data'] = tag
        sync['prev'] = None
        res = syncHandler.insert(sync)
    return res


def insert(tag, debug=False):
    res = None
    controller = controllerHandler.get_controller(tag.get('installation'), tag.get('controller_ip'))
    current_tag = tag_dao.get(tag.get('installation'), tag.get('controller_ip'), tag.get('name'))
    if controller and not current_tag:
        res = tag_dao.create_tag(tag)
    if res and not debug:
        print('Inserted new tag with name: ' + tag['name'])
        sync = {}
        sync['installation'] = tag['installation']
        sync['method'] = sync_methods.INSERT
        sync['table'] = 'tags'
        sync['data'] = tag
        sync['prev'] = None
        res = syncHandler.insert(sync)
    return res


def update(tag):
    res = False
    current_tag = get_tag_by_name(tag.get('installation'), tag.get('controller_ip'), tag.get('name'))
    if current_tag and current_tag != tag:
        res = tag_dao.update_tag(tag)
    if res:
        print('Updated tag with name: ' + tag['name'])
        sync = {}
        sync['installation'] = tag['installation']
        sync['method'] = sync_methods.UPDATE
        sync['table'] = 'tags'
        sync['data'] = tag
        sync['prev'] = None
        res = syncHandler.insert(sync)
    return res



def get_tag_by_name(serial_number, controller_ip, name):
    res = None
    controller = controllerHandler.get_controller(serial_number, controller_ip)
    if controller:
        res = tag_dao.get(serial_number, controller_ip, name)
    return res


def get_tags(serial_number, controller_ip):
    res = None
    if controllerHandler.get_controller(serial_number, controller_ip):
        res = tag_dao.get_all(serial_number, controller_ip)
    return res

def get_tags_by_type(serial_number, tag_type, controller_ip=None):
    res = None
    if controllerHandler.get_controllers(serial_number):
        if controller_ip:
            res = tag_dao.get_by_controller_and_type(serial_number, controller_ip, tag_type)
        else:
            res = tag_dao.get_by_installation_and_type(serial_number, tag_type)
    return res
