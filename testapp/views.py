from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# Importing models modules
from loginapp import models as login_models
from profileapp import models as profile_models
from courseapp import models as course_models
from testapp import models as test_models

# Importing Security modules.
from django.middleware import csrf
import bcrypt
import datetime
from backend_functions.universal_values import OFFERING_YEAR


def testPage(request):
	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	if active_status:
		extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.filter(id=user_id)[0]

		if extract_user__user_signup_database.user_category == "TEACHER":
			courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= extract_user__user_signup_database)
			if not (request.POST.get("upload", "no").strip().lower() == "yes"):

				return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":False, "user_courses":courses, "test_upload_for_course": None})
			else:	
				selected_course_id = request.POST.get("course_available", "").strip()
				verified_course_id = False
				for c in courses:
					if c.course_id == selected_course_id:
						verified_course_id = True
						break
				if verified_course_id and selected_course_id:
					return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload": False, "some_error":False, "user_courses": None, "test_upload_for_course":selected_course_id})
				else:
					# received course_id was tempered.
					return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":True, "user_courses":courses, "test_upload_for_course":None})

		if extract_user__user_signup_database.user_category == "STUDENT":
			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = selected_user_class + selected_user_section + OFFERING_YEAR

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=generated_unique_id)
			all_course_id = all_course_id.strip().split(" ")

			return render(request, "student_test.html", {"csrf_token":csrf_token, "user_courses":course_models.AVAILABLE_COURSES, "all_course_list":all_course_id})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
		

def testUploaded(request):
	if request.GET:
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

	# Session and tokens.
	csrf_token = csrf.get_token(request)
	active_status = False
	# getting user_id from session token.
	user_id = None
	if request.session.has_key('user_id'):
		active_status = True
		user_id = request.session["user_id"]

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.filter(id=user_id)[0]
	if active_status and extract_user__user_signup_database.user_category == "TEACHER":

		courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= extract_user__user_signup_database)
		

		# ------------again same strip and validation. And if tempered alert and then go to no_yet_upoload section.
		input_data = requset.POST

		selected_course_id = request.POST.get("selected_course", "").strip()
		test_title = input_data.get("test_title", "").strip()
		test_instruction = input_data.get("test_instruct", "").strip()
		test_start_date = input_data.get("start_date").strip()
		test_start_time = input_data.get("start_time").strip()
		test_end_date = input_data.get("end_date").strip()
		test_end_time = input_data.get("end_time").strip()
		test_files = request.FILES["test_files"]

		# here validate.
		selected_course_id_check = False
		for c in courses:
			if c.course_id == selected_course_id:
				selected_course_id_check = True
				course_in_context = c
				break

				
			"""test_title_check = 
			test_instruction_check =
			test_start_date_check =
			test_start_time_check
			test_end_date_check
			test_end_time_check
			test_files_check"""

		if not (selected_course_id_check and test_title_check and test_instruction_check and test_start_date_check and test_start_time_check and test_end_date_check and test_end_time_check and test_files_check):
			return HttpResponse(f'''<body><script>alert("Some error occured")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
			# alternatively use this,
			# return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":True, "user_courses":courses, "test_upload_for_course":None})
			
		# Formatting.
		s_date, s_time = test_start_date.split("-"), test_start_time.split(":")
		# datetime(year, month, day, hour, minute, second, microsecond.
		start_datetime = datetime(s_date[0], s_date[1], s_date[2], s_time[0], s_time[1], 0, 0)

		e_date, e_time = test_end_date_date.split("-"), test_end_time_time.split(":")
		end_datetime = datetime(e_date[0], e_date[1], e_date[2], e_time[0], e_time[1], 0, 0)



		test_series_number_new = len(course_in_context.all_tests_set.all()) + 1
		course_in_context.test_series_number = test_series_number_new
		course_in_context.save()

		test_unique_id = selected_course_id+test_series_number_new

		try:
			setting_test = test_models.ALL_TESTS(test_title = test_title, test_instruction = test_instruction, start_datetime =start_datetime, end_datetime=end_datetime, files=test_files, test_unique_id= test_unique_id, course_mapping = course_in_context)
			setting_test.save()
		except:
			"""----------Some error while setting test.---------------"""
			return HttpResponse(f'''<body><script>alert("Some error occured")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
			# alternatively use this,
			# return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":True, "user_courses":courses, "test_upload_for_course":None})
		"""----------test Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Test is sccessfully created!!")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def eachTestView(request, given_unique_id):
	if request.POST and len(request.GET)== 0:
		#------------ upload test, tbd--------------------------------
		
	elif request.GET and len(request.POST) == 0:
		# Session and tokens.
		csrf_token = csrf.get_token(request)
		active_status = False

		# getting user_id from session token.
		user_id = None
		if request.session.has_key('user_id'):
			active_status = True
			user_id = request.session["user_id"]

		if active_status:
			extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.filter(id=user_id)[0]
			
			if extract_user__user_signup_database.user_category == "TEACHER":
				courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= extract_user__user_signup_database)
				autheticated = False
				for c in courses:
					all_test_list_in_a_course = c.all_tests_set.all()
					for t in all_test_list_in_a_course:
						if t.test_unique_id == given_unique_id:
							autheticated = True
							selected_test = t
							break

				if autheticated:
					return render(request, "each_test_view_page.html", {"csrf_token": csrf_token, "user_category":"TEACHER", "test_view":selected_test, "error_occured":False})
				else:
					return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')

			if extract_user__user_signup_database.user_category == "STUDENT":
				selected_user_class = extract_user__user_signup_database.user_class
				selected_user_section = extract_user__user_signup_database.user_section
				generated_unique_id = selected_user_class + selected_user_section + OFFERING_YEAR

				all_course_id = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=generated_unique_id)
				all_course_id = all_course_id.strip().split(" ")

				autheticated = False
				for each_course_id in all_course_id:
					each_course = course_models.AVAILABLE_COURSES.objects.filter(course_id=each_course_id)[0]
					all_test_list_in_a_course = each_course.all_tests_set.all()
					for t in all_test_list_in_a_course:
						if t.test_unique_id == given_unique_id:
							autheticated = True
							selected_test = t
							break
				
				if autheticated:
					return render(request, "each_test_view_page.html", {"csrf_token": csrf_token, "user_category":"STUDENT", "test_view":selected_test, "error_occured":False})
				else:
					return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		else:
			# session is inactive.
			return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
	else:
		return HttpResponse(f'''<body><script>alert("Some Error Occured.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')


def editTest(request):
