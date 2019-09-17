# -*- coding: utf-8 -*-

import logging

from errors import ModuleImportError

from configparser import ConfigParser, MissingSectionHeaderError, ParsingError
from importlib import import_module
from json import load

LOG_FORMAT: str = '\x1b[37m--- %(levelname)s ---\x1b[0m %(asctime)s - %(name)s\n  %(message)s'


def dynamic_module_importer(module):

  try:
    module = import_module(f'drivers.{module}')

  except ModuleNotFoundError as e:
    print(e)
    raise ModuleImportError

  return module


def read_ini_file(config_file: str) -> ConfigParser:
  """

  :rtype: ConfigParser
  :type config_file: dict
  """
  log.debug(f'Reading config: {config_file}')

  ini: ConfigParser = ConfigParser()

  try:
    ini.read(config_file)

  except MissingSectionHeaderError as e:
    print(f'Error in file {config_file}: Option without Section')
    print(f'Error description: {e}')
    raise

  except ParsingError as e:
    print(f'Error in file {config_file}: Parsing error')
    print(f'Error description: {e}')
    raise

  return ini


def read_json_file(filename):
  try:
    with open(filename, 'r') as fd:
      data_dict = load(fd)
    fd.close()

  except:
    raise(BaseException('Test'))

  return data_dict


class Logger(object):
  def __init__(self, module_name: str) -> None:
    self.module_name = module_name
    self.log = logging.getLogger(module_name)
    console_debug = logging.StreamHandler()
    console_debug.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    console_debug.setFormatter(formatter)
    self.log.addHandler(console_debug)

    self.log.setLevel(logging.DEBUG)
    self.log.debug(f'Debug Logger initialized for: {self.module_name}')

  def debug(self, msg: str) -> None:
    self.log.debug(msg)


log = Logger(__name__)
