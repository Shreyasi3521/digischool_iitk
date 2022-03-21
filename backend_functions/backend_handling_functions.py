from courseapp import models as course_models
from digischool import univeral_values as *

def auto_assign_course(user_cls, user_sec):
	unique_id = user_cls + user_sec + str(OFFERING_YEAR)
	class_course_mapping_entry = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=unique_id)[0]
	return class_course_mapping_entry
