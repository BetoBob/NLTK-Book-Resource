#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

# modulemanager.py 
#   This script manages all needed modules for litegrade.py, to increase 
#   organization and reduce import overhead

import requests

def hand_in_assignment(assignment_name, student_obj):
	assignment_obj = {
		"assignment_name": assignment_name,
		"student": student_obj
	}
	post_obj = {
		"objective": "hand_in",
		"assignment":assignment_obj
	}

	url = 'https://www.justinleemorgan.com/ecai2020/studentapi'
	res = requests.post(url, json = post_obj)
	print(res.text)
