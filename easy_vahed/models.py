from django.db import models
from core.models import Student

class Day(models.Model):
    day = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.day
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    lecturer = models.CharField(max_length=100)
    # needs improvment
    students = models.ManyToManyField(Student,blank=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.lecturer}'
    
class Time(models.Model):
    day = models.ManyToManyField(Day,blank=True)
    start_time = models.FloatField()
    end_time = models.FloatField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.day} -> {self.start_time} - {self.end_time}'
    
    
