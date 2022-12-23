from django.db import models
from ..core.models import Student

class Course(models.Model):
    name = models.CharField()
    unit = models.IntegerField(max_length=1)
    # not sure for class dates 
    class_date1 = models.DateTimeField()
    class_date2 = models.DateTimeField()
    exam_date = models.DateTimeField()
    students = models.ManyToManyField(Student)
    
    def __str__(self) -> str:
        return self.name
    
