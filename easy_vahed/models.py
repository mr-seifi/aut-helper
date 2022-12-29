from django.db import models
from core.models import Student
from day_mapping import persian_day_mapping

class Day(models.Model):
    day = models.IntegerField()
    
    def map_day(self):
        return persian_day_mapping[self.day]
    
    def __str__(self) -> str:
        return self.map_day()
    
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    lecturer = models.CharField(max_length=100)
    days = models.ManyToManyField(Day)
    start_time = models.TimeField()
    end_time = models.TimeField()
    students = models.ManyToManyField(Student,blank=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.lecturer} - {self.days} - {self.start_time} - {self.end_time}'
    
    
    
