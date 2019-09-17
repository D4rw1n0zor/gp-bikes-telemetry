# -*- coding: utf-8 -*-

import logging

from .constants import EXEC_PATH

try:
  from logging import NullHandler

except ImportError:
  class NullHandler(logging.Handler):
    def emit(self, record):
      pass

logging.getLogger(__name__).addHandler(NullHandler())
