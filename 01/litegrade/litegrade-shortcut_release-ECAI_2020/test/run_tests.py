#!/home/jmorga27/Cal_Poly/Kurfess/litegrade/bin/python3

dir_of_code_to_test = "/home/jmorga27/Cal_Poly/Kurfess/litegrade/src"

import os
import sys

#sys.path.insert(1, dir_of_code_to_test)
#current_dir = os.path.dirname(os.path.realpath(__file__))

import inspect
from unittesting import my_assert

from importlib import reload
import litegrade
import questiondriver
#import commondriver
litegrade = reload(litegrade)
questiondriver = reload(questiondriver)
#commondriver = reload(commondriver)
from litegrade import load_questions, mutate_question
from questiondriver import get_nested_value, hello_from_qdriver
#from commondriver import *

msg_prefix = "testing"

def print_err(msg, **kwargs):
	frame = inspect.stack()[1]
	caller_line_num = inspect.getframeinfo(inspect.stack()[1][0]).lineno
	sys.stderr.write(f"{msg_prefix}: (line {caller_line_num}) {msg}\n")

	callback = kwargs.get("callback", None)
	if callback != None:
		callback()
	
def load_questions_tests():
	questions_fname = "questions.json"
	expected_questions_obj = {
		"questions": {
			"apples_question": {
				"question_type": "multiple-choice",
				"prompt": "How do you like them apples?",
				"choices_label_type": "letters",
				"choices": [
					{
						"description": "They're great!",
						"explanation": "Even though Matt Damon asked, the question isn't referring to apples"
					},
					{
						"description": "They're my favorite!",
						"explanation": "Though they keep the doctor away, the question isn't referring to apples"
					},
					{
						"description": "I'd rather have an orange",
						"explanation": "Though citrus is good for you, the question isn't referring to fruit"
					},
					{
						"description": "None of the above",
						"explanation": "'apples' is a metaphor"
					}
				],
				"correct_choice": 3
			},
			"gravy_question": {
				"question_type": "multiple-choice",
				"prompt": "Do you like gravy in your cereal?",
				"choices_label_type": "numbers",
				"choices": [
					{
						"description": "Obsolutely not!",
						"explanation": "Cereal tastes much better with cereal, a breakfast meal"
					},
					{
						"description": "Only on the side",
						"explanation": "Gravy on the side makes more sense. However, it's not suited for breakfast"
					},
					{
						"description": "Uhh, yeah! Gravy is my favorite",
						"explanation": "Though gravy is good, it's better suited for dinner"
					}
				],
				"correct_choice": 0
			},
			"cleverness_question": {
				"question_type": "true-or-false",
				"prompt": "Are these questions clever?",
				"correct_choice": "true",
				"explaination": "They're so good, an explaination is not needed"
			}
		}
	}

	if not os.path.isfile(questions_fname):
		print_err(f"'"+questions_fname+"' not found", callback=lambda: None)
	
	my_assert(load_questions(questions_fname), expected_questions_obj)

