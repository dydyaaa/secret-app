from redis.asyncio import Redis
from src.redis import RedisClient

async def get_redis() -> Redis:
    return RedisClient.get_client()