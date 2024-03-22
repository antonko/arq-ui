import asyncio
import random
from typing import Any

from arq import Retry, run_worker
from arq.connections import RedisSettings
from pydantic import BaseModel


def get_redis_settings() -> RedisSettings:
    return RedisSettings(host="redis")


class TaskResult(BaseModel):
    status: str
    message: str = ""


async def process_task(ctx: dict[str, Any], func: str, success: bool) -> str:
    print(f"Processing task with function: {func} and expected success: {success}")
    await asyncio.sleep(random.randint(1, 15))
    if success:
        print("Task processed successfully")
        return TaskResult(status="ok", message="Task processed successfully").json()
    else:
        print("Task processing failed")
        # raise Exception("Task processing failed")
        raise Retry(10)


class WorkerSettings:
    redis_settings = get_redis_settings()
    functions = [process_task]
    max_tries = 1


if __name__ == "__main__":
    run_worker(WorkerSettings)
