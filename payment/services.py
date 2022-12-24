from core.models import Student
from django.conf import settings
from django.db import transaction
from _helpers import NotEnoughBalance
from .models import Transaction


class PaymentService:

    @classmethod
    @transaction.atomic
    def make_transaction(cls, price: int, student_id, transaction_type='w'):
        student = Student.objects.get(student_id__exact=student_id)

        if transaction_type == 'w':  # TODO: State pattern
            if int(student.balance) - int(price) < settings.MINIMUM_STUDENT_BALANCE:
                raise NotEnoughBalance

            student.balance -= int(price)
            student.save()

        elif transaction_type == 'd':
            student.balance += int(price)
            student.save()

        return Transaction.objects.create(
            price=price,
            student_id=student.id,
            type=transaction_type
        )

    @classmethod
    def get_student_transactions(cls, student_id):
        return Transaction.objects.filter(
            student__student_id__exact=student_id
        )