def get_nested_value_tests():

	# def get_nested_value(nested_keys_and_indices_list, obj):
	# return target_value

	# Test 0.1
	my_assert( \
		get_nested_value([1],["first","second","third","fourth"]),
		"second")

	# Test 0.2
	my_assert( \
		get_nested_value( \
			["b","bc","bca"], \
			{
				"a": "a",
				"b": {
					"ba": "valba",
					"bb": {"bba":"valbba"},
					"bc": {
						"bca": "valbca",
						"bcb": "valbcb"
					}
				},
			}),
		"valbca")

	# Test 0.3
	my_assert( \
		get_nested_value( \
			["b","bb"], \
			{
				"a": "a",
				"b": {
					"ba": "valba",
					"bb": {"bba":"valbba"},
					"bc": {
						"bca": "valbca",
						"bcb": "valbcb"
					}
				},
			}),
		{"bba":"valbba"})

	# Test 1
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": "valC"
	}
	nested_keys_and_indices_list = ["keyB"]
	expected_value = {"keyBA": "valBA"}

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 2
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": "valC"
	}
	nested_keys_and_indices_list = ["keyB", "keyBA"]
	expected_value = "valBA"

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 3
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": {
			"keyCA": {
				"keyCAA": "valCAA",
				"keyCAB": [2, 5, 4]
			}
		}
	}
	nested_keys_and_indices_list = ["keyC", "keyCA", "keyCAB"]
	expected_value = [2, 5, 4]

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 4
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": {
			"keyCA": {
				"keyCAA": "valCAA",
				"keyCAB": [2, 5, 4]
			}
		}
	}
	nested_keys_and_indices_list = []
	expected_value = input_obj

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 5
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": {
			"keyCA": {
				"keyCAA": "valCAA",
				"keyCAB": [2, 5, 4]
			}
		}
	}
	nested_keys_and_indices_list = ["keyC", "keyCD", "keyCAA"]
	expected_value = {}

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 6
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": {
			"keyCA": [
				{
					"keyCAA": "valCAA"
				},
				{
					"keyCAB": [8, 3, 9]
				}
			]
		}
	}
	nested_keys_and_indices_list = ["keyC", "keyCA", 1 ,"keyCAB"]
	expected_value = [8, 3, 9]

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 7
	input_obj = {
		"keyA": "valA",
		"keyB": {
			"keyBA": "valBA"
		},
		"keyC": {
			"keyCA": [
				{
					"keyCAA": "valCAA"
				},
				{
					"keyCAB": [8, 3, 9]
				}
			]
		}
	}
	nested_keys_and_indices_list = ["keyC", "keyCA", 1 ,"keyCAZ"]
	expected_value = {}

	my_assert( \
		get_nested_value(nested_keys_and_indices_list, input_obj), \
		expected_value)

	# Test 8
	input_obj = {
		"keyA": "valA",
		"keyB": [3, 2],
		"keyC": {
			"keyCA": "valCA",
			"keyCB": "valCB"
		},
		"keyD": "valD"
	}
	nested_keys_and_indices_list = ["keyC", "keyCB"]
	expected_value = "valCB"

	my_assert( \
		get_nested_value(nested_keys_and_indices_list,input_obj), \
		expected_value)

	# Test 9
	input_obj = {
		"keyA": "valA",
		"keyB": [3, 2],
		"keyC": {
			"keyCA": "valCA",
			"keyCB": [
				000,
				111,
				222,
				333	
			],
			"keyCC": 100
		},
		"keyD": "valD"
	}
	nested_keys_and_indices_list = ["keyC","keyCB",2]
	expected_value = 222

	my_assert( \
		get_nested_value(nested_keys_and_indices_list,input_obj), \
		expected_value)

	# Test 10
	actual_val = get_nested_value([2],[{"a":"a"},{"b":"b"},{"c":"c"},{"d":"d"}])
	expect_val = {"c":"c"}
	my_assert(actual_val, expect_val)

def hello_from_qdriver_tests():

	# def hello_from_qdriver(obj):
	# (no return)

	input_obj = {
		"keyA": "valA",
		"keyB": [
			{
				"key_BA": "val_BA"
			},
			{
				"key_BB": "valBB"
			}
		],
		"keyC": {
			"keyCA": "valCA"
		}
	}

	expected_obj = {
		"keyA": "valA",
		"keyB": [
			{
				"key_BA": "val_BA"
			},
			{
				"key_BB": "New value added"
			}
		],
		"keyC": {
			"keyCA": "valCA"
		}
	}

	hello_from_qdriver(input_obj)
	my_assert(input_obj, expected_obj)

def mutate_question_tests():
	
	input_questions_obj = load_questions("questions.json")

	expected_questions_obj = {
		"questions": {
			"apples_question": {
				"question_type": "multiple-choice",
				"prompt": "How do you like them apples?",
				"choices_label_type": "letters",
				"choices": [
					{
						"description": "They're great!",
						"explanation": "Even though Matt Damon asked, the question isn't referring to apples"
					},
					{
						"description": "They're my favorite!",
						"explanation": "Though they keep the doctor away, the question isn't referring to apples"
					},
					{
						"description": "I'd rather have an orange",
						"explanation": "Though citrus is good for you, the question isn't referring to fruit"
					},
					{
						"description": "None of the above",
						"explanation": "'apples' is a metaphor"
					}
				],
				"correct_choice": 3
			},
			"gravy_question": {
				"question_type": "multiple-choice",
				"prompt": "Do you like gravy in your cereal?",
				"choices_label_type": "numbers",
				"choices": [
					{
						"description": "Obsolutely not!",
						"explanation": "Cereal tastes much better with cereal, a breakfast meal"
					},
					{
						"description": "NEW Answer Description", # <<< the mutation
						"explanation": "Gravy on the side makes more sense. However, it's not suited for breakfast"
					},
					{
						"description": "Uhh, yeah! Gravy is my favorite",
						"explanation": "Though gravy is good, it's better suited for dinner"
					}
				],
				"correct_choice": 0
			},
			"cleverness_question": {
				"question_type": "true-or-false",
				"prompt": "Are these questions clever?",
				"correct_choice": "true",
				"explaination": "They're so good, an explaination is not needed"
			}
		}
	}

	mutate_question(input_questions_obj)
	my_assert(input_questions_obj, expected_questions_obj)

def main():
	# litegrade.py
	load_questions_tests()
	mutate_question_tests()

	# questiondriver.py
	get_nested_value_tests()
	hello_from_qdriver_tests()

	print("main end")

main()




