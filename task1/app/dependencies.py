from fastapi import Request

from app.db import RedisService


def get_redis(request: Request) -> RedisService:
    """Dependency that uses connection pool created on startup event from fastapi request"""
    return RedisService(request.app.state.redis_pool)
