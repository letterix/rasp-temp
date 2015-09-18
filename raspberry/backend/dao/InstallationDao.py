import backend
from dao.base_dao import r_server

def get():
    installations = r_server.smembers('installations')
    if installations:
        installation = {}
        installation['serial_number'] = installations.pop()
        installation['model'] = r_server.hget('installation:%s' % installation['serial_number'], 'model')
        return installation
    return {}

def create(serial_number, model):
    if r_server.sadd('installations', serial_number):
        return r_server.hset('installation:%s' % serial_number, 'model', model)
    return False