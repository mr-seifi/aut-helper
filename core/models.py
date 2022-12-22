from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=32, unique=True, db_index=True)
    phone_number = models.CharField(max_length=20)
    enter_year = models.IntegerField()
    balance = models.IntegerField(default=0)
    average = models.FloatField(default=0)
