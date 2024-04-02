from pydantic import BaseModel

class FuelSystemStatus(BaseModel):
    fuel_level: float
    pumps_status: str

class NavigationSystemDiagnostic(BaseModel):
    system_status: str
    error_code: int | None

class LifeSupportSystemTestResult(BaseModel):
    air_quality: str
    water_supply_status: str

class CommunicationSystemCheck(BaseModel):
    signal_strength: float
    connection_status: str
    satellite_link_quality: float
    bandwidth: float
    latency: float
    error_rate: float
    frequency_stability: str
    encryption_status: str
    backup_system_status: str
    hardware_integrity: str
    software_version: str
    last_maintenance_date: str

class LaunchReadinessAnalysis(BaseModel):
    readiness_status: str
    fuel_system_ready: bool
    navigation_system_ready: bool
    life_support_system_ready: bool
    communication_system_ready: bool
    propulsion_system_status: str
    structural_integrity: str
    onboard_computer_status: str
    launch_pad_systems_ready: bool
    weather_conditions: str
    crew_readiness: bool
    issues: list[str] = []
    final_inspection_completed: bool