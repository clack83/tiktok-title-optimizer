import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)


async def cache_get(key: str) -> Optional[Any]:
    value = await redis.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_set(key: str, value: Any, ttl: int = 3600) -> None:
    await redis.set(key, json.dumps(value), ex=ttl)


async def cache_delete(key: str) -> None:
    await redis.delete(key)


async def cache_exists(key: str) -> bool:
    return await redis.exists(key) > 0
