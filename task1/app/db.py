from typing import Optional

from redis import asyncio as redis_aio

from app.models import Address, PhoneAddress
from settings import settings


def create_redis_pool():
    return redis_aio.ConnectionPool(
        host=settings.Redis.host,
        port=settings.Redis.port,
        db=settings.Redis.db,
        decode_responses=True
    )


class RedisService:
    def __init__(self, connection_pool: redis_aio.ConnectionPool):
        self.__pool = connection_pool
        self.__redis_connect = self.__create_redis_connect(connection_pool=self.__pool)

    def __create_redis_connect(self, connection_pool: redis_aio.ConnectionPool):
        """Create redis connection using precreated connection pool in lifespan on_startup"""
        return redis_aio.Redis(connection_pool=connection_pool)

    async def _set(self, name: str, value: str) -> bool:
        try:
            status = await self.__redis_connect.set(name, value)
        except Exception:
            return False
        else:
            return status

    async def _get(self, name: str) -> str:
        return await self.__redis_connect.get(name)

    async def get_address(self, phone: str) -> Optional[Address]:
        address = await self._get(phone)
        if not address:
            return None
        return Address(address=address)

    async def set_address(self, phone: str, address: str) -> Optional[PhoneAddress]:
        status = await self._set(phone, address)
        if not status:
            return None
        return PhoneAddress(phone=phone, address=address)
