from django.db import models


class FoodChoices(models.TextChoices):
    pizza = 'pizza', 'پیتزا'
    burger = 'burger', 'برگر'
    chicken = 'chicken', 'مرغ'