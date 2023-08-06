import importlib
from .tail_recursive import *
class CannotResolve(Exception):
  def __init__(self, inputname : str):
    self.msg = "Cannot resolve any module from {}".format(inputname)
  def __str__(self):
    return self.msg

def dynamic_load(string : str) :
  @tail_call_optimized
  def load_module(target : str, remained : list = list()) :
    try:
      module = importlib.import_module(target)
      return (module, remained)
    except ModuleNotFoundError:
      return load_module(target=".".join(target.split(".")[:-1]), remained=[target.split(".")[-1]] + remained)
    except ValueError:
      raise CannotResolve(string) from None
  module, last = load_module(string)
  for each in last:
    module = getattr(module, each)
  return module

def safe_dynamic_load(string : str):
  try:
    return dynamic_load(string)
  except CannotResolve:
    return None