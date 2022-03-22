from django.db import models
from backend_functions.universal_values import *
import os
from digischool.settings import BASE_DIR

class USER_PROFILE_DATABASE(models.Model):
	user_signup_db_mapping = models.OneToOneField("loginapp.USER_SIGNUP_DATABASE", on_delete=models.CASCADE)
	user_profile_photo = models.ImageField(max_length=PROFILE_PIC_PATH_LENGTH, default=os.path.join(BASE_DIR, DEFAULT_PROFILE_PHOTO))