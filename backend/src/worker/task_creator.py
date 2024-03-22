import asyncio
import logging
import random
from datetime import datetime

from arq import create_pool
from arq.connections import RedisSettings

logger = logging.getLogger(__name__)


def get_redis_settings() -> RedisSettings:
    return RedisSettings(host="redis")


async def create_tasks() -> None:
    print("Start creating tasks")

    redis = await create_pool(get_redis_settings())
    while True:
        num_tasks = random.randint(1, 5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating {num_tasks} tasks")
        for _ in range(num_tasks):
            await redis.enqueue_job(
                "process_task",
                func="Dummy Function",
                success=random.choice([True, False]),
            )
        await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(create_tasks())
    except Exception as e:
        print(f"Error occurred: {e}")
