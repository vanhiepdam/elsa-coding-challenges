import redis
import redis_lock
from django.conf import settings


class RedisClient(redis.Redis):
    def __init__(self, **kwargs):
        # Cache url pattern: redis://localhost:6379/0
        port = settings.CACHE_URL.split(":")[-1].split("/")[0]
        db = settings.CACHE_URL.split("/")[-1]
        super().__init__(host=settings.CACHE_URL, port=port, db=db, retry_on_timeout=True, **kwargs)


class RedisLock(redis_lock.Lock):
    def __init__(self, key: str, **kwargs):
        client = RedisClient()
        super().__init__(redis_client=client, name=key, **kwargs)
