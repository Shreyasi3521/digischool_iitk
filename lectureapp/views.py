from django.shortcuts import render
from django.middleware import csrf
from django.http import HttpRequest, HttpResponse
from courseapp import models as course_models

# test
def lecturePage(request):
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
		if extract_user__user_signup_database.user_category == "STUDENT":
			selected_user_class = extract_user__user_signup_database.user_class
			selected_user_section = extract_user__user_signup_database.user_section
			generated_unique_id = selected_user_class + selected_user_section + OFFERING_YEAR

			all_course_id = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=generated_unique_id)
			all_course_id = all_course_id.strip().split(" ")
			return render(request, "student_lecture.html", {"csrf_token":csrf_token, "user_courses":course_models.AVAILABLE_COURSES, "all_course_list":all_course_id})

		if extract_user__user_signup_database.user_category == "TEACHER":
			courses = course_models.AVAILABLE_COURSES.objects.filter(course_instructor= extract_user__user_signup_database)
			if not (request.POST.get("upload", "no").strip().lower() == "yes"):

				return render(request, "teacher_lecture.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":False, "user_courses":courses, "test_upload_for_course": None})
			else:

				# uploading lecture.
				selected_course_id = request.POST.get("course_available", "").strip()
				verified_course_id = False
				for c in courses:
					if c.course_id == selected_course_id:
						verified_course_id = True
						break
				if verified_course_id and selected_course_id:
					return render(request, "teacher_lecture.html", {"csrf_token":csrf_token, "not_yet_upload": False, "some_error":False, "user_courses": None, "test_upload_for_course":selected_course_id})
				else:
					# received course_id was tempered.
					return render(request, "teacher_lecture.html", {"csrf_token":csrf_token, "not_yet_upload": True, "some_error":True, "user_courses":courses, "test_upload_for_course":None})



# all functions are exactly same as testapp.views. (NOTE: Try to even keep the name same.)
def eachLectures(request,lecture_unique_id):
	pass