from django.db import models
from backend_functions.universal_values import *


# backend database (already filed.)
class CLASS_COURSES_MAPPING(models.Model):
	unique_id = models.CharField(max_length=CLS_COURSE_MAPPING_UNIQUE_ID_LENGTH) # format "class:section:offeringyear"
	course_id_array = models.CharField(max_length=COURSE_ID_ARRAY_MAX_LENGTH) # an array represented as string, where, each element is a course_id which is nothing but courseapp.AVALIABLE_COURSES course_id.


class AVAILABLE_COURSES(models.Model):
	course_id = models.CharField(max_length=COURSE_ID_LENGTH) # format, "sc-cl-cs-ofyr" subject_code:class:section:offeringyear
	course_instructor = models.OneToOneField("loginapp.USER_SIGNUP_DATABASE", on_delete=models.CASCADE)
	course_name = models.CharField(max_length=COURSE_NAME_LENGTH)
	lecture_series_number = models.IntegerField(default=0) # Needs to be updated whenever new lecture added # Backend handlingI
	test_series_number = models.IntegerField(default=0) # Same.