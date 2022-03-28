import csv, os
from random import randrange
from .universal_values import *
from courseapp import models as course_models
from loginapp import models as login_models



def code_generate():
    start = 10 ** (8 - 1)
    end = 10 ** (8)
    value_secret = str(randrange(start, end))
    return value_secret

# creating TEACHER_CODE_MAPPING
# in production it will be a csv file coming from school.
def get_teacher_class_data(prev_class, prev_section, prev_subject):
    if prev_subject == len(AVAILABLE_SUBJECTS) - 1:
        prev_section += 1
        prev_subject = 0
        if prev_section ==  len(AVAILABLE_SECTIONS):
            prev_class += 1
            prev_section = 0
            prev_subject = 0
    else:
        prev_subject += 1
    return prev_class, prev_section, prev_subject

def populate_teacher():
    entries = (HIGHEST_CLASS_AVAILABLE - LOWEST_CLASS_AVAILABLE + 1) * len(AVAILABLE_SECTIONS) *  len(AVAILABLE_SUBJECTS)
    
    with open('Indian_Names.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        count_entries_created = 0
        jumper = 0 # random index generator
        step = randrange(40, 85) # random step generator
        class_index, section_index, subject_index = LOWEST_CLASS_AVAILABLE, 0, 0
        for row in reader:
            if jumper != step:
                jumper += 1
            else:
                jumper = 0
                step = randrange(40, 80)
                unique_code = code_generate()
                while len(login_models.TEACHER_CODE_MAPPING.objects.filter(teacher_unique_code=unique_code)) != 0:
                    unique_code = code_generate()

                test_email = row["Name"] + "@" + 'example.com'
                assigned_class = str(class_index) if len(str(class_index)) == 2 else "0" + str(class_index)
                assigned_section = AVAILABLE_SECTIONS[section_index]
                assigned_subject = AVAILABLE_SUBJECTS[subject_index]
                
                class_index, section_index, subject_index = get_teacher_class_data(class_index, section_index, subject_index)
                
                # just to create a v10 BS SCalid entry
                if assigned_class == "10" and assigned_section == "BS" and assigned_subject=="SC":
                    test_email = "sumit.nagle@gmail.com"

                setting_entry = login_models.TEACHER_CODE_MAPPING(teacher_email=test_email, teacher_unique_code=unique_code, teacher_assigned_class=assigned_class, teacher_assigned_section=assigned_section, teacher_assigned_subject= assigned_subject)
                setting_entry.save()
                print(count_entries_created, unique_code, test_email, assigned_class, assigned_section, assigned_subject)
                count_entries_created += 1
                if count_entries_created == entries:
                    break

def populate_courses():
    entries = (HIGHEST_CLASS_AVAILABLE - LOWEST_CLASS_AVAILABLE + 1) * len(AVAILABLE_SECTIONS) *  len(AVAILABLE_SUBJECTS)
    class_index, section_index, subject_index = LOWEST_CLASS_AVAILABLE, 0, 0
    count_entries_created = 0
    while True:
        class_to_choose = str(class_index) if len(str(class_index)) == 2 else "0" + str(class_index)
        course_id = AVAILABLE_SUBJECTS[subject_index] + str(class_to_choose) + AVAILABLE_SECTIONS[section_index] + str(OFFERING_YEAR)

        

        mapped_teacher = login_models.TEACHER_CODE_MAPPING.objects.get(teacher_assigned_class=class_to_choose, teacher_assigned_section=AVAILABLE_SECTIONS[section_index], teacher_assigned_subject=AVAILABLE_SUBJECTS[subject_index])

        course_name = FULL_NAME[subject_index]
        print(count_entries_created, AVAILABLE_SUBJECTS[subject_index], str(class_to_choose), AVAILABLE_SECTIONS[section_index])
        class_index, section_index, subject_index = get_teacher_class_data(class_index, section_index, subject_index)
        setting_course = course_models.AVAILABLE_COURSES(course_id=course_id, course_instructor=mapped_teacher, course_name=course_name)
        setting_course.save()

        count_entries_created += 1
        if count_entries_created == entries:
            break

def populate_class_course_map():
    entries = (HIGHEST_CLASS_AVAILABLE - LOWEST_CLASS_AVAILABLE + 1) * len(AVAILABLE_SECTIONS) *  len(AVAILABLE_SUBJECTS)
    class_index, section_index, subject_index = LOWEST_CLASS_AVAILABLE, 0, 0
    entry_done = list()
    count_entries_created = 0
    while True:
        class_to_choose = str(class_index) if len(str(class_index)) == 2 else "0" + str(class_index)
        
        unique_id = str(class_to_choose) + AVAILABLE_SECTIONS[section_index] + str(OFFERING_YEAR)
        
        MODIFIED_SUBJECTS = [ str(AVAILABLE_SUBJECTS[i] + unique_id) for i in range(len(AVAILABLE_SUBJECTS))]

        course_id_array = " ".join(MODIFIED_SUBJECTS)
        course_id_array.strip()


        if not unique_id in entry_done:
            setting_class_course_map = course_models.CLASS_COURSES_MAPPING(unique_id=unique_id,course_id_array=course_id_array)
            setting_class_course_map.save()
            print(count_entries_created, unique_id, MODIFIED_SUBJECTS)
        
        class_index, section_index, subject_index = get_teacher_class_data(class_index, section_index, subject_index)
        

        entry_done.append(unique_id)

        
        count_entries_created += 1
        if count_entries_created == entries:
            break