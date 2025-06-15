from ast import Return
from fastapi import APIRouter, HTTPException, Query
from src.main.service.route_service import RouteService
from src.main.service.train_service import TrainService
from src.main.service.robot_service import RobotService
from src.main.repository.train_repository import TrainRepository
from src.main.model.models import Coordinates, LineData, Route, Station


router = APIRouter()

train_repo = TrainRepository()
train_service = TrainService(train_repo)
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


# gets all robot info 
@router.get("/allRobotInfo")
def get_robot_Info(id: int):
    return "Does nothing"


# gets current batterie start
@router.get("/batterieCharge")
def get_batterie_charge(id: int):
    return "Does nothing"


# gets current load capacity 
@router.get("/loadCapacity")
def get_load_capacity(): 
    return "Does nothing"


# gets current cargo from all robots
@router.get("/cargo")
def get_cargo(): 
    return "Does nothing"


#  gets nhext stops of the robots
@router.get("/nextStop")
def get_next_stop(): 
    return "Does nothing"

#post cargo stations before simulation
@router.post("/addCargoStations")
def add_cargo_stations():
    return "TBD"

# gets cargo stations
@router.get("/cargoStations")
def get_cargo_stations():
    return "Does nothing"


# new parcels (packages, but parcels is a term that is not part of normal informatics language) for the simulation get posted here
@router.post("/newParcel")
def add_new_package_to_simulation():
    return "Does nothing"


# robot configuration changes are posted here
@router.post("/robotConfig")
def change_robot_config(): 
    return "Does nothing"
