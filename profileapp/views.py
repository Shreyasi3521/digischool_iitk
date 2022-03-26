from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

from loginapp import models as login_models
from profileapp import models as profile_models

from django.middleware import csrf
from . import validation_check
# NOTE: Every view function (except loginapp.views) must have session token extraction and get "user_id" which is nothing by loginapp.models.USER_SIGNUP_DATABSE.id)
# NOTE: In every view function (except loginapp.views), session token must be validated. Else it should be redirected to loginapp.login_page.

def profilePage(request):
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


		## here run all the backend things of perfomance analysis.
		
		return render(request, "profile_page.html", {"user_data" : profile_models.USER_PROFILE_DATABASE.objects.filter(user_signup_db_mapping=extract_user__user_signup_database)[0]})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
		
def editProfilePage(request):
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
		extract_user__user_profile_database = profile_models.USER_PROFILE_DATABASE.objects.filter(user_signup_db_mapping=extract_user__user_signup_database)[0]

		if not extract_user__user_profile_database.edit_once:
			#return HttpResponse(str(extract_user__user_profile_database.edit_once))
			if extract_user__user_signup_database.user_category == "TEACHER":
				return render(request, "teacher_edit_profile_page.html", {"csrf_token":csrf_token})
			if extract_user__user_signup_database.user_category == "STUDENT":
				return render(request, "student_edit_profile_page.html", {"csrf_token":csrf_token})
		else:
			return render(request, "not_allowed_edit_page.html", {"user_category":extract_user__user_signup_database.user_category, "preview_user": extract_user__user_signup_database, "preview_profile": extract_user__user_profile_database})

	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

