#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

# litegrade.py 
#   This script contains student-interfacing functions that can be seen at the 
#   notebook level

import json

from importlib import reload
import modulemanager
modulemanager = reload(modulemanager)
from modulemanager import \
	print_err, \
	safe_fopen, \
	hello_from_qdriver, \
	get_nested_value, \
	hand_in_assignment

def load_questions(json_fname):

	questions_fobj = safe_fopen("questions.json", 'r')

	try:
		questions_obj = json.load(questions_fobj)
	except OSError as err:
		print_err(f"{msg_prefix}: '{fname}' json load error")
		print_err(f"(OS error below)\n{err}", callback=lambda: exit(1))

	return questions_obj

def get_input(msg, valid_inputs_list):
	user_input = input(msg)
	while not user_input:
		print("  Please enter something")
		user_input = input(msg)
	
	if not valid_inputs_list:
		return user_input

	lower_valid_inputs_list = [x.lower() for x in valid_inputs_list]
	while user_input.lower() not in lower_valid_inputs_list:
		print(f"  '{user_input}' is not a valid input")
		print(f"  valid inputs include {valid_inputs_list}")
		user_input = input(msg)

	return user_input

def mutate_question(questions_obj):
	hello_from_qdriver({},[questions_obj])

def hello_from_litegrade():
	print("hello from litegrade function")

def init_student(assignment_name):
	print("Please enter your name below")
	first_name = get_input("First Name: ", [])
	last_name = get_input("Last Name: ", [])
	id_number = "" #input("ID Number: ")
	student_obj = {
		"name": {
			"first": first_name,
			"last": last_name},
		"id": id_number,
		"assignment": assignment_name, #questions_obj}#init_assignment(assignment_name)}
		"questions": load_questions("questions.json"),
		"student_answers": []
	}
	return student_obj

def begin(assignment_name):
	student_obj = init_student(assignment_name)
	return student_obj

def print_question(question_type, prompt, choices, choices_labels):

	if question_type == "true-or-false":
		print(f"{prompt}")
		return get_input("Please enter your answer:\n  ", choices_labels)

	print(f"{prompt}")
	choice_num = 0
	for choice in choices:
		description = get_nested_value(["description"], choice)
		choice_label = choices_labels[choice_num]
		print(f"  {choice_label}) {description}")
		choice_num += 1
	return get_input("Please enter your answer:\n  ", choices_labels)

def get_choices_labels(question_type, number_of_choices):
	letters = ['A','B','C','D','E','F','G','H']

	choices_labels = [None] * number_of_choices
	if question_type == "multiple-choice":
		for choice_num in range(number_of_choices):
			choices_labels[choice_num] = letters[choice_num]
	if question_type == "true-or-false":
		choices_labels = ["true","false","t","f"]
	
	return choices_labels

def record_student_answer(question_name, student_answer, student_obj):
	student_answers = get_nested_value(["student_answers"], student_obj)
	student_answers.append([question_name, student_answer])
	
def ask(student_obj, question_name):
	questions = get_nested_value(["questions"], student_obj)
	question = get_nested_value( \
		["questions", question_name], questions)

	prompt = get_nested_value(["prompt"], question)
	choices = get_nested_value(["choices"], question)
	question_type = get_nested_value(["question_type"], question)
	choices_labels = get_choices_labels(question_type, len(choices))

	student_answer = \
		print_question(question_type, prompt, choices, choices_labels)
	correct_answer_index = get_nested_value(["correct_choice"], question)
	correct_answer = choices_labels[correct_answer_index]

	# hotfix
	if question_type == "true-or-false":
		correct_answer = "t" if correct_answer_index == 0 else "f"
	
	if correct_answer.lower() in student_answer.lower():
		print(f"'{student_answer}' is correct!")
	else:
		print(f"  '{student_answer}' is incorrect\n")
		ask(student_obj, question_name)
		return
		#student_try_again_answer = \
		#	get_input(f"'{student_answer}' is incorrect. " \
		#		"Would like to give it another try? (y or n)\n  ", \
		#		["yes", "y", "no", "n"])
		#if "y" in student_try_again_answer:
		#	print(" ")
		#	ask(student_obj, question_name)
		#	return

	record_student_answer(question_name, student_answer, student_obj)

def handin(assignment_name, student_obj):
	hand_in_assignment(assignment_name, student_obj)
	










