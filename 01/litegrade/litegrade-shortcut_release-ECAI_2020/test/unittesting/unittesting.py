#!/usr/bin/python

import inspect
import os

def my_assert(a, b):
	if a != b:
		frame = inspect.stack()[1]
		#caller_file_name = os.path.basename(frame.filename)
		caller_file_name = frame.filename
		caller_line_num = inspect.getframeinfo(inspect.stack()[1][0]).lineno
		print("\n"+"-"*15)
		print("file: "+str(caller_file_name))
		print("line: "+str(caller_line_num))
		print(a)
		print(" !=")
		print(b)
		print("-"*15+"\n")
