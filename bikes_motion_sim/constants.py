# -*- coding: utf-8 -*-

import re

from inspect import getsourcefile
from os.path import abspath, join

EXEC_PATH = re.sub('/[^/]*$', '',  abspath(getsourcefile(lambda:0)))
DRIVERS_PATH = join(EXEC_PATH, 'drivers')