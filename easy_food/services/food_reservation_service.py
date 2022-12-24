from easy_food.models import Food
from easy_food.services import FoodCacheService
from payment.services import PaymentService
from core.models import Student


class FoodReservationService:

    @classmethod
    def reserve_food(cls, student_id: int, food, reserve_date):
        payment_service = PaymentService()
        food_cache_service = FoodCacheService()
        food_price = food_cache_service.get_food_price(food=food)
        student = Student.objects.filter(student_id__exact=student_id).first()

        payment_service.make_transaction(price=food_price,
                                         student_id=student_id)
        return Food.objects.create(
            student_student_id=student.id,
            name=food,
            reserved_date=reserve_date
        )

    @classmethod
    def get_all_reserved_food(cls, date):
        return Food.objects.filter(
            reserved_date=date
        )
