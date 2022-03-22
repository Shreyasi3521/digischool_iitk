"""digischool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loginapp import views as login_views
from profileapp import views as profile_views
from testapp import views as test_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/", login_views.signUpPage),
    path("signup/status/", login_views.signUpPosted),
    path("login/", login_views.loginPage),
    path("login/check/", login_views.loginPageCheck),
    path("contact/", login_views.contactPage),
    path("contact/submit/", login_views.contactPageSubmitted),
    path("profile/", profile_views.profilePage),
    path("test/", test_views.testPage),
    path("test/view/<int:unique_id", test_views.eachTestView),
    path("test/upload/", test_views.testUploaded),
    path("", login_views.homePage) # keep this in last.
]
