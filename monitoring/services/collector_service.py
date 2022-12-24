from core.models import Student
from payment.models import Transaction
from django.utils import timezone


class CollectorService:

    def __init__(self):
        ...

    @classmethod
    def collect_unique_student_within_hour(cls) -> int:
        return Student.objects.filter(
            created__gt=timezone.now() - timezone.timedelta(hours=1)
        ).count()

    @classmethod
    def collect_all_unique_students(cls) -> int:
        return Student.objects.count()

    @classmethod
    def collect_unique_trxs_within_hour(cls) -> int:
        return Transaction.objects.filter(
            created__gt=timezone.now() - timezone.timedelta(hours=1)
        ).count()

    @classmethod
    def collect_all_unique_trxs(cls) -> int:
        return Transaction.objects.count()
