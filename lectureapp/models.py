from django.db import models
from backend_functions.universal_values import *
from courseapp.models import *

class ALL_LECTURES(models.Model):
	lecture_title = models.CharField(max_length=LECTURE_TITLE_LENGTH)
	yt_link_unique_id = models.URLField()
	lecture_unique_id = models.CharField(max_length=LECTURE_UNIQUE_ID) # "course_id(10):lecture_series_number(2)"
	course_mapping = models.ForeignKey(AVAILABLE_COURSES, on_delete=models.CASCADE)