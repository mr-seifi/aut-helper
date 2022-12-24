from django.db import models


class TransactionChoices(models.TextChoices):
    DEPOSIT = 'd', 'واریز'
    WITHDRAW = 'w', 'برداشت'
