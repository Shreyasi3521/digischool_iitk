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
from lectureapp import models as lecture_models
# Importing Security modules.
from django.middleware import csrf
import bcrypt
import datetime
from backend_functions.universal_values import *
import os, json
from digischool.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage

def newsPage(request):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>Some error occured: Incorrect HTTP Request Method.</script><meta http-equiv="refresh" content='0; url="/news/"'/></body>''')

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

			news_all_list = [course_models.ALL_ANOUNCEMENT.objects.filter(news_unique_id__contains=each_user_course.course_id) for each_user_course in teached_courses]

			return render(request, "news_teacher.html", { "news_all_list":news_all_list, "all_course_list":all_course_id,  "subject_code": { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})

		if extract_user__user_signup_database.user_category == "STUDENT":

			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = str(selected_user_class) + str(selected_user_section) + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)

			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")

			user_courses = course_models.AVAILABLE_COURSES.objects.filter(course_id__in=all_course_id)
			
			news_all_list = {i:course_models.ALL_ANOUNCEMENT.objects.filter(news_unique_id__contains=each_user_course.course_id) for i, each_user_course in enumerate(user_courses)}
			
			all_course_id = { i: all_course_id[i] for i in range(len(all_course_id)) }
			
			return render(request, "news_student.html", { "news_all_list":news_all_list, "all_course_list":all_course_id,  "subject_code":  { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})
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

		return render(request, "news_create.html", {"csrf_token" : csrf_token, "course_id":course_id_to_upload,  "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def newsUploaded(request):
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
	if active_status and extract_user__user_signup_database.user_category == "TEACHER":
		school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
		teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

		input_data = request.POST

		selected_course_id = request.POST.get("selected_course", "").strip()
		news_title = input_data.get("news_title", "").strip()
		news_description = input_data.get("news_description", "").strip()

		# Similar strip and validation. and then formating. And if tempered alert and then go to /test/upload/ with an alert.
		selected_course_id_check = False
		# here validate.

		for each_teached_course in teached_courses:
			if each_teached_course.course_id == selected_course_id:
				selected_course_id_check = True
				course_in_context = each_teached_course
				break

		
		

		

		news_title_check = True
		news_description_check =True
		


		if not (selected_course_id_check and news_title_check and news_description_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')

		

		news_series_number_new = course_in_context.news_series_number + 1
		course_in_context.news_series_number = news_series_number_new
		course_in_context.save()
		news_unique_id = str(selected_course_id) + (str(news_series_number_new) if len(str(news_series_number_new)) == 2 else "0" + str(news_series_number_new))


		

		try:
			setting_news = course_models.ALL_ANOUNCEMENT(news_title = news_title, news_description = news_description, news_unique_id= news_unique_id, course_mapping = course_in_context)
			
			setting_news.save()

		except:
			"""----------Some error while setting forum.---------------"""
			news_series_number_new = max(course_in_context.news_series_number - 1, 0)
			course_in_context.news_series_number = news_series_number_new
			course_in_context.save()
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
		
		"""----------forum Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Announcement is sccessfully created!!")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def editNewsPage(request, news_unique_id):
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
	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.get(id=user_id)
	if active_status and extract_user__user_signup_database.user_category == "TEACHER":
		school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
		teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

		autheticated = False
		for each_teached_course in teached_courses:
			all_news_list_in_a_course = course_models.ALL_ANOUNCEMENT.objects.filter(news_unique_id__contains=each_teached_course.course_id)
			for each_news_in_course in all_news_list_in_a_course:
				if each_news_in_course.news_unique_id == news_unique_id:
					autheticated = True
					selected_news =  each_news_in_course
					course_in_context = each_teached_course
					break
		try:
			if int(news_unique_id[10:]) > course_in_context.news_series_number:
				autheticated = False
		except:
			autheticated = False
		if not autheticated:
				return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
		full_course_name = FULL_NAME[AVAILABLE_SUBJECTS.index(news_unique_id[0:2])]

		return render(request, "news_edit.html", {"csrf_token": csrf_token, "news_unique_id": news_unique_id, "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')



def editNewsUpload(request, news_unique_id):
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
	if active_status and extract_user__user_signup_database.user_category == "TEACHER":
		
		school_db_teacher_entry = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_email=extract_user__user_signup_database.email_address)
		teached_courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= school_db_teacher_entry ) # for now, it will be only one entry.

		# Similar strip and validation. and then formating. And if tempered alert and then go to /test/upload/ with an alert.
		input_data = request.POST

		edit_news_title = input_data.get("news_title", "").strip()
		edit_news_description = input_data.get("news_description", "").strip()
		
		autheticated = False
		for each_teached_course in teached_courses:
			all_news_list_in_a_course = course_models.ALL_ANOUNCEMENT.objects.filter(news_unique_id__contains=each_teached_course.course_id)
			for each_news_in_course in all_news_list_in_a_course:
				if each_news_in_course.news_unique_id == news_unique_id:
					autheticated = True
					selected_news =  each_news_in_course
					course_in_context = each_teached_course
					break
		try:
			if int(news_unique_id[10:]) > course_in_context.news_series_number:
				autheticated = False
		except:
			autheticated = False

		
		edit_news_title_check = True
		edit_news_description_check = True

		if not (autheticated and edit_news_title_check and edit_news_description_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		try:
			updating_news = course_models.ALL_ANOUNCEMENT.objects.get(news_unique_id=news_unique_id)
			updating_news.news_title = edit_news_title
			updating_news.news_description = edit_news_description
			updating_news.news_datetime = datetime.datetime.now()
			updating_news.save()
		except:
			"""----------Some error while setting test.---------------"""
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
		"""----------test Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Announcement is sccessfully Edited!!")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

