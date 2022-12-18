from django.db import models
from core.models import Student


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=128, unique=True, db_index=True)
    row = models.CharField(max_length=8)
    col = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
