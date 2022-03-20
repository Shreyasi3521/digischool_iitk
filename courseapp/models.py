from django.db import models
from digischool import univeral_values as *
from loginapp import models as login_models
from lectureapp import models as lecture_models
from testapp import models as test_models

# backend database (already filed.)

class AVAILABLE_COURSES(models.Model):
	course_id = models.CharField(max_length=COURSE_ID_LENGTH) # format, "sc-cl-cs-ofyr" subject_code:class:section:offeringyear
	course_instructor = models.OneToOneField(login_models.USER_SIGNUP_DATABASE)
	course_name = models.CharField(max_length=COURSE_NAME_LENGTH)
	lecture_series_number = models.IntegerField() # Needs to be updated whenever new lecture added # Backend handlingI
	test_series_number = models.IntegerField() # Same.
class CLASS_COURSES_MAPPING(models.Model):
	unique_id = models.CharField(max_length=CLS_COURSE_MAPPING_UNIQUE_ID_LENGTH)
	course_id_array = models.CharField(max_length=COURSE_ID_ARRAY_MAX_LENGTH) # an array represented as string, where, each element is a course_id which is nothing but courseapp.AVALIABLE_COURSES course_id.
	