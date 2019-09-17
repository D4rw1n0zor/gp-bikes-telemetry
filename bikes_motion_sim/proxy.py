# -*- coding: utf-8 -*-

import re

from errors import ConfigError
from simulator import Simulator
from tools import Logger, read_ini_file

from configparser import ConfigParser
from typing import List, Dict, Any, Optional

log = Logger(__name__)


class Proxy(object):
  _config: Optional[ConfigParser]
  simulators: List[Simulator]

  def __init__(self, config_file=None):
    self._config = read_ini_file(config_file) if config_file else None
    self.simulators = self._create_simulators(self._config)
    self._data_input_driver, self._data_output_drivers = self._get_driver_types(self.simulators)

  def _blocking_event_loop(self, input_driver, output_drivers):
    log.debug('Blocking event-loop started.')

    try:
      for input_data in input_driver.data_output:
        print(input_data)
        output_data = input_data

        for driver in output_drivers:
          driver.input_data(output_data)

    except KeyboardInterrupt:
      return

  def _get_driver_types(self, simulators):
    data_input_drivers = None
    data_output_drivers = []

    for simulator in simulators:
      for driver in simulator.drivers:
        if hasattr(driver, 'data_output'):
          data_input_drivers = driver

        if hasattr(driver, 'data_input'):
          data_output_drivers.append(driver)

    return data_input_drivers, data_output_drivers

  @staticmethod
  def _create_simulators(config: ConfigParser) -> List[Simulator]:
    simulators = []

    for section in config.sections():
      if not config.has_option(section, 'drivers'):
        msg = f'Config-file section \'{section}\' does not have an option \'drivers\'.'
        raise(ConfigError(msg))

      drivers_list = config.get(section, 'drivers').split(',')
      driver_parameters: Dict[str, Any] = {}
      simulator = Simulator()

      for driver_name in drivers_list:
        simulator.add_driver(driver_name, driver_parameters)

      for option in config.options(section):
        for driver_name in drivers_list:
          if re.match(rf'{driver_name}_', option):
            key = re.search(f'{driver_name}_(.*)', option)[1]
            value = config.get(section, option)
            driver_parameters[key] = value

      simulators.append(simulator)
      log.debug(f'Simulator created for: {section}')

    return simulators

  def start_simulators(self) -> None:
    for simulator in self.simulators:
      simulator.start_all_drivers()

    self._blocking_event_loop(self._data_input_driver, self._data_output_drivers)
