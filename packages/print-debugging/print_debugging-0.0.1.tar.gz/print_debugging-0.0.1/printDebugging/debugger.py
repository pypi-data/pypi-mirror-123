import datetime
import inspect
import traceback
import json
import os
from colors import *
from collections.abc import Iterable
from dynamic_load import *
# LEVELS
DEBUG = 30
VERBOSE = 20
INFO = 10
QUIET = 0

#PRINT
WARN=25
ERROR=0

_levelToName = {
    DEBUG: 'DEBUG',
    VERBOSE: 'VERBOSE',
    INFO: 'INFO',
    QUIET: 'QUIET'
}

_nameToLevel = {
  "DEBUG" : DEBUG,
  "VERBOSE" : VERBOSE,
  "INFO" : INFO,
  "QUIET" : QUIET
}

_printLevel = {
  DEBUG : DEBUG,
  INFO : INFO,
  WARN : VERBOSE,
  ERROR : QUIET
}

_print2Name = {
  DEBUG : "DEBUG",
  INFO : "INFO",
  WARN : "WARN",
  ERROR : "ERROR"
}

_name2Print = {
  "DEBUG" : DEBUG,
  "INFO" : INFO,
  "WARN" : WARN,
  "ERROR" : ERROR
}

_LEVEL = QUIET
def setLevel(level) -> None:
  global _LEVEL
  if type(level) == str:
    _LEVEL = _nameToLevel[level]
  elif type(level) == int and level in _levelToName.keys():
    _LEVEL = level

def getLevel() -> str:
  return _levelToName[_LEVEL]

