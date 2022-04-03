from django.db import models
from backend_functions.universal_values import *


# backend database (already filed.)
class CLASS_COURSES_MAPPING(models.Model):
	unique_id = models.CharField(max_length=CLS_COURSE_MAPPING_UNIQUE_ID_LENGTH) # format "class:section:offeringyear"
	course_id_array = models.CharField(max_length=COURSE_ID_ARRAY_MAX_LENGTH) # an array represented as string, where, each element is a course_id which is nothing but courseapp.AVALIABLE_COURSES course_id.

"""unique_id = "06AS2020"
course_id = "MA06AS2020 SC06AS2020 SS06AS2020 HI06AS20202 EN06AS2020"
"""
class AVAILABLE_COURSES(models.Model):
	course_id = models.CharField(max_length=COURSE_ID_LENGTH) # format, "sc-cl-cs-ofyr" subject_code:class:section:offeringyear
	course_instructor = models.OneToOneField("loginapp.TEACHER_CODE_MAPPING", on_delete=models.CASCADE)
	course_name = models.CharField(max_length=COURSE_NAME_LENGTH)
	lecture_series_number = models.IntegerField(default=0) # Needs to be updated whenever new lecture added # Backend handlingI
	test_series_number = models.IntegerField(default=0) # Same.
	forum_series_number = models.IntegerField(default=0) # Same.
	news_series_number = models.IntegerField(default=0) # Same.

class ALL_ANOUNCEMENT(models.Model):
	news_title = models.TextField()
	news_description = models.TextField() 
	news_datetime = models.DateTimeField(auto_now=True) # upload date.
	news_unique_id = models.CharField(max_length=TEST_UNIQUE_ID) # "course_id(10):forum_series_number(2)"
	course_mapping = models.ForeignKey("courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)