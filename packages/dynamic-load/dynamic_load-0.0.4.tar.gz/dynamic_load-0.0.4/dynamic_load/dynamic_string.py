import inspect
import re
from .tail_recursive import *

def dynamic_string(f):
  if(inspect.isbuiltin(f)):
    name = f.__name__
    def helper(string : str) -> str:
      @tail_call_optimized
      def recursive(str1):
        p = re.compile(f"[a-z|A-Z]*\((.*{name}.*)\)")
        functionName = p.findall(str1)
        if len(functionName) == 0:
          return str1
        else:
          return recursive(functionName[0])
      return recursive(string).replace("\"","")

    @tail_call_optimized
    def recursive(frame):
      if f".{name}" in inspect.getframeinfo(frame).code_context[0]:
        return helper(inspect.getframeinfo(frame).code_context[0].replace("\n",""))
      else:
        return recursive(frame.f_back)
    return recursive(inspect.currentframe())
  else:
    return f"{f.__module__}.{f.__name__}"
