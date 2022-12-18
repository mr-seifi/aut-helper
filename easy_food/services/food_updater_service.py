from . import FoodCacheService
from random import sample
from easy_food.enums import FoodChoices
from django.utils import timezone


class FoodUpdaterService:

    @classmethod
    def _get_available_from_aut(cls):
        return list(map(lambda x: x[0], sample(FoodChoices.choices, len(FoodChoices.choices))))

    @classmethod
    def get_daily_available_foods(cls, cache=True):
        cache_service = FoodCacheService()

        _today = timezone.now().date()
        cached_foods = cache_service.get_foods(date=_today)
        if cached_foods:
            return cached_foods

        selected_foods = cls._get_available_from_aut()
        if not cache:
            return selected_foods

        cache_service.cache_foods(_today, selected_foods)
        return selected_foods
