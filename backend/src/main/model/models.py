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
    size: float     # optional: in Litern, cm³ etc.


class Robot(BaseModel):
    id: str
    name: str
    # position: Coordinates
    battery_level: float = 100.0
    status: str  # 'idle', 'moving', 'charging', etc.
    # assigned_route: Route
    packages: List[Package] = []  # jetzt als Liste von echten Packages
    dis_charge_time: float
    dissipation_factor: float
