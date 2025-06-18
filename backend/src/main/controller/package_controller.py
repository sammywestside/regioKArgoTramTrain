from ast import Return
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
import uuid
from src.main.repository.train_repository import TrainRepository
from src.main.repository.repository_container import robot_repo_singleton as robot_repo
from src.main.model.models import CargoStationInput, Package, PackageSize, Station, Coordinates

router = APIRouter()

# New parcels (packages, but parcels is a term that is not part of normal informatics language) for the simulation get posted here
@router.post("/addPackage")
def add_new_package_to_simulation(
    robot_id: str = Query(...),
    weight: float = Query(...),
    size: PackageSize = Query(PackageSize.M),
    count: int = Query(1, ge=1)
):
    robot = robot_repo.get_robot_by_id(robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {robot_id} not found")

    package_ids = []
    for _ in range(count):
        package = Package(
            id=str(uuid.uuid4()),
            weight=weight,
            size=size,
            start=Station(
                id=f"start-{robot.id}",
                name="Start Position",
                coordinates=Coordinates(lat=robot.position.lat, long=robot.position.long)
            ),
            destination=None
        )

        #TODO Die Pakete werden nicht direkt den Robotern angehängt sondern den Beladestationen!
        robot.packages.append(package)
        robot.num_packages += 1
        package_ids.append(package.id)

    robot_repo.update_robot(robot.id, robot)

    return {
        "message": f"{count} package(s) added to robot {robot.id}",
        "package_ids": package_ids
    }


# Remove one package from robot
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
def add_cargo_stations(data: List[CargoStationInput], train_repo: TrainRepository = Depends()):
    updated_robots = []

    for entry in data:
        robot = robot_repo.get_robot_by_id(entry.robot_id)
        if not robot:
            continue  # oder Fehler werfen

        valid_stations = []
        for station in entry.stations:
            # Nur wenn Station in TrainRepository existiert
            known_station = train_repo.get_station_by_id(station.id)
            if known_station:
                valid_stations.append(known_station)
            else:
                raise HTTPException(status_code=400, detail=f"Station ID '{station.id}' existiert nicht.")

        # TODO Warum wird die Beladestation an die Route des Roboters angehängt? 
        # TODO Die Beladestationen sollten in die Listen-Variable angefügt werden
        # TODO Die Variable die oben im RouteController genutzt wird.
        robot.route.stations.extend(valid_stations)
        robot_repo.update_robot(robot.id, robot)
        updated_robots.append(robot.id)

    return {"updated_robots": updated_robots}


# Gets cargo stations
@router.get("/cargoStations")
def get_cargo_stations():
    all_stations = []

    for robot in robot_repo.get_all_robots().values():
        for station in robot.route.stations:
            all_stations.append({
                "robot_id": robot.id,
                "station_id": station.id,
                "station_name": station.name,
                "coordinates": {
                    "lat": station.coordinates.lat,
                    "long": station.coordinates.long
                }
            })

    return {
        "total_stations": len(all_stations),
        "cargo_stations": all_stations
    }