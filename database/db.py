import redis.asyncio as redis
async def create_redis_pool():
    pool = redis.ConnectionPool.from_url("redis://localhost", db=0)
    client = redis.Redis(connection_pool=pool)
    return client

