import asyncio
import logging
import random
import sys

sys.path.insert(0, '/app/src')
from core.depends import get_redis_settings
from models import CommunicationSystemCheck, FuelSystemStatus, LaunchReadinessAnalysis, LifeSupportSystemTestResult, NavigationSystemDiagnostic
from typing import Any

from arq import run_worker
from core.config import Settings, get_app_settings
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)
settings: Settings = get_app_settings()

def sleep_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await asyncio.sleep(random.uniform(0.1, 20))
        return await func(*args, **kwargs)
    return wrapper

@sleep_decorator
async def check_fuel_system(ctx: dict[str, Any], is_successful: bool) -> str:
    """Check fuel system status."""
    if is_successful:
        return FuelSystemStatus(
            fuel_level=random.uniform(0, 100),
            pumps_status=random.choice(["active", "inactive"]),
        ).model_dump_json()
    raise Exception("Fuel system check failed")

@sleep_decorator
async def diagnose_navigation_system(ctx: dict[str, Any], is_successful: bool) -> str:
    """Diagnose navigation system."""
    if is_successful:
        return NavigationSystemDiagnostic(
            system_status=random.choice(["ok", "error"]),
            error_code=random.randint(0, 100) if random.random() > 0.5 else None,
        ).model_dump_json()
    raise Exception("Navigation system diagnosis failed")

@sleep_decorator
async def test_life_support_system(ctx: dict[str, Any], is_successful: bool) -> str:
    """Test life support system."""
    if is_successful:
        return LifeSupportSystemTestResult(
            air_quality=random.choice(["good", "bad"]),
            water_supply_status=random.choice(["ok", "error"]),
        ).model_dump_json()
    raise Exception("Life support system test failed")

@sleep_decorator
async def check_communication_system(ctx: dict[str, Any], is_successful: bool) -> str:
    """Check communication system."""
    if is_successful:
        return CommunicationSystemCheck(
            signal_strength=random.uniform(0, 100),
            connection_status=random.choice(["ok", "error"]),
            satellite_link_quality=random.uniform(0, 100),
            bandwidth=random.uniform(0, 100),
            latency=random.uniform(0, 100),
            error_rate=random.uniform(0, 100),
            frequency_stability=random.choice(["ok", "error"]),
            encryption_status=random.choice(["ok", "error"]),
            backup_system_status=random.choice(["active", "inactive"]),
            hardware_integrity=random.choice(["ok", "error"]),
            software_version="1.0",
            last_maintenance_date="2026-01-01",
        ).model_dump_json()
    raise Exception("Communication system check failed")

@sleep_decorator
async def analyze_launch_readiness(ctx: dict[str, Any], is_successful: bool) -> str:
    """Analyze launch readiness."""
    if is_successful:
        return LaunchReadinessAnalysis(
            readiness_status=random.choice(["ready", "not ready"]),
            fuel_system_ready=random.choice([True, False]),
            navigation_system_ready=random.choice([True, False]),
            life_support_system_ready=random.choice([True, False]),
            communication_system_ready=random.choice([True, False]),
            propulsion_system_status=random.choice(["ok", "error"]),
            structural_integrity=random.choice(["ok", "error"]),
            onboard_computer_status=random.choice(["ok", "error"]),
            launch_pad_systems_ready=random.choice([True, False]),
            weather_conditions=random.choice(["good", "bad"]),
            crew_readiness=random.choice([True, False]),
            issues=["Issue 1", "Issue 2"] if random.random() > 0.5 else [],
            final_inspection_completed=random.choice([True, False]),
        ).model_dump_json()
    raise Exception("Launch readiness analysis failed")
    
class WorkerSettings:
    redis_settings = get_redis_settings()
    functions = [
        check_fuel_system,
        diagnose_navigation_system,
        test_life_support_system,
        check_communication_system,
        analyze_launch_readiness
        ]
    max_tries = 1
    queue_name = settings.queue_name
    allow_abort_jobs = True


if __name__ == "__main__":
    run_worker(WorkerSettings)