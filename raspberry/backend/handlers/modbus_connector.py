
from dao import tag_dao
from handlers.ModbusHandler import ModbusHandler

handler = ModbusHandler()

def get_value(tag):
    address = tag['address']
    ip = tag['controller_ip']
    return handler.execute_read_parameter(address, ip)


def set_value(parameter, value):
    """not implemented"""
    pass

