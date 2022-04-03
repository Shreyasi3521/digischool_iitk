from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# Importing models modules
from loginapp import models as login_models
from courseapp import models as course_models
from lectureapp import models as lecture_models

# Importing Security modules.
from django.middleware import csrf

# extra utilities.
import re
import datetime
from backend_functions.universal_values import *


def lecturePage(request):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>alert("Some error occured: Incorrect Http Method")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')

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
				return HttpResponse(f'''<body><script>alert("Some Error Occured: Maybe the teacher is still not verified, Please contact us.")</script><meta http-equiv="refresh" content='0; url="/logout/"'/></body>''')
			
			all_course_id = [each_teached_course.course_id for each_teached_course in teached_courses]

			lecture_all_list = [lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_user_course.course_id) for each_user_course in teached_courses]

			return render(request, "lecture_teacher.html", { "lecture_all_list":lecture_all_list, "all_course_list":all_course_id,  "subject_code": { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))} })

		if extract_user__user_signup_database.user_category == "STUDENT":

			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = str(selected_user_class) + str(selected_user_section) + str(OFFERING_YEAR)

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.get(unique_id=generated_unique_id)
			all_course_id = all_course_id.course_id_array
			all_course_id = all_course_id.strip().split(" ")
			all_course_id = { i: all_course_id[i] for i in range(len(all_course_id)) }

			user_courses = course_models.AVAILABLE_COURSES.objects.filter(course_id__in=all_course_id)
			
			lecture_all_list = {i:lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_user_course.course_id) for i, each_user_course in enumerate(user_courses)}
			
			return render(request, "lecture_student.html", { "lecture_all_list":lecture_all_list, "all_course_list":all_course_id,  "subject_code":  { i: [AVAILABLE_SUBJECTS[i], FULL_NAME[i]] for i in range(len(AVAILABLE_SUBJECTS))}})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

		
