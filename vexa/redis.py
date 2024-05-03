import redis.asyncio as aioredis
import os




async def get_connections(redis_client, name="initialFeed_audio", pattern='*', min_length=1):
    """
    Finds queues that match a given pattern and have a minimum number of items.
    """
    matching_queues = []
    cursor = '0'
    while cursor != 0:
        cursor, keys = await redis_client.scan(cursor, match=f'{name}:{pattern}', count=min_length)
        for key in keys:
            length = await redis_client.llen(key)
            if await redis_client.type(key) == 'list' and await redis_client.llen(key) >= min_length:
                key = key.replace(f'{name}:', '')  # Remove the prefix
                matching_queues.append((key,length))
    return matching_queues

async def get_redis(host = 'host.docker.internal',port=6380,db=0):
    
    db = await aioredis.from_url(
            f"redis://{host}:{port}/{db}",decode_responses=True
        )

    await db.ping()

    return db