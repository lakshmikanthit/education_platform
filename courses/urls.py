# courses/urls.py
from django.urls import path
from .views import course_list, course_detail  # Import your views

urlpatterns = [
    path("", course_list, name="courses"),  # ✅ List all courses
    path("<int:course_id>/", course_detail, name="course_detail"),  # ✅ View a single course
]