def createPage(request, course_id_to_upload):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>alert("Some error occured: Incorrect HTTP Request Method.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
	
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
			return HttpResponse(f'''<body><script>alert("Some error occured: This is not the course for the current teacher.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
		
		full_course_name = FULL_NAME[AVAILABLE_SUBJECTS.index(course_id_to_upload[0:2])]

		return render(request, "lecture_create.html", {"csrf_token" : csrf_token, "course_id":course_id_to_upload,  "full_course_name": full_course_name })
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')

def lectureUploaded(request):
	if request.GET or len(request.GET) > 0:
		return HttpResponse(f'''<body><script>alert("Some error occured: Incorrect HTTP Request Method.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
	
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
		lecture_title = input_data.get("lecture_title", "").strip()
		lecture_title_check = len(lecture_title) <= 200 and len(lecture_title) >= 10
		
		selected_course_id_check = False
		for each_teached_course in teached_courses:
			if each_teached_course.course_id == selected_course_id:
				selected_course_id_check = True
				course_in_context = each_teached_course
				break


		if request.FILES:
			lecture_files = request.FILES.get("lecture-files", None)
			video_file = request.FILES.get("video-file", None)
		else:
			lecture_files = None
			video_file = None

		lecture_files_check = True
		if lecture_files:
			# lecture files are not compulsory.
			if len(lecture_files.name.strip()) > 100 or len(lecture_files.name.strip()) < 6:
				lecture_files_check = False
			reverse_file_name = lecture_files.name.strip()[::-1]
			file_extension = ""
			for char in reverse_file_name:
				file_extension += char
				if char == ".":
					break
			file_extension = file_extension[::-1]
			if not (file_extension in ALLOWED_FILE_TYPE):
				lecture_files_check = False


		video_files_check= True
		if video_file:
			# video files are not compulsory.
			if len(video_file.name.strip()) > 100 or len(video_file.name.strip()) < 6:
				video_files_check = False
			

			reverse_file_name = video_file.name.strip()[::-1]
			file_extension = ""
			for char in reverse_file_name:
				file_extension += char
				if char == ".":
					break
			file_extension = file_extension[::-1]

			if not (file_extension in ALLOWED_VIDEO_FILE_TYPE):
				video_files_check = False
		
		if not (selected_course_id_check and lecture_files_check and video_files_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')


		lecture_series_number_new = course_in_context.lecture_series_number + 1
		
		if lecture_series_number_new >= 100:
			return HttpResponse(f'''<body><script>alert("Maximum Limit of Lectures is reached. Please contact us.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
		
		course_in_context.lecture_series_number = lecture_series_number_new
		course_in_context.save()

		lecture_unique_id = str(selected_course_id) + (str(lecture_series_number_new) if len(str(lecture_series_number_new)) == 2 else "0" + str(lecture_series_number_new))

		try:
			setting_lecture = lecture_models.ALL_LECTURES(lecture_title = lecture_title,  files=lecture_files, lecture_unique_id= lecture_unique_id, course_mapping = course_in_context, video_server_name= video_file)
			setting_lecture.save()
		except:
			"""----------Some error while setting lecture.---------------"""
			lecture_series_number_new = max(course_in_context.lecture_series_number - 1, 0)
			course_in_context.lecture_series_number = lecture_series_number_new
			course_in_context.save()
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/lecture/create/{selected_course_id}"'/></body>''')
		
		"""----------lecture Succesfully Created.---------------"""
		return HttpResponse(f'''<body><script>alert("Lecture is sccessfully created!!")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def eachLectures(request, given_unique_id):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>alert("Some error occured: Incorrect HTTP Request Method.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
	
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

		if not autheticated:
			return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')

		upload_date_q = selected_lecture.lecture_datetime

		return render(request, "lecture_each_page.html", {"csrf_token": csrf_token, "given_lecture":selected_lecture, "upload_date":upload_date_q, "course_id":course_in_context.course_id})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')


def editLecturePage(request, lecture_unique_id):
	if request.POST or len(request.POST) > 0:
		return HttpResponse(f'''<body><script>alert("Some error occured: Incorrect HTTP Request Method.")</script><meta http-equiv="refresh" content='0; url="/lecture/"'/></body>''')
	
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

		if not autheticated:
			return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/lecture/view/{lecture_unique_id}"'/></body>''')
		
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
		edit_lecture_title_check = len(edit_lecture_title) <= 200 and len(edit_lecture_title) >= 10


		if request.FILES:
			edit_lecture_files = request.FILES.get("lecture-files", None)
			edit_video_file = request.FILES.get("video-file", None)
		else:
			edit_lecture_files = None
			edit_video_file = None

		autheticated = False
		for each_teached_course in teached_courses:
			all_lecture_list_in_a_course = lecture_models.ALL_LECTURES.objects.filter(lecture_unique_id__contains=each_teached_course.course_id)
			for each_lecture_in_course in all_lecture_list_in_a_course:
				if each_lecture_in_course.lecture_unique_id == lecture_unique_id:
					autheticated = True
					selected_test = each_lecture_in_course
					course_in_context = each_teached_course
					break

		edit_lecture_files_check = True
		if edit_lecture_files:
			# lecture files are not compulsory.
			if len(edit_lecture_files.name.strip()) > 100 or len(edit_lecture_files.name.strip()) < 6:
				edit_lecture_files_check = False
			reverse_file_name = edit_lecture_files.name.strip()[::-1]
			file_extension = ""
			for char in reverse_file_name:
				file_extension += char
				if char == ".":
					break
			file_extension = file_extension[::-1]
			if not (file_extension in ALLOWED_FILE_TYPE):
				edit_lecture_files_check = False


		edit_video_files_check= True
		if edit_video_file:
			# video files are not compulsory.
			if len(edit_video_file.name.strip()) > 100 or len(edit_video_file.name.strip()) < 6:
				edit_video_files_check = False
			reverse_file_name = edit_video_file.name.strip()[::-1]
			file_extension = ""
			for char in reverse_file_name:
				file_extension += char
				if char == ".":
					break
			file_extension = file_extension[::-1]
			if not (file_extension in ALLOWED_VIDEO_FILE_TYPE):
				edit_video_files_check = False
		

		if not (autheticated and edit_lecture_title_check and edit_lecture_files_check and edit_video_files_check):
			return HttpResponse(f'''<body><script>alert("Some error occured: some inputs were invalid.")</script><meta http-equiv="refresh" content='0; url="/lecture/edit/{lecture_unique_id}"'/></body>''')

		try:
			updating_lecture = lecture_models.ALL_LECTURES.objects.get(lecture_unique_id=lecture_unique_id)
			updating_lecture.lecture_title = edit_lecture_title
			updating_lecture.video_server_name = edit_video_file
			updating_lecture.files = edit_lecture_files
			updating_lecture.save()
		except:
			"""----------Some error while updating lecture.---------------"""
			return HttpResponse(f'''<body><script>alert("Some error occured: Server issue. Please try again later. If issue persists contact us.")</script><meta http-equiv="refresh" content='0; url="/lecture/edit/{lecture_unique_id}"'/></body>''')
		
		"""----------lecture is successfully edited.---------------"""
		return HttpResponse(f'''<body><script>alert("Lecture is sccessfully Edited!!")</script><meta http-equiv="refresh" content='0; url="/lecture/view/{lecture_unique_id}"'/></body>''')
	else:
		# session is inactive or user is not "TEACHER"
		return HttpResponse(f'''<body><script>alert("Unauthorised Access.")</script><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')