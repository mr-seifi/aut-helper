from core.models import Student
from django.conf import settings
from django.db import transaction
from _helpers import NotEnoughBalance
from .models import Transaction


class PaymentService:

    @classmethod
    @transaction.atomic
    def make_transaction(cls, price: int, student_id):
        student = Student.objects.get(student_id__exact=student_id)
        if int(student.balance) - int(price) < settings.MINIMUM_STUDENT_BALANCE:
            raise NotEnoughBalance

        student.balance -= price
        student.save()

        return Transaction.objects.create(
            price=price,
            student_id=student.id
        )
