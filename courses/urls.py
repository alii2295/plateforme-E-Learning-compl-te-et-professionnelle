from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course//', views.course_detail, name='course_detail'),
    path('course//enroll/', views.enroll_course, name='enroll_course'),
    path('course//comment/', views.add_comment, name='add_comment'),
    path('course//lesson//', views.lesson_detail, name='lesson_detail'),
    path('my-courses/', views.my_courses, name='my_courses'),
]