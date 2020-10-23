#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

# commondriver.py 
#   This script contains functions that are to be used in multiple scripts
#   of the litegrade module

import os
import sys
import inspect

msg_prefix = "litegrade"

def print_err(msg, **kwargs):
	frame = inspect.stack()[1]
	caller_line_num = inspect.getframeinfo(inspect.stack()[1][0]).lineno
	sys.stderr.write(f"{msg_prefix}: (line {caller_line_num}) {msg}\n")

	callback = kwargs.get("callback", None)
	if callback != None:
		callback()

def safe_fopen(fname, mode):
	if not os.path.isfile(fname):
		print_err(f"'{fname}' not found", callback=lambda: exit(1))

	try:
		fobj = open(fname, mode=mode)
	except OSError as err:
		print_err(f"'{fname}' open error")
		print_err(f"(OS error below)\n{err}", callback=lambda: exit(1))

	return fobj



