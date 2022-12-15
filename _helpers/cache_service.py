from django.core.cache import caches
from redis import Redis


class BaseCacheService:
    PREFIX = ''
    KEYS = {

    }
    EX = 0


