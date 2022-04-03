from django.db import models
from backend_functions.universal_values import *

class ALL_LECTURES(models.Model):
	lecture_title = models.CharField(max_length=LECTURE_TITLE_LENGTH)
	lecture_datetime = models.DateTimeField(auto_now=True) # upload date.
	lecture_unique_id = models.CharField(max_length=LECTURE_UNIQUE_ID) # "course_id(10):lecture_series_number(2)"
	course_mapping = models.ForeignKey("courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)
	video_server_name = models.FileField(upload_to="videos/", null=True, verbose_name="")
	files = models.FileField(upload_to="lecturefiles/", null=True, verbose_name="")
