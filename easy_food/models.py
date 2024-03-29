from django.db import models
from core.models import Student
from .enums import FoodChoices


class Food(models.Model):
    name = models.CharField(max_length=128, choices=FoodChoices.choices)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    reserved_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
