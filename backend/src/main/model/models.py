from pydantic import BaseModel
from typing import List

class Coordinates(BaseModel):
    lat: float
    long: float

class Station(BaseModel):
    name: str
    coordinates: Coordinates

class LineData(BaseModel):
    line_name: str
    stations: List[Station]