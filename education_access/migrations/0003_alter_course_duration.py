# Generated by Django 5.1.6 on 2025-03-21 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_access', '0002_course_duration_course_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.IntegerField(default=6, help_text='Duration in weeks'),
        ),
    ]