def editProfilePagePosted(request):
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
		extract_user__user_profile_database = profile_models.USER_PROFILE_DATABASE.objects.filter(user_signup_db_mapping=extract_user__user_signup_database)[0]
		
		if not extract_user__user_profile_database.edit_once:
			if extract_user__user_signup_database.user_category == "STUDENT":
				input_data = request.POST

				other_error = False
				# Stripping and Validating data.
				edit_full_name = input_data.get("edit_name", "").strip().lower().split()
				try:
					edit_first_name, edit_last_name = edit_full_name[0], edit_full_name[1]
					first_name_check = validation_check.nameCheck(edit_first_name)
					last_name_check = validation_check.nameCheck(edit_last_name)
				except:
					other_error = True

				edit_class, edit_section = input_data.get("edit_class", "0").strip(), input_data.get("edit_section", "NaN").strip()
				user_class_check = validation_check.classCheck(edit_class)
				user_section_check = validation_check.sectionCheck(edit_section)

				edit_contact, edit_r_number = input_data.get("edit_contact", "0").strip(), input_data.get("edit_r_number", "0").strip()
				contact_check = validation_check.contactCheck(edit_contact)
				r_number_check = validation_check.rCheck(edit_r_number)


				edit_school_name = input_data.get("edit_school", "").strip()
				school_name_check = validation_check.schoolNameCheck(edit_school_name)

				father_name, mother_name = input_data.get("father_name", "").strip().lower().split(), input_data.get("mother_name", "").strip().lower().split()
				try:
					father_name_check = validation_check.nameCheck(father_name[0]) and validation_check.nameCheck(father_name[1])
					mother_name_check = validation_check.nameCheck(mother_name[0]) and validation_check.nameCheck(mother_name[1])
				except:
					if len(father_name) == 1:
						father_name.append(edit_last_name)
					else:
						other_error = True
					if len(mother_name) == 1:
						mother_name.append(edit_last_name)
					else:
						other_error = True

				if not ((not other_error) and first_name_check and last_name_check and user_class_check and user_section_check and contact_check and r_number_check and school_name_check and father_name_check and mother_name_check):
					# handling tempered data.
					# The incoming data was corrupted (maybe using burpsuite.) (This is because, all the above validations were done at frontend, but still the value arent valid values.)
					return render(request, 'student_edit_profile_page.html', {"csrf_token": csrf_token , "error_edit" : True})

				"""----------Now all the input values are valid.---------------"""



				# data formatting.
				edit_first_name = edit_first_name[0].upper() + edit_first_name[1:]
				edit_last_name = edit_last_name[0].upper() + edit_last_name[1:]
				edit_section = edit_section.upper()
				if len(edit_class) != 2:
					edit_class = "0" + edit_class
				father_name = father_name[0][0].upper() + father_name[0][1:] + " " + father_name[1][0].upper() + father_name[1][1:]
				mother_name = mother_name[0][0].upper() + mother_name[0][1:] + " " + mother_name[1][0].upper() + mother_name[1][1:]


				# backend database working
				#class_course_field = backend_handling_functions.auto_assign_course(edit_class, edit_section, "STUDENT")


				try:
					extract_user__user_signup_database.first_name = edit_first_name
					extract_user__user_signup_database.last_name = edit_last_name
					extract_user__user_signup_database.user_class = edit_class
					extract_user__user_signup_database.user_section = edit_section
					extract_user__user_signup_database.user_contact = edit_contact 
					extract_user__user_signup_database.user_r_number = edit_r_number
					extract_user__user_signup_database.school_name = edit_school_name
					extract_user__user_signup_database.save()

					extract_user__user_profile_database.user_signup_db_mapping = extract_user__user_signup_database
					extract_user__user_profile_database.father_name = father_name
					extract_user__user_profile_database.mother_name = mother_name
					extract_user__user_profile_database.edit_once = True
					extract_user__user_profile_database.save()
				except:
					"""----------Some error while setting.---------------"""
					return render(request, 'student_edit_profile_page.html', {"csrf_token": csrf_token , "error_edit" : True})
				
				"""----------User Succesfully Edited.---------------"""
				return HttpResponse(f'''<body><script>Details are successfully Edited.</script><meta http-equiv="refresh" content='0; url="/profile/"'/></body>''')

			if extract_user__user_signup_database.user_category == "TEACHER":
				input_data = request.POST

				other_error = False
				# Stripping and Validating data.
				edit_full_name = input_data.get("edit_name", "").strip().lower().split()
				try:
					edit_first_name, edit_last_name = edit_full_name[0], edit_full_name[1]
					first_name_check = validation_check.nameCheck(edit_first_name)
					last_name_check = validation_check.nameCheck(edit_last_name)
				except:
					other_error = True

				edit_class, edit_section = input_data.get("edit_class", "0").strip(), input_data.get("edit_section", "NaN").strip()
				user_class_check = validation_check.classCheck(edit_class)
				user_section_check = validation_check.sectionCheck(edit_section)

				edit_contact, edit_r_number = input_data.get("edit_contact", "0").strip(), input_data.get("edit_r_number", "0").strip()
				contact_check = validation_check.contactCheck(edit_contact)
				r_number_check = validation_check.rCheck(edit_r_number)


				edit_school_name = input_data.get("edit_school", "").strip()
				school_name_check = validation_check.schoolNameCheck(edit_school_name)

				if not (other_error and first_name_check and last_name_check and user_class_check and user_section_check and contact_check and r_number_check and school_name_check):
				# handling tempered data.
				# The incoming data was corrupted (maybe using burpsuite.) (This is because, all the above validations were done at frontend, but still the value arent valid values.)
					return render(request, 'teacher_edit_profile_page.html', {"csrf_token": csrf_token , "error_edit" : True})

				"""----------Now all the input values are valid.---------------"""

				# data formatting.
				edit_first_name = edit_first_name[0].upper() + edit_first_name[1:]
				edit_last_name = edit_last_name[0].upper() + edit_last_name[1:]
				edit_section = edit_section.upper()
				if len(user_class) != 2:
					edit_class = "0" + edit_class

				# backend database working
				class_course_field = backend_handling_functions.auto_assign_course(edit_class, edit_section, "TEACHER")


				try:
					extract_user__user_signup_database.first_name = edit_first_name
					extract_user__user_signup_database.last_name = edit_last_name
					extract_user__user_signup_database.user_class = edit_class
					extract_user__user_signup_database.user_section = edit_section
					extract_user__user_signup_database.user_contact = edit_contact 
					extract_user__user_signup_database.user_r_number = edit_r_number
					extract_user__user_signup_database.school_name = edit_school_name
					extract_user__user_signup_database.save()

					extract_user__user_profile_database.user_signup_db_mapping = extract_user__user_signup_database
					extract_user__user_profile_database.save()
				except:
					"""----------Some error while setting.---------------"""
					return render(request, 'teacher_edit_profile_page.html', {"csrf_token": csrf_token , "error_edit" : True})
				extract_user__user_profile_database.editonce = True
				extract_user__user_profile_database.save()
				"""----------User Succesfully Edited.---------------"""
				return HttpResponse(f'''<body><script>Details are successfully Edited.</script><meta http-equiv="refresh" content='0; url="/profile/"'/></body>''')
		else:
			return render(request, "not_allowed_edit_page.html", {"user_category":extract_user__user_signup_database.user_category, "preview_user": extract_user__user_signup_database, "preview_profile": extract_user__user_profile_database})
	else:
		# session is inactive.
		return HttpResponse(f'''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')
