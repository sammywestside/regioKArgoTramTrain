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
