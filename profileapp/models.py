from django.db import models
import loginapp.models
from backend_functions.universal_values import *

class USER_PROFILE_DATABASE(models.Model):
	user_signup_db_mapping = models.OneToOneField(loginapp.models.USER_SIGNUP_DATABASE, on_delete=models.CASCADE)
	user_profile_photo = models.ImageField(max_length=PROFILE_PIC_PATH_LENGTH, default=os.path.join(BASE_DIR, DEFAULT_PROFILE_PHOTO))