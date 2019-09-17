# -*- coding: utf-8 -*-

from abstracts import Drivers

DRIVER_NAME = 'display_stats'


class Driver(Drivers):
  def __init__(self, instance, driver_parameters=None) -> None:
    super().__init__(instance, DRIVER_NAME, driver_parameters)
    self.console_printer = ConsoleOutput()
    self.data_input = None

  def start(self):
    pass

class ConsoleOutput(object):
  text_to_print: list

  def __init__(self):
    self.text_to_print = []
