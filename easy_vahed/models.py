from django.db import models
from core.models import Student

class Course(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    lecturer = models.CharField(max_length=100)
    # needs improvment
    students = models.ManyToManyField(Student,blank=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.lecturer}'
    
class ClassTime(models.Model):
    day = models.CharField(max_length=100)
    start_time = models.FloatField()
    end_time = models.FloatField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

class ExamTime(ClassTime):
    date = models.DateField()
