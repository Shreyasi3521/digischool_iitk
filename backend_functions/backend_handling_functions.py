from courseapp import models as course_models
from . import universal_values
from loginapp import models as login_models
import os, json
def auto_assign_course(user_cls, user_sec, user_category):
	if user_category == "STUDENT":
		unique_id = user_cls + user_sec + str(universal_values.OFFERING_YEAR)
		class_course_mapping_entry = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=unique_id)
		return class_course_mapping_entry
	if user_category == "TEACHER":
		return None

def removing_entries():
	pass
	# remove loginapp.models.USER_SIGNUP_DATABASE entries if user is not verfied and time is excceded by 2 (ALLOWED_ENTRY_TIME) days.

def returnStats(test_each, student_id):

	test_answer_file_name = test_each.test_data
	test_answer_file = open(test_answer_file_name,"r")
	test_answer = json.load(test_answer_file)

	n = 0
	sum_score = 0
	individual_score = float('-inf')
	for keys in test_answer:
		if str(keys).isnumeric():
			student_answer_file_name = test_answer[keys]
			student_answer_file = open(student_answer_file_name,"r")
			student_answer = json.load(student_answer_file)
			if student_answer["SCORE"] != float("inf"):
				sum_score += int(student_answer["SCORE"])
				n += 1
				if str(student_id) == str(keys):
					individual_score = int(student_answer["SCORE"])
	average = (sum_score / n) if n != 0 else 0

	return average, individual_score
