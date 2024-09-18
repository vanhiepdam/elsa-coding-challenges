import redis
import redis_lock
from django.conf import settings


class RedisClient(redis.Redis):
    def __init__(self, **kwargs):
        super().__init__(host=settings.CACHE_URL, port=6379, db=0, **kwargs)


class RedisLock(redis_lock.Lock):
    def __init__(self, key: str, **kwargs):
        client = RedisClient()
        super().__init__(redis_client=client, name=key, **kwargs)
