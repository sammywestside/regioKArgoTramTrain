# models.py

from pydantic import BaseModel
from typing import List, Optional


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


class Package(BaseModel):
    id: str
    destination: Station
    weight: float   # in kg
    size: list     # optional: in Litern, cm³ etc.


class Robot(BaseModel):
    id: str
    name: str
    position: str = ""
    battery_level: float = 100.0
    status: str  = "idle"         # 'idle', 'moving', 'charging', etc.
    route: Route = {}
    packages: List[Package] = []  # jetzt als Liste von echten Packages
    num_packages: int = 0
    # dis_charge_time: float
    # dissipation_factor: float
