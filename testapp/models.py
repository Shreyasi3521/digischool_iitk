from django.db import models
import courseapp.models
from backend_functions.universal_values import *

class ALL_TESTS(models.Model):
	test_title = models.CharField(max_length=TEST_TITLE_LENGTH)
	test_instruction = models.CharField(max_length=TEST_INSTRUCTION_LENGTH)
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField() # NOTE: In views we need to use "datetime module" such as start = datetime(incoming input)
	files = models.FileField(max_length=FILES_STRING_MAX_LENGTH) # an array represented as string, where, each element is file path
	test_unique_id = models.CharField(max_length=TEST_UNIQUE_ID) # "course_id(10):test_series_number(2)"
	course_mapping = models.ForeignKey(courseapp.models.AVAILABLE_COURSES)