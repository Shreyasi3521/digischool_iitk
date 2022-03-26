import datetime
import os

NAME_LIMIT = 40
USER_CLASS = {"class_length": [1, 2], "class_range":[1, 12], "section_length": 2, "values":["AS", "BS", "CS","DS"]}
USER_CONTACT = {"contact_length": [10, 11]}
R_NUMBER = {"number_length": [6, 10]}
SCHOOL_NAME = 100
USER_CATEGORY = {"length_limit": 10, "values": ["STUDENT","TEACHER"]}
PASSWORD_LENGTH = {"length_range":[8, 25]} # 25 need to be replaced with the output length of cryptographic technique used.

QUERY_URL_LIMIT = 100
QUERY_DESCRIPTION_LENGTH = 500

PROFILE_PIC_PATH_LENGTH = 200
DEFAULT_PROFILE_PHOTO = 'Templates/default_profile_photo.jpg'

AVAILABLE_SECTIONS = ["AS", "BS", "CS", "DS"]
AVAILABLE_SUBJECTS = ["MA", "SC", "EN", "HI", "SS"]
FULL_NAME = ["Maths", "Science", "English", "Hindi", "Social Studies"]
HIGHEST_CLASS_AVAILABLE = 10
LOWEST_CLASS_AVAILABLE = 6

OFFERING_YEAR = datetime.date.today().year

CLS_COURSE_MAPPING_UNIQUE_ID_LENGTH = 8
COURSE_ID_LENGTH = 10 # format, "sc-cl-cs-ofyr" subject_code:class:section:offeringyear
COURSE_NAME_LENGTH = 100
COURSE_ID_ARRAY_MAX_LENGTH = (len(AVAILABLE_SECTIONS) + 1) * (COURSE_ID_LENGTH + 1)

LECTURE_TITLE_LENGTH = 100
LECTURE_UNIQUE_ID = COURSE_ID_LENGTH + 2

TEST_TITLE_LENGTH = 100
TEST_INSTRUCTION_LENGTH = 100
TEST_UNIQUE_ID = COURSE_ID_LENGTH + 2
FILES_ALLOWED = 10
FILES_STRING_MAX_LENGTH = FILES_ALLOWED * 25


OTP_LENGTH = 8
EMAIL_ADDRESS = "digi.school@yahoo.com"
EMAIL_PASSWORD = "fxejcayvhfwoysdj"
MAIL_SERVER = "smtp.mail.yahoo.com"
PORT = 0
TEACHER_UNIQUE_CODE_LENGTH = 8



FORUM_TITLE_LENGTH = 100
FORUM_QUES_LEN = 500