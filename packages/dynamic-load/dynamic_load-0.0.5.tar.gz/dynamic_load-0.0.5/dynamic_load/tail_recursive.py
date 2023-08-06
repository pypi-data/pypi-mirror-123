# From https://code.activestate.com/recipes/474088-tail-call-optimization-decorator/
import sys
import inspect
class TailRecurseException(Exception):
  def __init__(self, args, kwargs):
    self.args = args
    self.kwargs = kwargs

class NotTailRecursive(Exception):
  def __init__(self, g):
    self.msg = "Function {} is not tail recursive".format(g)
  def __str__(self):
    return self.msg
def tail_call_optimized(g):
  name = g.__name__
  sources = [x for x in inspect.getsource(g).split("\n") if "return" in x]
  for each in sources:
    x = each.count(name)
    if x > 1:
      raise NotTailRecursive(name)
  """
  This function decorates a function with tail call
  optimization. It does this by throwing an exception
  if it is it's own grandparent, and catching such
  exceptions to fake the tail call optimization.

  This function fails if the decorated
  function recurses in a non-tail context.
  """
  def func(*args, **kwargs):
    f = sys._getframe()
    if f.f_back and f.f_back.f_back \
        and f.f_back.f_back.f_code == f.f_code:
      raise TailRecurseException(args, kwargs)
    else:
      while 1:
        try:
          return g(*args, **kwargs)
        except TailRecurseException as e:
          args = e.args
          kwargs = e.kwargs
  func.__doc__ = g.__doc__
  return func