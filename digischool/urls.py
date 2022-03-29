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
from django.conf import settings
from django.conf.urls.static import static
from lectureapp import views as lecture_views
from forumapp import views as forum_views
from courseapp import views as course_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # These are all related to login system.
    path("signup/", login_views.signUpPage),
    path("signup/status/", login_views.signUpPosted),
    path("signup/verify/", login_views.signupOTPVerfied),
    path("resend/", login_views.resendOTPVerify),
    path("login/", login_views.loginPage),
    path("login/check/", login_views.loginPageCheck),
    path("logout/", login_views.logoutPage),
    path("contact/", login_views.contactPage),
    path("contact/submit/", login_views.contactPageSubmitted),


    path("profile/", profile_views.profilePage),
    path("profile/edit/", profile_views.editProfilePage),
    path("profile/edit/status/", profile_views.editProfilePagePosted),

    # all test related things
    path("test/", test_views.testPage),
    path("test/view/<str:given_unique_id>", test_views.eachTestView),
    path("test/upload/", test_views.testUploaded),
    path("test/create/<str:course_id_to_upload>", test_views.createPage),
    path("test/submit/<str:test_unique_id>", test_views.answerUpload),
    path("test/edit/<str:test_unique_id>", test_views.editTestPage),
    path("test/edit/upload/<str:test_unique_id>", test_views.editTestUpload),
    path("test/answer/<str:test_unique_id>", test_views.answerCheckPage),
    path("test/answer/save/<str:test_unique_id>", test_views.scoreUpload),

    # all lectures related things
    path("lecture/", lecture_views.lecturePage),
    path("lecture/view/<str:given_unique_id>", lecture_views.eachLectures),
    path("lecture/create/<str:course_id_to_upload>", lecture_views.createPage),
    path("lecture/upload/", lecture_views.lectureUploaded),
    path("lecture/edit/<str:lecture_unique_id>", lecture_views.editLecturePage),
    path("lecture/edit/upload/<str:lecture_unique_id>", lecture_views.editLectureUpload),
    
    # all forum related things
    path("forum/", forum_views.forumPage),
    path("forum/create/<str:course_id_to_upload>", forum_views.createPage),
    path("forum/upload/", forum_views.forumUploaded),
    path("forum/view/<str:given_unique_id>", forum_views.eachForumView),
    path("forum/submit/<str:forum_unique_id>", forum_views.forumAnswerUpload),

    # all announcement related things.
    path("news/", course_views.newsPage),
    path("news/create/<str:course_id_to_upload>", course_views.createPage),
    path("news/upload/", course_views.newsUploaded),
    path("news/edit/<str:news_unique_id>", course_views.editNewsPage),
    path("news/edit/upload/<str:news_unique_id>", course_views.editNewsUpload),



    path("", login_views.homePage) # keep this in last.
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)