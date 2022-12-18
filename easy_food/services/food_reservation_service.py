from easy_food.models import Food


class FoodReservationService:

    @classmethod
    def reserve_food(cls, student_id: int, food, reserve_date):
        return Food.objects.create(
            student_id=student_id,
            name=food,
            reserved_date=reserve_date
        )

    @classmethod
    def get_all_reserved_food(cls, date):
        return Food.objects.filter(
            reserved_date=date
        )
