from redis.asyncio import Redis


class RedisClient:
    _client: Redis | None = None

    @classmethod
    async def init(cls, host: str, port: int, db: int = 0, password: str | None = None):
        cls._client = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("Redis client is not initialized")
        return cls._client
