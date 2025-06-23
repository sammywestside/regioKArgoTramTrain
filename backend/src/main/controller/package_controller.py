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

    print(f"STart: {start_station.name}, dest: {dest_station.name}")

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

# Remove one package from robot
#TODO Eigentlich haben wir uns drauf geeinigt das Pakete nucht entfernt werden können. 
# Nur CargoStations und Roboter
@router.delete("/removePackage")
def remove_package_from_robot(robot_id: str = Query(...)):
    robot = robot_repo.get_robot_by_id(robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {robot_id} not found")

    from src.main.service.robot_service import RobotService
    robot_service = RobotService(robot)
    before = robot.num_packages

    robot_service.remove_one_package_from_robot()
    robot_repo.update_robot(robot.id, robot)

    if before == robot.num_packages:
        raise HTTPException(status_code=404, detail=f"No packages found on robot {robot_id}")
    return {"message": f"One package removed from robot {robot_id}."}


# Remove all packages from robot
@router.delete("/removeAllPackages")
def remove_all_packages_from_robot(robot_id: str = Query(...)):
    robot = robot_repo.get_robot_by_id(robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {robot_id} not found")

    from src.main.service.robot_service import RobotService
    robot_service = RobotService(robot)

    count_before = robot.num_packages
    robot_service.remove_all_packages_from_robot()
    robot_repo.update_robot(robot.id, robot)

    if count_before == 0:
        return {"message": f"No packages to remove on robot {robot_id}."}
    else:
        return {"message": f"All {count_before} packages removed from robot {robot_id}."}


# Gets current cargo from all robots
@router.get("/cargo")
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

    train_service.add_cargo_station(station_id)

    return {"message": "New Cargo-Station created."}

@router.post("/removeCargoStation")
def remove_cargo_stations(station_name: str = Query(...)):
    station_id = train_service.get_station_id(station_name)

    if station_id:
        train_service.remove_cargo_station(station_id)

        return {"message": f"{station_name} as CargoStation deleted."}
    else:
        raise HTTPException(status_code=404, detail=f"{station_name} as CargoStation not found.")

# Gets cargo stations
@router.get("/cargoStations")
def get_cargo_stations():
    cargo_station_ids = train_service.get_cargo_station_ids()

    stations = []
    for id in cargo_station_ids:
        name = train_service.get_station_name(id)
        stations.append(name)
    
    return stations