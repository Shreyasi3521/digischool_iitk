from django.db import models
from backend_functions.universal_values import *

class ALL_LECTURES(models.Model):
	lecture_title = models.CharField(max_length=LECTURE_TITLE_LENGTH)
	yt_link_unique_id = models.URLField()
	lecture_unique_id = models.CharField(max_length=LECTURE_UNIQUE_ID) # "course_id(10):lecture_series_number(2)"
	course_mapping = models.ForeignKey("courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)

class ALL_VIDEO(models.Model):
	connected_lecture = models.OneToOneField(ALL_LECTURES, on_delete=models.CASCADE)
	video_server_name = models.FileField(upload_to="videos/", null=True, verbose_name="")