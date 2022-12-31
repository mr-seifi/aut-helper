from celery import app
from .services import FoodUpdaterService, FoodCacheService
from .enums import FoodChoices


@app.shared_task
def update_foods_price():
    updater_service = FoodUpdaterService()
    cache_service = FoodCacheService()

    for food in FoodChoices.labels:
        price = updater_service.get_food_prices(food)
        cache_service.cache_food_price(food=food,
                                       price=price)
