from django.db import models
from core.models import Student


class Book(models.Model):
    title = models.CharField(max_length=255)
    id = models.IntegerField()
    student = models.ManyToManyField(to=Student)

