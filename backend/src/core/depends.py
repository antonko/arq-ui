from arq.connections import RedisSettings
from core.cache import LRUCache
from core.config import Settings, get_app_settings

settings: Settings = get_app_settings()
cache_singleton = LRUCache(capacity=settings.max_jobs)


def get_lru_cache() -> LRUCache:
    """Get LRU cache."""
    return cache_singleton


def get_redis_settings() -> RedisSettings:
    """Get Redis settings."""
    return RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        database=settings.redis_db,
        password=settings.redis_password,
        ssl=settings.redis_ssl,
        ssl_cert_reqs=settings.redis_ssl_cert_reqs,
    )
