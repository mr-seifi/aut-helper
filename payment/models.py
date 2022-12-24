from django.db import models
from uuid import uuid4
from core.models import Student
from .enums import TransactionChoices


class Transaction(models.Model):
    tx_hash = models.UUIDField(default=uuid4)
    student = models.ForeignKey(to=Student, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=2, choices=TransactionChoices.choices, default=TransactionChoices.WITHDRAW)
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tx_hash[:6]}|{self.created}|{self.price:,} Toman'
