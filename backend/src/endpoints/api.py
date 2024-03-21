from endpoints import jobs, status
from fastapi import APIRouter

routers = APIRouter()

routers.include_router(jobs.router)
routers.include_router(status.router)
