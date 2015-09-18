#!/usr/bin/python
# -*- coding: utf-8 -*-
from modbus_tcp.modbus_tcp import ModbusTcp
import re, threading

global LOCK
LOCK = threading.Lock()
_READ_COMMAND = 'READ'
_WRITE_COMMAND = 'WRITE'

class ModbusHandler:

    def __init__(self):
        pass

    _COMMAND_GET_PARAMETER = 0x90
    _COMMAND_SET_PARAMETER = 0x91

    _GET_PARAMETER_REQUEST = '>BBxx'
    _GET_PARAMETER_RESPONSE = '>BBh'
    _SET_PARAMETER_REQUEST = '>BBh'

    _HOLDING_REGISTERS_TAG = '%MW'

    _IP_ADDRESS = ''

    #----------------------------------------------------------------------------------------


    #Toplevel method for executing a read command
    def execute_read_parameter(self, address, controller_ip, num_addresses = 1):
        self._IP_ADDRESS = controller_ip
        bit = self._extract_bit_address(address)
        result = None
        if address.startswith(self._HOLDING_REGISTERS_TAG):
            result = self._read_holding_registers(self._extract_address(address), num_addresses)
        return self._extract_result(result, bit)

    #Submethod for second layer methods (2)
    def _read_holding_registers(self, start_address, num_addresses):
        client = ModbusTcp(self._IP_ADDRESS)
        result = client.read_holding_registers(start_address, num_addresses)
        return result[0]

    #Submethod for third layer methods (3)
    def _extract_result(self, value, bit):
        if bit is None:
            return value
        else:
            return self._value_of_16bit(value, bit)

    #Helper method for reading the value of a bit in a 16-bit byte
    def _value_of_16bit(self, value, bit):
        value_set = False
        if 0 <= bit <= 15:
            value_set = ((value & (1 << bit)) != 0)
        if value_set:
            return 1
        else:
            return 0

    #Returns the address from a tag
    def _extract_address(self, tag):
        numbers = re.findall(r'\d+', tag)
        return int(numbers[0])

    #Helper method that returns the bit-tag from an address-tag.
    def _extract_bit_address(self, tag):
        result = None
        numbers = re.findall(r'\d+', tag)
        if(len(numbers) == 2):
            result = int(numbers[1])
        return result
