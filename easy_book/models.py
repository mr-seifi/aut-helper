from django.db import models
from core.models import Student
from uuid import uuid4


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    uid = models.UUIDField(default=uuid4, db_index=True)
    author = models.CharField(max_length=255, db_index=True, null=True)
    publisher = models.CharField(max_length=255, null=True)
    is_exist = models.BooleanField(default=False)
    year = models.CharField(max_length=64, null=True)
    cover = models.ImageField(upload_to='asset', null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.author}'
