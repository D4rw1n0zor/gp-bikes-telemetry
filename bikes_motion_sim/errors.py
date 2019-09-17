
def get_error_classes():
  print(dir(self))

class BaseException(Exception):
  """Base Exception Handler"""

class ConfigError(BaseException):
  """Excpetion when there are errors occruing in the config-object"""

class DriverError(BaseException):
  """Excpetion when there are errors occruing during run of a driver"""

class ModuleImportError(BaseException):
  """Excpetion when there are errors dynamically importing modules"""