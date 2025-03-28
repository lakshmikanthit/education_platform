from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Admin URLs
    path('course/add/', views.add_course, name='add_course'),
    path('instructor/add/', views.add_instructor, name='add_instructor'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
]