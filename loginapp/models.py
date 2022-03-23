from django.db import models
from backend_functions.universal_values import *


class USER_SIGNUP_DATABASE(models.Model):
	first_name = models.CharField(max_length=NAME_LIMIT)
	last_name = models.CharField(max_length=NAME_LIMIT)
	
	user_class = models.CharField(max_length=USER_CLASS["class_length"][1])
	user_section = models.CharField(max_length=USER_CLASS["section_length"])
	
	user_contact = models.CharField(max_length=USER_CONTACT["contact_length"][1])
	user_r_number = models.CharField(max_length=R_NUMBER["number_length"][1])

	school_name = models.CharField(max_length=SCHOOL_NAME)
	user_category = models.CharField(max_length=USER_CATEGORY["length_limit"])

	email_address = models.EmailField()
	password = models.CharField(max_length=PASSWORD_LENGTH["length_range"][1])
	verfied_user = models.BooleanField(default=False)
	
	# backend handled.
	class_course_field = models.OneToOneField("courseapp.CLASS_COURSES_MAPPING", on_delete=models.CASCADE) # for teachers it will be "None"

class QUERY_DATABASE(models.Model):
	query_date_time = models.DateTimeField(auto_now_add=True)
	query_email_address = models.EmailField()
	query_url = models.CharField(default=None, max_length=QUERY_URL_LIMIT)
	query_description = models.CharField(max_length=QUERY_DESCRIPTION_LENGTH)

	# backend handled.
	query_resolved = models.BooleanField(default=False)

class OTP_DATABASE(models.Model):
	assigned_email = models.EmailField()
	assigned_OTP = models.CharField(max_length=OTP_LENGTH)
	assigned_time = models.DateTimeField(auto_now_add=True)

class TEACHER_CODE_MAPPING(models.Model):
	teacher_unique_code = models.CharField(max_length=TEACHER_UNIQUE_CODE_LENGTH)
	activation_status = models.BooleanField(default=False)
	teacher_email = models.EmailField()
	teacher_mapping = models.OneToOneField("courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)