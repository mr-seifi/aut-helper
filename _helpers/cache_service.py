from django.core.cache import caches
from redis import Redis


class BaseCacheService:
    PREFIX = ''
    KEYS = {

    }
    EX = 0

    @staticmethod
    def _get_redis_client() -> Redis:
        return caches['default'].client.get_client()
