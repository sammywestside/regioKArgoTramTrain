from ast import Return
from fastapi import APIRouter, HTTPException, Query, Body
import uuid
from src.main.service.train_service import TrainService
from src.main.service.robot_service import RobotService
from src.main.repository.repository_container import robot_repo_singleton as robot_repo
from src.main.repository.repository_container import train_repo_singleton as train_repo
from src.main.model.models import Robot, RobotConfigInput, Route, RobotCreate, RobotPosition, Coordinates

router = APIRouter()
train_service = TrainService(train_repo)


# Get all robot information
@router.get("/AllRobotInfo")
def get_all_robot_info():
    all_robots = robot_repo.get_all_robots()
    if not all_robots:
        raise HTTPException(status_code=404, detail="No robots found")

    result = []
    for robot in all_robots:
        result.append({
            "id": robot.id,
            "name": robot.name,
            "position": {
                "lat": robot.position.lat,
                "long": robot.position.long
            },
            "battery_level": robot.battery_level,
            "status": robot.status,
            "route": robot.route,
            "packages": robot.packages,
            "num_packages": robot.num_packages
        })
    return result


# Get information of one robot
@router.get("/RobotInfo")
def get_robot_Info(id: str = Query(..., description="Robot ID"), 
                   lat: float = Query(...), long: float = Query(...)):
    
    robot = robot_repo.get_robot_by_id(id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {id} not found")

    robot_service = RobotService(robot)
    pos_coords = Coordinates(lat=lat, long=long)
    robot_service.calculate_changes(pos_coords)

    return {
        "id": robot.id,
        "name": robot.name,
        "position": {
            "lat": robot.position.lat,
            "long": robot.position.long
        },
        "battery_level": robot.battery_level,
        "status": robot.status,
        "route": robot.route,
        "packages": robot.packages,
        "num_packages": robot.num_packages
    }


# Init two robots
@router.post("/init_robots")
def init_robots():
    stations_data = train_service.get_all_line_stations("S1")
    stations = stations_data.stations[:5] if stations_data else []

    if len(stations) < 2:
        raise HTTPException(status_code=400, detail="Nicht genügend Stationen in Linie S1")

    start_station = stations[0]
    reverse_start_station = stations[-1]

    robot1 = Robot(
        id="1",
        position=RobotPosition(
            lat=start_station.coordinates.lat,
            long=start_station.coordinates.long
        ),
        battery_level=100.0,
        status="idle",
        route=Route(stations=stations, stops=0, transfer=[], travel_time=0, transfer_time=0),
        packages=[],
        num_packages=0
    )
    robot2 = Robot(
        id="2",
        position=RobotPosition(
            lat=reverse_start_station.coordinates.lat,
            long=reverse_start_station.coordinates.long
        ),
        battery_level=100.0,
        status="idle",
        route=Route(stations=stations[::-1], stops=0, transfer=[], travel_time=0, transfer_time=0),
        packages=[],
        num_packages=0
    )

    robot_repo.add_robot(robot1)
    robot_repo.add_robot(robot2)

    return {"message": "2 robots initialized with stations from line S1"}


# Add new robot
@router.post("/addRobot")
def add_robot(robot_data: RobotCreate):
    position_station_name = robot_data.position
    position_id = train_service.get_station_id(position_station_name)
    position_station = train_service.get_station_by_id(position_id)
    position = position_station.coordinates
    route = Route(
        stations=[],
        stops=0,
        transfer=[],
        travel_time=0,
        transfer_time=0
    )
    robot = Robot(
        id=robot_data.id,
        name=robot_data.name,
        position=position,
        battery_level=robot_data.battery_level,
        status="idle",
        route=route,
        packages=[],
        num_packages=0
    )
    if robot_repo.get_robot_by_id(robot.id):
        raise HTTPException(status_code=400, detail=f"Robot with id {robot.id} already exists")
    robot_repo.add_robot(robot)
    return {"message": f"Robot with id {robot.id} added."}


@router.post("/addPackagesToRobot")
def add_packages_to_robot(robot_id: str = Query(...)):
    robot = robot_repo.get_robot_by_id(robot_id)
    cargo_station = train_service.get_station_id_by_coords(robot.position)
    packages = train_service.get_cargo_station_packages_by_id(cargo_station)

    robot.packages.extend(packages)
    robot.num_packages += len(packages)
    robot.battery_level = min(100, robot.battery_level + len(packages) * 2)

    train_service.remove_package(cargo_station, robot.packages)

    return {"message": f"Added {len(packages)} Packages to Robot {robot.name}"}

# Delete robot
@router.delete("/removeRobot")
def remove_robot(id: str = Query(..., description="Robot ID")):
    try:
        robot_repo.remove_robot(id)
        return {"message": f"Robot with id {id} removed."}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.delete("/removeAllRobots")
def remove_all_robots():
    robot_repo.remove_all_robots()
    return {"message": "All robots removed."}


# Hets current batterie start
@router.get("/batterieCharge")
def get_batterie_charge(id: str = Query(..., description="Robot ID")):
    robot = robot_repo.get_robot_by_id(id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {id} not found")

    service = RobotService(robot)
    return {"battery_level": service.robot.battery_level}


# Gets current load capacity 
@router.get("/loadCapacity")
def get_load_capacity(id: str = Query(..., description="Robot ID")):
    robot = robot_repo.get_robot_by_id(id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {id} not found")
    
    service = RobotService(robot)
    
    return {
        "robot_id": robot.id,
        "current_num_packages": robot.num_packages,
        "max_packages": service.get_capacity(),
        "available_capacity": service.get_capacity() - robot.num_packages,
        "total_weight": service.get_total_package_weight()
    } 


#  Gets nhext stops of the robots
@router.get("/nextStop")
def get_next_stop():
    robots = robot_repo.get_all_robots()
    next_stops = []

    for robot_id, robot in robots.items():
        if robot.route.stations and len(robot.route.stations) > 0:
            next_station = robot.route.stations[0]
            next_stops.append({
                "robot_id": robot_id,
                "next_stop_id": next_station.id,
                "next_stop_name": next_station.name
            })
        else:
            next_stops.append({
                "robot_id": robot_id,
                "message": "No stops remaining"
            })

    return {
        "next_stops": next_stops 
    }


# Robot configuration changes are posted here
@router.post("/robotConfig")
def change_robot_config(config: RobotConfigInput):
    robot = robot_repo.get_robot_by_id(config.robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {config.robot_id} not found")

    if config.battery_level is not None:
        robot.battery_level = config.battery_level
    if config.status is not None:
        robot.status = config.status

    robot_repo.update_robot(robot.id, robot)
    return {"message": f"Configuration updated for robot {robot.id}"}