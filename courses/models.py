from django.db import models
from django.conf import settings  # Import settings to get AUTH_USER_MODEL

class Instructor(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(default=60)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True,blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
