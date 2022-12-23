from . import FoodCacheService
from random import sample
from easy_food.enums import FoodChoices
from django.utils import timezone


class FoodUpdaterService:

    @classmethod
    def _get_available_from_aut(cls):
        return list(map(lambda x: x[1], sample(FoodChoices.choices, 1)))[0]

    @classmethod
    def get_daily_available_foods(cls, date=timezone.now().date(), cache=True):
        cache_service = FoodCacheService()

        _today = date
        cached_foods = cache_service.get_foods(date=_today)
        if cached_foods:
            return cached_foods[0].decode()

        selected_foods = cls._get_available_from_aut()
        if not cache:
            return selected_foods

        cache_service.cache_foods(_today, selected_foods)
        return selected_foods

    @classmethod
    def get_a_food_cycle(cls, cache=True):
        _dates = [timezone.now().date() + timezone.timedelta(days=i) for i in range(7)]

        return {date.weekday(): cls.get_daily_available_foods(date=date,
                                                              cache=cache)
                for date in _dates}
