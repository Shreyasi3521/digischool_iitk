import re
import datetime

def titleCheck(value):
    value = value.strip()
    return len(value) <= 100 and len(value) >= 10

def instructionCheck(value):
    value = value.strip()
    return len(value) <= 500 and len(value) >= 50

def dateCheck(value):
    value = value.strip()
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d')
        today = datetime.date.today()
        return dt.year==today.year or dt.year==today.year+1
    except ValueError:
        return False

def timeCheck(value):
    value = value.strip()
    try:
        datetime.datetime.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False

def filenameCheck(value):
    value = value.strip()
    if len(value)>50:
        return False
    regex = r'[a-z0-9 \\\/]+\.[a-z]{3}'
    if not re.fullmatch(regex, value):
        return False
    ext = value.split('.')[-1]
    return ext in ["jpg","png","pdf"]

def marksCheck(value):
    value = value.strip()
    if not value.isnumeric():
        return False
    num = int(value)
    return num<=100 and num>=0