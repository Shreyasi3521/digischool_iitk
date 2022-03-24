from random import randrange # more strong random value generator is required.
from backend_functions.universal_values import *
from loginapp.models import OTP_DATABASE, TEACHER_CODE_MAPPING
import smtplib
import os


def otp_generate():
	start = 10 ** (OTP_LENGTH - 1)
	end = 10 ** (OTP_LENGTH)
	OTP_value_secret = str(randrange(start, end))
	return OTP_value_secret


def send_mail(to_email, OTP_value):
	internal_network = ["iitk.ac.in"]
	try:
		if to_email.split("@")[1] in internal_network:
			mail_server = "smtp.cc.iitk.ac.in"
		else:
			mail_server = "mmtp.iitk.ac.in"
		with  smtplib.SMTP(mail_server) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.ehlo()

			smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
			
			subject = "OTP(One-time-Password) for digischool signup verification | digischool"
			body = "The user otp is: " + OTP_value + "\nIt is valid only for 10 minutes."
			msg = f'From: {EMAIL_ADDRESS}\nTo: {to_email}\nSubject: {subject}\n\n{body}'
			smtp.sendmail(EMAIL_ADDRESS, to_email, msg)
			
			if len(OTP_DATABASE.objects.filter(assigned_email=to_email)) > 0:
				selected_user = OTP_DATABASE.objects.filter(assigned_email=to_email)[0]
				selected_user.assigned_OTP = OTP_value
				selected_user.save()
			else:
				setting_entry = OTP_DATABASE(assigned_email=to_email, assigned_OTP=OTP_value)
				setting_entry.save()
			return True
	except:
		return False

def check_otp(email, received_otp, user_category):
	if user_category == "STUDENT":
		database_otp = OTP_DATABASE.objects.filter(assigned_email=email)[0].assigned_OTP
	else:
		database_otp = TEACHER_CODE_MAPPING.objects.filter(teacher_email=to_email)[0].teacher_unique_code
	if not (len(database_otp) > 0):
		return False
	return database_otp == received_otp

def otp_sending_handling(to_email, user_category):
	if user_category == "STUDENT":
		otp = otp_generate()
	else:
		otp = TEACHER_CODE_MAPPING.objects.filter(teacher_email=to_email)[0].teacher_unique_code
	status_email = send_mail(to_email, otp)
	return status_email

def otp_receiving_handling(to_email, received_otp, user_category):
	return check_otp(to_email, received_otp, user_category)
