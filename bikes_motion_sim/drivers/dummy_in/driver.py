# -*- coding: utf-8 -*-

from abstracts import Drivers

from time import sleep

DRIVER_NAME = 'dummy_in'

class Driver(Drivers):
  def __init__(self, instance, driver_parameters=None) -> None:
    super().__init__(instance, DRIVER_NAME, driver_parameters)
    self.dummy = Dummy()
    self.data_output = None

  def start(self):
    self.data_output = self.dummy.output_generator()

class Dummy(object):
  def output_generator(self):
    while True:
      for i in range(100):
        for j in sorted([n for n in range(100)], reverse=True):
          yield {'test1': i, 'test2': j}
          sleep(0.05)

