from django.db import models
from loginapp import models as login_models
from digischool import univeral_values as *

class USER_PROFILE_DATABASE(models.Model):
	user_signup_db_mapping = models.OneToOneField(login_models.USER_SIGNUP_DATABASE, on_delete=models.CASCADE)
	user_profile_photo = models.ImageField(max_length=PROFILE_PIC_PATH_LENGTH, default=os.path.join(BASE_DIR, DEFAULT_PROFILE_PHOTO))