_data = {
  "INFO" : {
    "ansi" : {
      "fg" : "GREEN",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  },
  "WARN" : {
    "ansi" : {
      "fg" : "YELLOW",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  },
  "ERROR" : {
    "ansi" : {
      "fg" : "RED",
      "bg" : "",
      "style" : []
    },
    "prefixes" : [],
    "postfixes" : []
  },
  "DEBUG" : {
    "ansi" : {
      "fg" : "BLUE",
      "bg" : "",
      "style" : []
    },
    "prefixes" : [],
    "postfixes" : []
  }
}

DEFAULTMAP = {
  "INFO" : {
    "ansi" : {
      "fg" : "GREEN",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  },
  "WARN" : {
    "ansi" : {
      "fg" : "YELLOW",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  },
  "ERROR" : {
    "ansi" : {
      "fg" : "RED",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  },
  "DEBUG" : {
    "ansi" : {
      "fg" : "BLUE",
      "bg" : "",
      "style" : []
    },
    "prefixes" : ["{inspect}"],
    "postfixes" : []
  }
}

def setDefault()-> None:
  global _data
  _data = DEFAULTMAP
def saveConfigure(path : str = ".debug-setting.json") -> None:
  with open(path, "w") as f:
    json.dump(_data, f, indent=4)
def loadConfigure(path : str = ".debug-setting.json") -> None:
  if os.path.isfile(path):
    with open(path) as f:
      data = json.load(f)
    for each in data:
      _data[each] = data[each]
loadConfigure()

def set_color(c : str, lvl, tg = "fg") -> None:
  if type(lvl) == int:
    lvl = _print2Name[lvl]
  if tg == "style":
    c = c.split("+")
  _data[lvl]["ansi"][tg] = c
def add_style(c : str, lvl) -> None:
  if type(lvl) == int:
    lvl = _print2Name[lvl]
  _data[lvl]["ansi"]["style"] = _data[lvl]["ansi"]["style"] + c.split("+")

def reset_style(lvl = None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    _data[lvl]["ansi"]["style"] = []
  else:
    for each in _data.keys():
      _data[each]["ansi"]["style"] = []
def reset_background(lvl = None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    _data[lvl]["ansi"]["bg"] = ""
  else:
    for each in _data.keys():
      _data[each]["ansi"]["bg"] = ""

def add_prefixes(c, lvl=None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    if type(c) != list:
      c = [c]
    c = [each if not callable(c) else "function://{}".format(dynamic_string(c)) for each in c]
    _data[lvl]["prefixes"] = _data[lvl]["prefixes"] + c
  else:
    for each in _data.keys():
      add_prefixes(c, each)

def reset_prefixes(lvl=None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    _data[lvl]["prefixes"] = []
  else:
    for each in _data.keys():
      reset_prefixes(each)
def set_prefixes(c, lvl = None)-> None:
  reset_prefixes(lvl)
  add_prefixes(c, lvl)

def add_postfixes(c, lvl=None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    if type(c) != list:
      c = [c]
    c = [each if not callable(each) else "function://{}".format(dynamic_string(each)).split(",")[0] for each in c]
    _data[lvl]["postfixes"] = _data[lvl]["postfixes"] + c
  else:
    for each in _data.keys():
      add_postfixes(c, each)

def reset_postfixes(lvl=None) -> None:
  if lvl != None:
    if type(lvl) == int:
      lvl = _print2Name[lvl]
    _data[lvl]["postfixes"] = []
  else:
    for each in _data.keys():
      reset_postfixes(each)

def set_postfixes(c, lvl = None)-> None:
  reset_postfixes(lvl)
  add_postfixes(c, lvl)

def printHelper(text : str) -> None:
  level = _name2Print[inspect.getframeinfo(inspect.currentframe().f_back).function.upper()]
  if _LEVEL < _printLevel[level]:
    return None
  level = _print2Name[level]
  prefixed = []
  for each in _data[level]["prefixes"]:
    if callable(each):
      prefixed.append(str(each()))
    elif each.startswith("function://"):
      prefixed.append(str(dynamic_execute(each.replace("function://",""))))
    else:
      prefixed.append(str(each))
  postfixed = []
  for each in _data[level]["postfixes"]:
    if callable(each):
      postfixed.append(str(each()))
    elif each.startswith("function://"):
      postfixed.append(str(dynamic_execute(each.replace("function://",""))))
    else:
      postfixed.append(str(each))
  messageFormat = [x for x in [" ".join(prefixed), text, " ".join(postfixed)] if x != ""]
  message = ": ".join(messageFormat)
  frame = inspect.getframeinfo(inspect.currentframe().f_back.f_back)
  message = message.replace("{level}", level)
  message = message.replace("{inspect}", "{}:{}".format(frame.filename,frame.lineno))
  message = message.replace("{datetime}", str(datetime.datetime.now()))
  message = message.replace("{trace}", traceback.format_exc().rstrip("\n"))
  message = message.rstrip("\n")
  print(color(message, bg=_data[level]["ansi"]["bg"].lower(), style="+".join(_data[level]["ansi"]["style"]).lower(),fg=_data[level]["ansi"]["fg"].lower()))

def intoString(args) -> str:
  converted = []
  for each in args:
    if callable(each):
      converted.append(str(each()))
    else:
      converted.append(each)
  return " ".join(converted)

def debug(*args) -> None:
  printHelper(intoString(args))
def error(*args) -> None:
  printHelper(intoString(args))
def warn(*args) -> None:
    printHelper(intoString(args))
def info(*args) -> None:
    printHelper(intoString(args))

# #   def test(cls, target = True, expected = None, method = "==", text: str = ""):
# #     if type(target) != bool and expected != None:
# #       if method == "!=" or method.startswith("dif"):
# #         method = "!="
# #         condition = target != expected
# #       elif method == "in":
# #         try:
# #           condition = expected in target
# #         except TypeError:
# #           condition = None
# #           debug.error(f"target {target} is type of {type(target)}, which is not iterable")
# #       else:
# #         condition = target == expected
# #       text = f"{text} =>" if text != "" else f"Testing {target} {method} {expected} =>"
# #     else:
# #       condition = target
# #       text = "" if text == "" else f"{text} "
# #       text = f"Simple Testing : {text}=>"
# #     if condition != None:
# #       answer = "True" if condition else "False"
# #       cls.debug(f"{text} {answer}")