from ast import Return
from fastapi import APIRouter, HTTPException
from src.main.service.train_service import TrainService
from src.main.repository.repository_container import train_repo_singleton as train_repo
from src.main.model.models import Coordinates, LineData, Station

router = APIRouter()
train_service = TrainService(train_repo)


# Get all stations
@router.get("/stations", response_model=list[Station])
def get_all_stations():
    try:
        stations_data = train_service.train_repo.load_stations_data()
        stations = [
            Station(
                id=station["triasID"],
                name=station["name"],
                coordinates=Coordinates(
                    lat=station["coordPositionWGS84"]["lat"],
                    long=station["coordPositionWGS84"]["long"]
                )
            )
            for station in stations_data
        ]
        return stations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get station informations
@router.get("/station/{station_id}", response_model=Station)
def get_station_info(station_id: str):
    try:
        name = train_service.get_station_name(station_id)
        coords = train_service.get_station_coords(station_id)
        if not name or not coords:
            raise HTTPException(status_code=404, detail="Station not found.")
        return Station(id=station_id, name=name, coordinates=coords)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get the line by station_id
@router.get("/station/{station_id}/line", response_model=LineData)
def get_line_by_station(station_id: str):
    if not station_id.startswith("de:"):
        raise HTTPException(status_code=400, detail="Invalid station_id format")
    
    try:
        line_name = train_service.get_line(station_id)
        if not line_name:
            raise HTTPException(status_code=404, detail="Line not found")
        return line_name
    except Exception as e:
        print(f"Error occurred in get_line_by_station: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")