from django.core.cache import caches
from django.conf import settings
from redis import Redis


class BaseCacheService:
    PREFIX = ''
    KEYS = {

    }
    EX = settings.REDIS_DEFAULT_EX

    @property
    def _client(self) -> Redis:
        return caches['default'].client.get_client()

    def _set(self, key, val):
        return self._client.set(key, val, ex=self.EX)

    def _get(self, key):
        return self._client.get(key)
