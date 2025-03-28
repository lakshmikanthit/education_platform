from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(default=6, help_text="Duration in weeks")  # ✅ Default value

    def __str__(self):
        return self.title