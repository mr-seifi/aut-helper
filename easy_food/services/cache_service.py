from _helpers import BaseCacheService
from django.conf import settings


class FoodCacheService(BaseCacheService):
    PREFIX = 'F'
    KEYS = {
        'food': f'{PREFIX}'':{date}'
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
