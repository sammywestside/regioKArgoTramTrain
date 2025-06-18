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
    start: Optional[Station]
    destination: Optional[Station] = None  # optional
    weight: float  # in kg
    size: PackageSize

RobotPosition = Coordinates

class Robot(BaseModel):
    id: str
    name: str = ""
    position: RobotPosition = RobotPosition(lat=0, long=0)
    battery_level: float = 100.0
    status: str = "idle"
    route: Optional[Route] = None
    packages: List[Package] = []
    num_packages: int = 0

class RobotCreate(BaseModel):
    id: str
    name: str
    battery_level: float
    position: RobotPosition

class PakcageCreate(BaseModel):
    start: Coordinates
    weight: float
    size: PackageSize
    destination: Coordinates

class StationInput(BaseModel):
    robot_id: str
    stations: List[Station]

class CargoStationInput(BaseModel):
    robot_id: str
    stations: List[StationInput]

class RobotConfigInput(BaseModel):
    robot_id: str
    battery_level: Optional[float] = None
    status: Optional[str] = None
