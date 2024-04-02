import asyncio
import logging
import random
import sys

sys.path.insert(0, "/app/src")
from arq import ArqRedis, create_pool
from core.config import Settings, get_app_settings
from core.depends import get_redis_settings

logger = logging.getLogger(__name__)
settings: Settings = get_app_settings()


async def enqueue_job(redis_pool: ArqRedis, is_successful: bool):
    await redis_pool.enqueue_job(
        random.choice(
            [
                "check_fuel_system",
                "diagnose_navigation_system",
                "test_life_support_system",
                "check_communication_system",
                "analyze_launch_readiness",
            ],
        ),
        is_successful=is_successful,
    )

async def pattern_hill(redis_pool: ArqRedis, max_tasks_per_minute: int):
    total_minutes = 10
    for minute in range(1, total_minutes + 1):
        num_tasks = (
            round(max_tasks_per_minute * (minute / 5))
            if minute <= 5
            else round(max_tasks_per_minute * (2 - minute / 5))
        )
        for _ in range(num_tasks):
            await enqueue_job(redis_pool, True)
        
        if minute < total_minutes:
            await asyncio.sleep(60)

async def pattern_increasing_errors(redis_pool: ArqRedis, max_tasks_per_minute: int):
    total_minutes = 5
    for minute in range(1, total_minutes + 1):
        num_tasks = random.randint(1, max_tasks_per_minute)
        error_ratio = minute / 5
        for _ in range(num_tasks):
            is_successful = random.random() > error_ratio
            await enqueue_job(redis_pool, is_successful)
        if minute < total_minutes:
            await asyncio.sleep(60)

async def pattern_peak(redis_pool: ArqRedis, max_tasks_per_minute: int):
    total_minutes = 5
    for minute in range(1, total_minutes + 1):
        num_tasks = round(max_tasks_per_minute * (2 * abs(3 - minute) / 5))
        for _ in range(num_tasks):
            await enqueue_job(redis_pool, True)
        
        if minute < total_minutes:
            await asyncio.sleep(60)


async def pattern_random_distribution(redis_pool: ArqRedis, max_tasks_per_minute: int):
    total_minutes = 10    
    for _ in range(total_minutes):
        num_tasks = random.randint(0, max_tasks_per_minute)
        for _ in range(num_tasks):
            await enqueue_job(redis_pool, True)
        
        if _ < total_minutes - 1:
            await asyncio.sleep(60)


async def main():
    redis_pool = await create_pool(get_redis_settings(), default_queue_name=settings.queue_name)

    while True:
        await pattern_hill(redis_pool, 20)
        await pattern_random_distribution(redis_pool, 20)
        await pattern_increasing_errors(redis_pool, 20)
        await pattern_random_distribution(redis_pool, 20)
        await pattern_peak(redis_pool, 20)

if __name__ == "__main__":
    asyncio.run(main())
