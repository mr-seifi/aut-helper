from django.db import models
from ..core.models import Student

class Course(models.Model):
    course_name = models.TextField()
    course_unit = models.IntegerField(max_length=1)
    class_date1 = models.DateTimeField()
    class_date2 = models.DateTimeField()
    exam_date = models.DateTimeField()
    student = models.ForeignKey(Student)
    
