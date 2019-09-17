# -*- coding: utf-8 -*-

# import bikes_motion_sim.errors
import re

import proxy
import errors

from inspect import getsourcefile
from os.path import abspath, join

EXEC_PATH = re.sub('/[^/]*$', '', abspath(getsourcefile(lambda: 0)))
CONFIG_FILE = join(EXEC_PATH, 'dummy_config.ini')


def main():

  # print(dir(errors))
  #
  # error_objects = []
  # module = errors
  # for name in dir(module):
  #   obj = getattr(module, name)
  #   if isclass(obj):
  #     error_objects.append(name)
  #
  # error_objects = tuple(error_objects)
  # print(error_objects)

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
