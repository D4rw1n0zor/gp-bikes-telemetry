# -*- coding: utf-8 -*-

import re

import proxy
import errors
from inspect import getsourcefile
from os.path import abspath, join

EXEC_PATH = re.sub('/[^/]*$', '', abspath(getsourcefile(lambda: 0)))
CONFIG_FILE = join(EXEC_PATH, 'config.ini')


def main():
  error_objects = (errors.BaseException,
                   errors.ConfigError,
                   errors.ModuleImportError,
                   errors.DriverError
                   )

  try:
    bms = proxy.Proxy(CONFIG_FILE)

  except error_objects as e:
    print(f'Error: {e}')
    return

  bms.start_simulators()

if __name__ == '__main__':
  main()
