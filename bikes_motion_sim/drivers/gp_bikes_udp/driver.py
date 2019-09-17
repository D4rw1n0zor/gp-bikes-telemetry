# -*- coding: utf-8 -*-

import socket
import struct

from constants import DRIVERS_PATH
from abstracts import Drivers
from errors import DriverError
from tools import Logger, read_json_file

from os.path import join
from typing import Union, List

DRIVER_NAME: str = 'gp_bikes_udp'

DEFAULT_UDP_IP: str = '127.0.0.1'
DEFAULT_UDP_PORT: int = 30001
DEFAULT_UDP_BUFFERSIZE: int = 880
JSON_STRUCT_FILE: Union[bytes, str] = join(DRIVERS_PATH, 'gp_bikes_udp', 'struct.json')
KEYS: List[str] = [ 'byte_index', 'short_name', 'type', 'description', 'matrix_group' ]

log = Logger(__name__)

class Driver(Drivers):
  def __init__(self, instance, driver_parameters=None) -> None:
    super().__init__(instance, DRIVER_NAME, driver_parameters)
    log.debug(f'Driver parameters for \'{DRIVER_NAME}\': {", ".join(driver_parameters)}')
    self.udp_importer = UDP_Importer(driver_parameters)

  def data_input(self):
    pass

  def start(self):
    self.udp_importer.udpserver.start()

class UDP_Importer(object):
  def __init__(self, parameters=None):
    ip = str(parameters['ip']) if 'ip' in parameters else DEFAULT_UDP_IP
    port = int(parameters['port']) if 'port' in parameters else DEFAULT_UDP_PORT
    buffersize = int(parameters['buffersize']) if 'buffersize' in parameters else DEFAULT_UDP_BUFFERSIZE
    self._blueprint = read_json_file(JSON_STRUCT_FILE)
    self.udpserver = UDPServer(ip, port, buffersize)

  def _unpack_packet(self, raw_packet):
    # When GP-bikes is outside of simulation (like in one of it's menu's)
    if struct.unpack_from('i', raw_packet, offset=4)[0] == 0:
      return None

    # TODO: finish method

  def packet(self):
    raw_packet = self.udpserver.get_packet()
    yield self._unpack_packet(raw_packet)

class UDPServer(object):
  def __init__(self, ip, port, buffer_size):
    self._buffersize = buffer_size
    self._ip = ip
    self._port = port
    self._UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def start(self):
    port_not_bound = True

    while port_not_bound == True:
      try:
        self._UDPClientSocket.bind((self._ip, self._port))

      except OSError as e:
        if e.errno == 98:
          self._port += 1

        else:
          msg = (DriverError(f'{__name__}: {e}'))
          raise(DriverError(msg))

      port_not_bound = False

    log.debug(f'UDP Server started: {self._ip}:{self._port}')
    print(f'UDP Server on: {self._ip}:{self._port}')

  def get_packet(self):
    return self._UDPClientSocket.recvfrom(self._buffersize)[0]