# -*- coding: utf-8 -*-

from constants import DRIVERS_PATH
from errors import ConfigError
from tools import Logger, dynamic_module_importer

from os import listdir
from os.path import isdir, join
from typing import Optional

DRIVERS_FOLDERS = [f for f in listdir(DRIVERS_PATH) if isdir(join(DRIVERS_PATH, f))]

log = Logger(__name__)


class Simulator(object):
  def __init__(self) -> None:
    self.drivers = []
    self.data_input = []

  def add_driver(self, driver_name: str, driver_parameters: Optional[dict] = None) -> None:
    if driver_name.lower() in DRIVERS_FOLDERS:
      driver_module = dynamic_module_importer(driver_name.lower())
      driver_module = driver_module.driver.Driver(self, driver_parameters)
      self.drivers.append(driver_module)

      log.debug(f'Simulator has driver attached: {driver_name}')

    else:
      raise(ConfigError(f'{driver_name} does not exist as a driver in the drivers-folder \'{DRIVERS_PATH}\' .'))

  def start_driver(self, driver_id):
    self.drivers[driver_id].start()

  def start_all_drivers(self):
    if len(self.drivers) == 1:
      self.start_driver(0)

    else:
      for i in range(len(self.drivers) - 1):
        self.start_driver(i)

  def stop_driver(self):
    pass
