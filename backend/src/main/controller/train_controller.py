from ast import Return
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from src.main.repository import robot_repository
from src.main.service.route_service import RouteService
from src.main.service.train_service import TrainService
from src.main.service.robot_service import RobotService
from src.main.repository.train_repository import TrainRepository
from src.main.repository.robot_repository import RobotRepository
from src.main.model.models import CargoStationInput, Coordinates, LineData, Package, Route, Station, Robot, RobotConfigInput, PackageSize
import uuid


router = APIRouter()
train_repo = TrainRepository()
robot_repo = RobotRepository()
train_service = TrainService(train_repo)
route_service = RouteService(train_service)
route_service = RouteService(train_service)


# ROUTE CONTROLLERS:

# get route
@router.get("/route", response_model=Route)
def get_route(start: str = Query(...), target: str = Query(...)):
    try:
        # load all lines and transfer it to lineData
        all_lines = []
        for line in train_repo.load_lines_v2()["lines"]:
            stations = train_service.get_all_line_stations(line["number"])
            # Dummy travel_time
            stations.travel_time = 10  # we have to calculate it !!!!!
            all_lines.append(stations)

        # build graph from line data
        graph = route_service.build_graph(all_lines)

        # calculate fastest route
        route = route_service.calculate_route(graph, start, target)

        if not route:
            raise HTTPException(status_code=404, detail="No route found")

        return route

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# calculates the fastest route between two stations and returns the route steps along with the total travel time.
@router.get("/route/steps")
def get_route_steps(start: str = Query(...), end: str = Query(...)):
    try:
        all_lines = []

        # Load all train lines and create LineData
        for line in train_repo.load_lines_v2()["lines"]:
            stations = train_service.get_all_line_stations(line["number"])
            stations.travel_time = 10
            all_lines.append(stations)

        # Build graph from the line data
        graph = route_service.build_graph(all_lines)
        # Find the fastest route from start to end
        route, total_time = route_service.find_fastest_route(graph, start, end)

        if not route:
            raise HTTPException(status_code=404, detail="no route found.")
        
        return {"steps": route, "total time": total_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# LINE CONTROLLERS:

# get all lines
@router.get("/lines")
def get_all_lines():
    try:
        lines_data = train_repo.load_lines_v2()
        return lines_data.get("lines", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get the line by station_id
@router.get("/station/{station_id}/line", response_model=LineData)
def get_line_by_station(station_id: str):
    # Validierung der station_id
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
    

# get line coords
@router.get("/line/coords/{line_id}")
def get_line_coords(line_id: str):
    try:
        coords = train_service.get_line_draw_coords(line_id)
        if not coords:
            raise HTTPException(status_code=404, detail="Line not found or has no coordinates.")
        return {"lines_id": line_id, "coordinates": coords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# STATION CONTROLLERS:

# get all stations
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
    

# **IS WORKING**
# get all stations from a line
@router.get("/line/stations/{lines_id}", response_model=LineData)
def get_all_line_stations(line_id: str):
    try:
        line_data = train_service.get_all_line_stations(line_id)
        if line_data is None:
            raise HTTPException(status_code=404, detail="Line not found")
        return line_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get station informations
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

@router.post("/init_robots")
def init_robots():
    # Lade Stationen der Linie S1
    stations_data = train_service.get_all_line_stations("S1")
    stations = stations_data.stations[:5] if stations_data else []

    if len(stations) < 2:
        raise HTTPException(status_code=400, detail="Nicht genügend Stationen in Linie S1")

    # Roboterposition auf erste Station setzen
    start_station = stations[0]
    reverse_start_station = stations[-1]

    # Roboter anlegen mit gültiger Position
    robot1 = Robot(
        id="1",
        position=start_station,
        battery_level=100.0,
        status="idle",
        route=Route(stations=stations, stops=0, transfer=[], travel_time=0, transfer_time=0),
        packages=[],
        num_packages=0
    )
    robot2 = Robot(
        id="2",
        position=reverse_start_station,
        battery_level=100.0,
        status="idle",
        route=Route(stations=stations[::-1], stops=0, transfer=[], travel_time=0, transfer_time=0),
        packages=[],
        num_packages=0
    )

    # Roboter zum Repository hinzufügen
    robot_repo.add_robot(robot1)
    robot_repo.add_robot(robot2)

    return {"message": "2 robots initialized with stations from line S1"}


# gets info of all robots
@router.get("/AllRobotInfo")
def get_all_robot_info():
    all_robots = robot_repo.get_all_robots()
    if not all_robots:
        raise HTTPException(status_code=404, detail="No robots found")

    result = []
    for robot in all_robots:
        service = RobotService(robot)
        result.append(service.get_robot_information())

    return result


# gets robot info 
@router.get("/RobotInfo")
def get_robot_Info(id: str = Query(..., description="Robot ID")):
    try:
        robot = robot_repo.get_robot_by_id(id)
        if not robot:
            raise HTTPException(status_code=404, detail=f"Robot with id {id} not found")

        service = RobotService(robot)
        return service.get_robot_information()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# gets current batterie start
@router.get("/batterieCharge")
def get_batterie_charge(id: str = Query(..., description="Robot ID")):
    robot = robot_repo.get_robot_by_id(id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {id} not found")

    service = RobotService(robot)
    return {"battery_level": service.robot.battery_level}


# gets current load capacity 
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
    } # wie machen wir das mit dem Akku verlust? 


# gets current cargo from all robots
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

#  gets nhext stops of the robots
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

#post cargo stations before simulation
@router.post("/addCargoStations")
def add_cargo_stations(data: List[CargoStationInput], train_repo: TrainRepository = Depends()):
    updated_robots = []

    for entry in data:
        robot = robot_repository.get_robot_by_id(entry.robot_id)
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

        robot.route.stations.extend(valid_stations)
        robot_repository.update_robot(robot.id, robot)
        updated_robots.append(robot.id)

    return {"updated_robots": updated_robots}

# gets cargo stations
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


# new parcels (packages, but parcels is a term that is not part of normal informatics language) for the simulation get posted here
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
            destination=None
        )
        robot.packages.append(package)
        robot.num_packages += 1
        package_ids.append(package.id)

    robot_repo.update_robot(robot.id, robot)

    return {
        "message": f"{count} package(s) added to robot {robot.id}",
        "package_ids": package_ids
    }


# robot configuration changes are posted here
@router.post("/robotConfig")
def change_robot_config(config: RobotConfigInput):
    robot = robot_repo.get_robot_by_id(config.robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail=f"Robot with id {config.robot_id} not found")

    # Werte aktualisieren, wenn sie übergeben wurden
    if config.battery_level is not None:
        robot.battery_level = config.battery_level
    if config.status is not None:
        robot.status = config.status

    robot_repo.update_robot(robot.id, robot)
    return {"message": f"Configuration updated for robot {robot.id}"}