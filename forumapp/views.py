from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# Importing models modules
from loginapp import models as login_models
from profileapp import models as profile_models
from courseapp import models as course_models
from testapp import models as test_models
from forumapp import models as forum_models
# Importing Security modules.
from django.middleware import csrf
import bcrypt
import datetime
from backend_functions.universal_values import *
import os, json
from digischool.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage
# Create your views here.
def forumPage(request):
	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	if active_status:
		extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)

		if extract_user__user_signup_database.user_category == "TEACHER":
			school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
			teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.
			
			if not school_db_teacher_entry.activation_status:
				return HttpResponse(f'''<body><script>Some error occured: Maybe the teacher is still not verified, please contact us.</script><meta http-equiv="refresh" content='0; url="/logout/"'/></body>''')
			all_course_id = [each_teached_course.course_id for each_teached_course in teached_courses]
		
			forum_all_list = [forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_user_course.course_id) for each_user_course in teached_courses]

			return render(request, "forum_teacher.html", { "forum_all_list":forum_all_list, "all_course_list":all_course_id,  "subject_code": { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})

		if extract_user__user_signup_database.user_category == "STUDENT":

			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = str(selected_user_class) + str(selected_user_section) + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)

			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")

			user_courses = course_models.AVAILABLE_COURSES.objects.filter(course_id__in=all_course_id)
			
			forum_all_list = {i:forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_user_course.course_id) for i, each_user_course in enumerate(user_courses)}
			all_course_id = { i: all_course_id[i] for i in range(len(all_course_id)) }
			return render(request, "forum_student.html", { "forum_all_list":forum_all_list, "all_course_list":all_course_id,  "subject_code":  { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def createPage(request, course_id_to_upload):
	if request.POST or len(request.POST) > 0 or len(request.GET) > 0: # need to confirm.
		return HttpResponse(f'''<body><script>Some error occured: Incorrect HTTP Request Method.</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)
	if active_status and extract_user__user_signup_database.user_category == "TEACHER":
		school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
		teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

		selected_course_id_check = False
		for each_teached_course in teached_courses:
			if each_teached_course.course_id == course_id_to_upload:
				selected_course_id_check = True
				course_in_context = each_teached_course
				break
		if not selected_course_id_check:
			return HttpResponse(f'''<body><script>Some error occured: This is not the course for the current teacher.</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
		
		full_course_name = FULL_NAME[AVAILABLE_SUBJECTS.index(course_id_to_upload[0:2])]

		return render(request, "forum_create.html", {"csrf_token" : csrf_token, "course_id":course_id_to_upload,  "full_course_name": full_course_name })
	elif active_status and extract_user__user_signup_database.user_category == "STUDENT":
		selected_user_class = extract_user__user_signup_database.user_class
		selected_user_section = extract_user__user_signup_database.user_section
		generated_unique_id = selected_user_class + selected_user_section + str(OFFERING_YEAR)

		all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)
		all_course_id = all_course_id.course_id_array
		all_course_id = all_course_id.strip().split(" ")

		autheticated = False
		for each_course_id in all_course_id:
			if each_course_id == course_id_to_upload:
				autheticated = True
				break

		if not autheticated:
			return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')	
		
		full_course_name = FULL_NAME[AVAILABLE_SUBJECTS.index(course_id_to_upload[0:2])]

		return render(request, "forum_create.html", {"csrf_token" : csrf_token, "course_id":course_id_to_upload,  "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def forumUploaded(request):
	if request.GET or len(request.GET) > 0:
		return HttpResponse(f'''<body><script>Some error occured: Incorrect HTTP Request Method.</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)
	if active_status:
		
		input_data = request.POST

		selected_course_id = request.POST.get("selected_course", "").strip()
		forum_topic = input_data.get("forum_topic", "").strip()
		forum_description = input_data.get("forum_description", "").strip()

		# Similar strip and validation. and then formating. And if tempered alert and then go to /test/upload/ with an alert.
		selected_course_id_check = False
		# here validate.
		if extract_user__user_signup_database.user_category == "TEACHER":
			school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
			teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

			for each_teached_course in teached_courses:
				if each_teached_course.course_id == selected_course_id:
					selected_course_id_check = True
					course_in_context = each_teached_course
					break

		if extract_user__user_signup_database.user_category == "STUDENT":
			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = selected_user_class + selected_user_section + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)
			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")

			for each_course_id in all_course_id:
				if each_course_id == selected_course_id:
					selected_course_id_check =True
					course_in_context = course_models.AVAILABLE_COURSES.objects.get(course_id=each_course_id)
					break

		forum_topic_check = True
		forum_description_check =True


		if not (selected_course_id_check and forum_topic_check and forum_description_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
		
		# Formatting.
		forum_question_json = {"vote": 0}
		forum_question_json["question"] = forum_description
		forum_question_json["id"] = extract_user__user_signup_database.id
		forum_series_number_new = course_in_context.forum_series_number + 1
		course_in_context.forum_series_number = forum_series_number_new
		course_in_context.save()
		forum_unique_id = str(selected_course_id) + (str(forum_series_number_new) if len(str(forum_series_number_new)) == 2 else "0" + str(forum_series_number_new))

		try:
			forum_file_name = os.path.join(BASE_DIR, f"Forum/{forum_unique_id}.json")
			forum_file = open(forum_file_name, "w")
			
			a = json.dump(forum_question_json, forum_file)

			forum_file.close()

		except:
			return HttpResponse("Some error occured. server side.")

		try:
			forum_answer_file_name = os.path.join(BASE_DIR, f"Forum/{forum_unique_id}-answer.json")

			forum_answer_file = open(forum_answer_file_name, "w")
			b = json.dump({"RESOLVED": False, "TIMES": 0}, forum_answer_file)
			forum_answer_file.close()

		except:
			return HttpResponse("Some error occured. server side.")

		try:
			setting_forum = forum_models.ALL_FORUMS(forum_title = forum_topic, forum_question = forum_file_name, forum_unique_id= forum_unique_id, course_mapping = course_in_context, forum_answers=forum_answer_file_name)
			
			setting_forum.save()

		except:
			"""----------Some error while setting forum.---------------"""
			forum_series_number_new = max(course_in_context.forum_series_number - 1, 0)
			course_in_context.forum_series_number = forum_series_number_new
			course_in_context.save()
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
		
		"""----------forum Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Forum is sccessfully created!!")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def eachForumView(request, given_unique_id):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>Some error occured: Incorrect HTTP Request Method.</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False

	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	if active_status:
		extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)

		if extract_user__user_signup_database.user_category == "TEACHER":
			school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
			teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

			autheticated = False
			for each_teached_course in teached_courses:
				all_forum_list_in_a_course = forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_teached_course.course_id)
				for each_forum_in_course in all_forum_list_in_a_course:
					if each_forum_in_course.forum_unique_id == given_unique_id:
						autheticated = True
						selected_forum = each_forum_in_course
						course_in_context = each_teached_course
						break
			try:
				if int(given_unique_id[10:]) > course_in_context.forum_series_number:
					autheticated = False
			except:
				autheticated = False

			if not autheticated:
				return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
			
			forum_questions_file_name = selected_forum.forum_question
			
			forum_questions_file = open(forum_questions_file_name, "r")
			forum_questions = json.load(forum_questions_file)
			forum_questions_file.close()

			full_name_q = login_models.USER_SIGNUP_DATABASE.objects.get(id=forum_questions["id"])
			full_name_q = full_name_q.first_name + " " + full_name_q.last_name

			upload_date_q = selected_forum.forum_datetime

			forum_description = forum_questions["question"]


			forum_answers_file_name = selected_forum.forum_answers
			
			forum_answers_file = open(forum_answers_file_name, "r")
			forum_answers = json.load(forum_answers_file)
			forum_answers_file.close()

			answer_number = forum_answers["TIMES"]
			answer_data = dict()
			for i in range(1, answer_number + 1):
				entry = forum_answers[str(i)]
				answer_data[i] = entry



			return render(request, "forum_each_page.html", {"csrf_token": csrf_token, "given_forum":selected_forum, "full_name":full_name_q, "upload_date":upload_date_q, "forum_description": forum_description, "answer_data":answer_data, "forum_unique_id":given_unique_id})

		if extract_user__user_signup_database.user_category == "STUDENT":
			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = selected_user_class + selected_user_section + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)
			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")

			autheticated = False
			for each_course_id in all_course_id:
				each_course = course_models.AVAILABLE_COURSES.objects.get(course_id=each_course_id)
				all_forum_list_in_a_course = forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_course.course_id)
				for each_forum_in_course in all_forum_list_in_a_course:
					if each_forum_in_course.forum_unique_id == given_unique_id:
						autheticated = True
						selected_forum = each_forum_in_course
						course_in_context = each_course
						break

			try:
				if int(given_unique_id[10:]) > course_in_context.forum_series_number:
					autheticated = False
			except:
				autheticated = False
			if not autheticated:
				return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')	
			
			forum_questions_file_name = selected_forum.forum_question
			
			forum_questions_file = open(forum_questions_file_name, "r")
			forum_questions = json.load(forum_questions_file)
			forum_questions_file.close()

			full_name_q = login_models.USER_SIGNUP_DATABASE.objects.get(id=forum_questions["id"])
			full_name_q = full_name_q.first_name + " " + full_name_q.last_name

			upload_date_q = selected_forum.forum_datetime

			forum_description = forum_questions["question"]


			forum_answers_file_name = selected_forum.forum_answers
			
			forum_answers_file = open(forum_answers_file_name, "r")
			forum_answers = json.load(forum_answers_file)
			forum_answers_file.close()

			answer_number = forum_answers["TIMES"]
			answer_data = dict()
			for i in range(1, answer_number + 1):
				entry = forum_answers[str(i)]
				answer_data[i] = entry



			return render(request, "forum_each_page.html", {"csrf_token": csrf_token, "given_forum":selected_forum, "full_name":full_name_q, "upload_date":upload_date_q, "forum_description": forum_description, "answer_data":answer_data, "forum_unique_id":given_unique_id})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def forumAnswerUpload(request,forum_unique_id):
	if request.GET or len(request.GET) > 0:
		return HttpResponse(f'''<body><script>Some error occured: Incorrect HTTP Request Method.</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')

	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)
	if active_status:

		if extract_user__user_signup_database.user_category == "TEACHER":
			school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
			teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.


			autheticated = False
			for each_teached_course in teached_courses:
				all_forum_list_in_a_course = forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_teached_course.course_id)
				
				for each_forum_in_course in all_forum_list_in_a_course:
					if each_forum_in_course.forum_unique_id == forum_unique_id:
						autheticated = True
						selected_forum = each_forum_in_course
						course_in_context = each_teached_course
						break
		
		if extract_user__user_signup_database.user_category == "STUDENT":
			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = selected_user_class + selected_user_section + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)
			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")
			autheticated = False
			for each_course_id in all_course_id:
				each_course = course_models.AVAILABLE_COURSES.objects.get(course_id=each_course_id)
				all_forum_list_in_a_course = forum_models.ALL_FORUMS.objects.filter(forum_unique_id__contains=each_course.course_id)
				for each_forum_in_course in all_forum_list_in_a_course:
					if each_forum_in_course.forum_unique_id == forum_unique_id:
						autheticated = True
						selected_forum = each_forum_in_course
						course_in_context = each_course
						break

		if not autheticated:
			return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')	

		input_data = request.POST

		answer_each = input_data.get("message", "")

		answer_each_check = True

		if not answer_each_check:
			return HttpResponse("wrong data.")


		forum_answers_file_name = selected_forum.forum_answers
		forum_answers_file = open(forum_answers_file_name, "r")
		forum_answers = json.load(forum_answers_file)
		forum_answers_file.close()
		

		try:
			still_entry = forum_answers["TIMES"]
			still_entry += 1
			forum_answers["TIMES"] = still_entry

			create_answer_json = dict()
			create_answer_json["iseven"] = still_entry % 2 == 0
			user_answered = extract_user__user_signup_database
			create_answer_json["full_name"] = user_answered.first_name + " " + user_answered.last_name
			create_answer_json["date_answer"] = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)
			create_answer_json["answer"] = answer_each
			forum_answers[str(still_entry)] = create_answer_json

			
			forum_answers_file = open(forum_answers_file_name, "w")
			a = json.dump(forum_answers, forum_answers_file)
			
			forum_answers_file.close()


		except:
			return HttpResponse(f'''<body><script>alert(There was an error while submission. If time is there please upload the answer again. Else contact teacher.")</script><meta http-equiv="refresh" content='0; url="/forum/view/{forum_unique_id}"'/></body>''')

		return HttpResponse(f'''<body><script>alert(Comment successfully submitted.")</script><meta http-equiv="refresh" content='0; url="/forum/view/{forum_unique_id}"'/></body>''')

