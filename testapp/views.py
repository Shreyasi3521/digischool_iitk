from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

# Importing models modules
from loginapp import models as login_models
from profileapp import models as profile_models
from courseapp import models as course_models

# Importing Security modules.
from django.middleware import csrf
import bcrypt


def testPage(request):
	# Session and tokens.
	csrf_token = csrf.get_token(request)

	# getting user_id from session token.

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.filter(id=user_id)[0]

	if extract_user__user_signup_database.user_category == "TEACHER":
		
		if len(request.POST) != 8:
			# again same strip and validation. And if tempered alert and then go to no_yet_upoload section.
			courses = course_model.Course.objects.filter(course_instuctor= login_model.UserDB.objects.filter(id=userid)[0])
			test = course_model.Test

			return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload":True, "user_courses":courses, "user_tests": test})
		else:
			return render(request, "teacher_test.html", {"csrf_token":csrf_token, "not_yet_upload":False, "user_courses": None, "user_tests": None})
		#show the teacher page.

	else:
		# show the student page.
