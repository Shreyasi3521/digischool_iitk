from courseapp import models as course_models
from . import universal_values
from loginapp import models as login_models

def auto_assign_course(user_cls, user_sec, user_category):
	if user_category == "STUDENT":
		unique_id = user_cls + user_sec + str(universal_values.OFFERING_YEAR)
		class_course_mapping_entry = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=unique_id)[0]
		return class_course_mapping_entry
	if user_category == "TEACHER":
		return None

def removing_entries():
	pass
	# remove loginapp.models.USER_SIGNUP_DATABASE entries if user is not verfied and time is excceded by 2 (ALLOWED_ENTRY_TIME) days.