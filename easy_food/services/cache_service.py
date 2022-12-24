from _helpers import BaseCacheService
from django.conf import settings


class FoodCacheService(BaseCacheService):
    PREFIX = 'F'
    KEYS = {
        'food': f'{PREFIX}'':{date}',
        'food_price': f'{PREFIX}'':{food}_PRICE'
    }
    EX = settings.REDIS_FOOD_EX

    def cache_foods(self, date, *foods):
        return self._lpush(
            self.KEYS['food'].format(
                date=date
            ),
            *foods
        )

    def get_foods(self, date):
        return self._lrange(
            key=self.KEYS['food'].format(
                date=date
            )
        )

    def cache_food_price(self, food, price):
        return self._set(
            self.KEYS['food_price'].format(food=food),
            price,
        )

    def get_food_price(self, food) -> int:
        return int((self._get(
            self.KEYS['food_price'].format(food=food)
        ) or b'0').decode())
