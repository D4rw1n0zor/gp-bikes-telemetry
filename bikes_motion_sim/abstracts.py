# -*- coding: utf-8 -*-

from tools import Logger
from abc import ABCMeta

log = Logger(__name__)


class Drivers(metaclass=ABCMeta):
  def __init__(self, instance: object, driver_name: str, driver_parameters=None) -> None:
    self.driver_name = driver_name
    self.driver_parameters = driver_parameters
    self.channel = instance

    log.debug(f'Driver Initialized: {self.driver_name}')

  def start(self):
    pass

  def stop(self):
    pass