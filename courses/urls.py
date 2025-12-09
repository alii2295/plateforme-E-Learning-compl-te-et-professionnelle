from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/<slug:slug>/edit/', views.edit_course, name='edit_course'),
    path('course/<slug:slug>/delete/', views.delete_course, name='delete_course'),
]