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

    def _lpush(self, key, *vals):
        return self._client.lpush(key, *vals)

    def _lrange(self, key, l=0, r=-1):
        return self._client.lrange(key, l, r)
