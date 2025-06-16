from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Coordinates(BaseModel):
    lat: float
    long: float


class Station(BaseModel):
    id: str
    name: str
    coordinates: Coordinates


class LineData(BaseModel):
    line_name: str
    stations: List[Station]
    travel_time: Optional[int] = None


class Route(BaseModel):
    stations: List[Station]
    stops: int
    transfer: List[Station]
    travel_time: float
    transfer_time: float


class PackageSize(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

class Package(BaseModel):
    id: str
    destination: Optional[Station] = None # optional
    weight: float   # in kg
    size: PackageSize


class Robot(BaseModel):
    id: str
    position: Station = None
    battery_level: float = 100.0
    status: str  = "idle"         # 'idle', 'moving', 'charging', etc.
    route: Route = {}
    packages: List[Package] = []  # jetzt als Liste von echten Packages
    num_packages: int = 0
    # dis_charge_time: float
    # dissipation_factor: float

class StationInput(BaseModel):
    robot_id: str
    stations: List[Station]

class CargoStationInput(BaseModel):
    robot_id: str
    stations: List[StationInput]

class RobotConfigInput(BaseModel):
    robot_id: str
    battery_level: float | None = None
    status: str | None = None