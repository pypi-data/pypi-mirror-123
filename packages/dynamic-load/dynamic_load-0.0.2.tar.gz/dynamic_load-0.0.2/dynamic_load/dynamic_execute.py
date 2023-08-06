from .dynamic_load import *

def dynamic_execute(function : str, *args, **kwargs):
  func = dynamic_load(function)
  return func(*args, **kwargs)

def safe_dynamic_execute(function : str, *args, **kwargs):
  try:
    func = dynamic_load(function)
    func(*args, **kwargs)
  except CannotResolve:
    return None
