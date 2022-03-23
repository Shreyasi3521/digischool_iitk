from courseapp import models as course_models
from . import universal_values

def auto_assign_course(user_cls, user_sec, user_category):
	if user_category == "STUDENT":
		unique_id = user_cls + user_sec + str(universal_values.OFFERING_YEAR)
		class_course_mapping_entry = course_models.CLASS_COURSES_MAPPING.objects.filter(unique_id=unique_id)[0]
		return class_course_mapping_entry
	if user_category == "TEACHER":
		# maybe create a null entry.
		return None

def course_instructor_assigning(teacher_entry):
	## subject_code, coming from a csv file where we uses teachers:sc:otp mapping.	
	course_unique_id = subject_code + teacher_entry.user_class + teacher_entry.user_section + str(OFFERING_YEAR)
	selected_course = course_models.AVAILABLE_COURSES.objects.filter(course_id=course_unique_id)[0]
	selected_course.course_instructor = teacher_entry
	selected_course.save()

