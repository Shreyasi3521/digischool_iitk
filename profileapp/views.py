from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context

from loginapp import models as login_models
from profileapp import models as profile_models

from django.middleware import csrf

# NOTE: Every view function (except loginapp.views) must have session token extraction and get "user_id" which is nothing by loginapp.models.USER_SIGNUP_DATABSE.id)
# NOTE: In every view function (except loginapp.views), session token must be validated. Else it should be redirected to loginapp.login_page.

def profilePage(request):
	# getting user_id from session token.
	try:
		integer_check = int(user_id)
	except:
		return HttpResponse('''<body><meta http-equiv="refresh" content='0; url="/login/"'/></body>''')

	extract_user__user_signup_database = login_models.USER_SIGNUP_DATABASE.objects.filter(id=user_id)[0]
	return render(request, "profile_page.html", {"user_id" : profile_models.USER_PROFILE_DATABASE.objects.filter(user_signup_db_mapping=extract_user__user_signup_database)[0]})
