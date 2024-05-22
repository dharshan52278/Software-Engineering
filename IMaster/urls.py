from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("", views.info, name="info"),
    path("signup/", views.signup, name="signup"),

    #course
    path("view_course/<int:course_id>", views.view_course, name="view_course"),
    path('course/<int:course_id>/', views.view_course, name='view_course'),
    path('course/<int:course_id>/mark_topic_complete/<int:topic_id>/', views.mark_topic_complete, name='mark_topic_complete'),
    path('course/<int:course_id>/topic/<int:topic_id>/complete/', views.mark_topic_complete, name='mark_topic_complete'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('enrolled-courses/', views.enrolled_courses, name='enrolled_courses'),
    path('course_overview/<int:course_id>/', views.course_overview, name="course_overview"),

    #timetable
    path('timetable/', views.timetable, name="timetable"),
    path('timetable/cse/', views.cse_timetable, name='cse_timetable'),
    path('timetable/it/', views.it_timetable, name='it_timetable'),

    #admin
    path("admins/", views.admins, name="admins"),
    path("base/", views.base, name="base"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)