from django.contrib import admin
from .models import Course, Enrollment  # Import both models

admin.site.register(Course)
admin.site.register(Enrollment)  # Register Enrollment model
