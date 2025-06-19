from ast import Return
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
import uuid
from src.main.repository.train_repository import TrainRepository
from src.main.service.train_service import TrainService
from src.main.repository.repository_container import robot_repo_singleton as robot_repo
from src.main.model.models import PakcageCreate, Package, Coordinates

router = APIRouter()
train_repo = TrainRepository()
train_service = TrainService(train_repo)

# New parcels (packages, but parcels is a term that is not part of normal informatics language) for the simulation get posted here
@router.post("/addPackage")
def add_new_package_to_simulation(data: PakcageCreate):
    start_id = train_service.get_station_id(data.start)
    start_station = train_service.get_station_by_id(start_id)

    dest_id = train_service.get_station_id(data.destination)
    dest_station = train_service.get_station_by_id(dest_id)

    package = Package(
        id=str(uuid.uuid4()),
        weight=data.weight,
        size=data.size,
        start=start_station,
        destination=dest_station
    )

    train_service.add_package(start_id, [package])

    return {
        "message": f"Package added to CargoStation {start_station.name}",
        "package_id": package.id
    }

# Gets current cargo from all robots
@router.get("/cargoOnDelivery")
def get_cargo():
    all_cargo = []
    
    for robot in robot_repo.get_all_robots().values():
        for pkg in robot.packages:
            all_cargo.append({
                "robot_id": robot.id,
                "package_id": pkg.id,
                "weight": pkg.weight,
                "destination": pkg.destination.name if pkg.destination else None
            })

    return {"total_packages": len(all_cargo), "cargo": all_cargo}


# Post cargo stations before simulation
@router.post("/addCargoStations")
def add_cargo_stations(station_name: str = Query(...)):
    station_id = train_service.get_station_id(station_name)
    
    if station_id:
        train_service.add_cargo_station(station_id)

        return {"message": "New Cargo-Station created."}
    else:
        raise HTTPException(status_code=404, detail=f"{station_name} not found.")

@router.post("/deleteCargoStation")
def delete_cargo_station(station_name: str = Query(...)):
    station_id = train_service.get_station_id(station_name)
    print(f"Station to remove: {station_id}")
    if station_id:
        train_service.remove_cargo_station(station_id)

        return {"message": f"{station_name} as CargoStation deleted."}
    else:  
        raise HTTPException(status_code=404, detail=f"{station_name} not found.")

# Gets cargo stations
@router.get("/cargoStations")
def get_cargo_stations():
    cargo_station_ids = train_service.get_cargo_station_ids()

    stations = []
    for id in cargo_station_ids:
        name = train_service.get_station_name(id)
        stations.append(name)
    
    return stations