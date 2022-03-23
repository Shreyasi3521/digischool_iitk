import csv
from courseapp import models as course_models
from .universal_values import *
from loginapp import models as login_models


def code_generate():
    start = 10 ** (OTP_LENGTH - 1)
    end = 10 ** (OTP_LENGTH)
    value_secret = str(randrange(start, end))
    return value_secret

def populate_teacher():
    entries = (HIGHEST_CLASS_AVAILABLE - LOWEST_CLASS_AVAILABLE + 1) * len(AVAILABLE_SECTIONS) *  len(AVAILABLE_SUBJECTS)
    with open('teacher_email_database.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            count += 1
            unique_code = code_generate()
            while len(login_models.TEACHER_CODE_MAPPING.objects.filter(teacher_unique_code=unique_code)) != 0:
                unique_code = code_generate()
            test_email = row["first_name"] + "@" + 'example.com'
            if count == entries:
                break
            TEACHER_CODE_MAPPING(dfasfasdf= f adsf= fdaf)
            .save()


with open('available_course.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    for class_int in range(LOWEST_CLASS_AVAILABLE, HIGHEST_CLASS_AVAILABLE + 1):
        for class_section in range(0, len(AVAILABLE_SECTIONS)):
            for subjecti in range(0, len(AVAILABLE_SUBJECTS)):
                if class_int <= 9:
                    class_int_str = "0" + str(class_int)
                else:
                    class_int_str = str(class_int)
                course_id = AVAILABLE_SUBJECTS[subjecti] + class_int_str + AVAILABLE_SECTIONS[class_section] + str(OFFERING_YEAR)
                course_name = class_int_str + " " +  AVAILABLE_SECTIONS[class_section] + ": " + FULL_NAME[subjecti]
                course_models.AVAILABLE_COURSES(course_id=course_id, course_name)
                thewriter.writerow(
                    [unique, 'teachername', subject[subjecti], '0', '0'])
