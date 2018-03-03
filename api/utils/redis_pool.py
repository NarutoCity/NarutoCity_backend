import django_redis
from redis.client import StrictRedis

conn = django_redis.get_redis_connection()  # type:StrictRedis
