from django.db import models
from backend_functions.universal_values import *

# Create your models here.
class ALL_FORUMS(models.Model):
	forum_title = models.TextField()
	forum_question = models.TextField() # file path # json format {"question" : "question content", "upvote counter"}
	forum_datetime = models.DateTimeField(auto_now_add=True) # upload date.
	forum_unique_id = models.CharField(max_length=TEST_UNIQUE_ID) # "course_id(10):forum_series_number(2)"
	course_mapping = models.ForeignKey("courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)
	forum_answers = models.TextField() #{"1" : {} , 2: . .. # json format {"answer1": "answer content", "date_answer": "datetime string" , "user" : "loginapp.USER_SIGNUPUP_DATABASE.id", "upvotecounter": value (negative means more downvotes)}