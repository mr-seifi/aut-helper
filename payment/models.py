from django.db import models
from uuid import uuid4
from core.models import Student


class Transaction(models.Model):
    tx_hash = models.UUIDField(default=uuid4)
    student = models.ForeignKey(to=Student, on_delete=models.DO_NOTHING)
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
