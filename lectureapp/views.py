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


def lecturePage(request):
	if request.POST or len(request.POST) > 0:
		return HttpResponse("wrong method")

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

			lecture_all_list = [lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_user_course.course_id) for each_user_course in teached_courses]

			return render(request, "lecture_teacher.html", { "lecture_all_list":lecture_all_list, "all_course_list":all_course_id,  "subject_code": { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})

		if extract_user__user_signup_database.user_category == "STUDENT":

			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = str(selected_user_class) + str(selected_user_section) + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)

			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")

			user_courses = course_models.AVAILABLE_COURSES.objects.filter(course_id__in=all_course_id)
			
			lecture_all_list = {i:lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_user_course.course_id) for i, each_user_course in enumerate(user_courses)}
			all_course_id = { i: all_course_id[i] for i in range(len(all_course_id)) }
			return render(request, "lecture_student.html", { "lecture_all_list":lecture_all_list, "all_course_list":all_course_id,  "subject_code":  { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}, "current_datetime":datetime.datetime.now()})
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

		return render(request, "lecture_create.html", {"csrf_token" : csrf_token, "course_id":course_id_to_upload,  "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def lectureUploaded(request):
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

		# Similar strip and validation. and then formating. And if tempered alert and then go to /test/upload/ with an alert.
		input_data = request.POST

		selected_course_id = request.POST.get("selected_course", "").strip()
		lecture_title = input_data.get("lecture_title", "").strip()

		if request.FILES:
			lecture_files = request.FILES.get("lecture-files", None)
			video_file = request.FILES.get("video-file", None)

		# here validate.
		selected_course_id_check = False
		for each_teached_course in teached_courses:
			if each_teached_course.course_id == selected_course_id:
				selected_course_id_check = True
				course_in_context = each_teached_course
				break

		lecture_title_check = True
		lecture_files_check=True
		video_files_check=True


		if not (selected_course_id_check and lecture_title_check and lecture_files_check and video_files_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')

		lecture_series_number_new = course_in_context.lecture_series_number + 1
		course_in_context.lecture_series_number = lecture_series_number_new
		course_in_context.save()

		lecture_unique_id = str(selected_course_id) + (str(lecture_series_number_new) if len(str(lecture_series_number_new)) == 2 else "0" + str(lecture_series_number_new))

		try:
			setting_lecture = lecture_models.ALL_LECTURES(lecture_title = lecture_title,  files=lecture_files, lecture_unique_id= lecture_unique_id, course_mapping = course_in_context, video_server_name= video_file)
			setting_lecture.save()
		except:
			"""----------Some error while setting test.---------------"""
			lecture_series_number_new = max(course_in_context.lecture_series_number - 1, 0)
			course_in_context.lecture_series_number = lecture_series_number_new
			course_in_context.save()
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
		"""----------test Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Lecture is sccessfully created!!")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def eachLectures(request, given_unique_id):
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
				all_lecture_list_in_a_course = lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_teached_course.course_id)
				for each_lecture_in_course in all_lecture_list_in_a_course:
					if each_lecture_in_course.lecture_unique_id == given_unique_id:
						autheticated = True
						selected_lecture = each_lecture_in_course
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
				all_lecture_list_in_a_course = lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_course.course_id)
				for each_lecture_in_course in all_lecture_list_in_a_course:
					if each_lecture_in_course.lecture_unique_id == given_unique_id:
						autheticated = True
						selected_lecture = each_lecture_in_course
						course_in_context = each_course
						break
		try:
			if int(given_unique_id[10:]) > course_in_context.lecture_series_number:
				autheticated = False
		except:
			autheticated = False

		if not autheticated:
			return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/forum/"'/></body>''')

		upload_date_q = selected_lecture.lecture_datetime

		return render(request, "lecture_each_page.html", {"csrf_token": csrf_token, "given_lecture":selected_lecture, "upload_date":upload_date_q, "course_id":course_in_context.course_id})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')



def editLecturePage(request, lecture_unique_id):
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
			all_lecture_list_in_a_course = lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_teached_course.course_id)
			for each_lecture_in_course in all_lecture_list_in_a_course:
				if each_lecture_in_course.lecture_unique_id == lecture_unique_id:
					autheticated = True
					selected_test = each_lecture_in_course
					course_in_context = each_teached_course
					break
		try:
			if int(lecture_unique_id[10:]) > course_in_context.lecture_unique_id:
				autheticated = False
		except:
			autheticated = False
		if not autheticated:
				return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
		full_course_name = FULL_NAME[AVAILABLE_SUBJECTS.index(lecture_unique_id[0:2])]

		return render(request, "lecture_edit.html", {"csrf_token": csrf_token, "lecture_unique_id": lecture_unique_id, "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')



def editLectureUpload(request, lecture_unique_id):
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


		input_data = request.POST

		edit_lecture_title = input_data.get("lecture_title", "").strip()

		if request.FILES:
			edit_lecture_files = request.FILES.get("lecture-files", None)
			edit_video_file = request.FILES.get("video-file", None)



		
		autheticated = False
		for each_teached_course in teached_courses:
			all_lecture_list_in_a_course = lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_teached_course.course_id)
			for each_lecture_in_course in all_lecture_list_in_a_course:
				if each_lecture_in_course.lecture_unique_id == lecture_unique_id:
					autheticated = True
					selected_test = each_lecture_in_course
					course_in_context = each_teached_course
					break
		try:
			if int(lecture_unique_id[10:]) > course_in_context.lecture_unique_id:
				autheticated = False
		except:
			autheticated = False	

		edit_lecture_title_check = True
		edit_lecture_files_check=True
		edit_video_files_check=True

		if not (autheticated and edit_lecture_title_check and edit_lecture_files_check and edit_video_files_check ):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')

		try:
			updating_lecture = lecture_models.ALL_LECTURES.objects.get(lecture_unique_id=lecture_unique_id)
			updating_lecture.lecture_title = edit_lecture_title
			updating_lecture.lecture_datetime = datetime.datetime.now()
			updating_lecture.video_server_name = edit_video_file
			updating_lecture.files = edit_lecture_files
			updating_lecture.save()
		except:
			"""----------Some error while setting test.---------------"""
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
		
		"""----------test Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Test is sccessfully Edited!!")</script><meta http-equiv="refresh" content='0; url="/test/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

