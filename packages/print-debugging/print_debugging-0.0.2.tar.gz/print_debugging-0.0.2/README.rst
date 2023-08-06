Debug and Release the code with same code
=========================================

Do not use print for debugging and delete print for release

Example Usage
-------------
::

  from printDebugging import *
  setLevel(DEBUG) # or setLevel("DEBUG")
  debug("hi")     # printed out
  setLevel(QUIET) # set debug level into QUIET
  debug("hi")     # not printed out

  # Configure Color
  set_color("purple", INFO)         # set foreground color as purple  for info
  set_color("WHITE", WARN, "bg")    # set backgournd color as white for warn
  add_style("underline", DEBUG)
  reset_style(WARN)
  reset_style()

  # Configure Prefix
  setLevel(INFO)
  set_prefixes("{trace}", INFO)   # Add string as prefix for INFO
  info("HI")                      # FileName with Line number is printed out as prefix
  import datetime
  set_prefixes(datetime.datetime.now) # Add function with no parameter as prefix
  info("hello")                   # Result of `datetime.datetime.now()` is printed out as prefix

  # Configure postfix
  import traceback
  set_postfixes(traceback.format_exc, ERROR)
  try:
    0 / 0
  except:
    error("Expected Error")             # traceback is printed out

Debug Level
-----------
- QUIET : DO NOT PRINT EXCEPT "error"
- INFO  : Print info and error
- VERBOSE : Print info, warn and error
- DEBUG : print info, warn, error and debug

TO DO
-----
Add function with arugment as prefix or postfix