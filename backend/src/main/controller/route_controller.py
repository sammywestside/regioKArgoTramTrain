import traceback
from ast import Return
from fastapi import APIRouter, HTTPException, Query
from src.main.service.route_service_2 import Route2Service
from src.main.service.train_service import TrainService
from src.main.repository.repository_container import robot_repo_singleton as robot_repo
from src.main.repository.repository_container import train_repo_singleton as train_repo
from src.main.model.models import Route

router = APIRouter()
train_service = TrainService(train_repo)
RELOAD_STATIONS = ["de:08212:606"]


# Get all the informationen needed to start the application
@router.get("/start")
def get_start_information():
    try:
        lines_data = train_repo.load_lines_v2()
        lines = lines_data.get("lines", [])

        route_service = Route2Service(train_service, RELOAD_STATIONS)

        stations_data = train_service.train_repo.load_stations_data()
        coordinates = [
            {
                "id": station["triasID"],
                "name": station["name"],
                "lat": station["coordPositionWGS84"]["lat"],
                "long": station["coordPositionWGS84"]["long"]
            }
            for station in stations_data
        ]

        all_lines = []
        for line in lines:
            stations = train_service.get_all_line_stations(line["number"])
            stations.travel_time = 10  # Dummy travel_time
            all_lines.append(stations)

        graph, station_coords = route_service.build_graph(all_lines)

        routes = []
        for line in all_lines:
            routes.append({
                "line": line.line_name,
                "stations": [
                    {
                        "id": s.id,
                        "name": s.name
                    } for s in getattr(line, "stations", [])
                ]
            })

        return {
            "lines": lines,
            "coordinates": coordinates,
            "routes": routes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Route
# @router.get("/route", response_model=Route)
# def get_route(start: str = Query(...), target: str = Query(...)):
#     try:
#         all_lines = []
#         for line in train_repo.load_lines_v2()["lines"]:
#             stations = train_service.get_all_line_stations(line["number"])
#             stations.travel_time = 10
#             all_lines.append(stations)

#         graph, station_coords = route_service.build_graph(all_lines)

#         # Route2Service erwartet IDs, nicht Namen!
#         start_id = train_service.get_station_id(start)
#         target_id = train_service.get_station_id(target)
#         path, total_time = route_service._dijkstra(start_id, target_id)
#         if not path:
#             raise HTTPException(status_code=404, detail="No route found")

#         route = route_service.build_route_object(path, total_time)
#         print("DEBUG: route object:", route)
#         print("DEBUG: route.stations:", getattr(route, "stations", "not present"))
#         return route

#calculate route
@router.get("/route", response_model=Route)
def get_route(robot_id: str = Query(...)):
    try:
        all_lines = train_service.load_all_line_data()

        robot = robot_repo.get_robot_by_id(robot_id)
        print(f"Robot: {robot}")
        start_station_id = train_service.get_station_id_by_coords(robot.position)

        reload_stations = train_service.get_cargo_station_ids()

        route_service = Route2Service(train_service, reload_stations)

        ready = route_service.build_graph(all_lines)
        if ready: 
            packages = robot.packages

            delivery_targets = []
            #TODO Package is only the packages id as string
            # Need to rethink how I save package information in the json.
            for package in packages:
                package_destination = package["destination"]
                dest_id = train_service.get_station_id(package_destination)
                delivery_targets.append(dest_id)
            
            delivery_route, delivery_time = route_service.calculate_delivery_route(start_station_id, delivery_targets)

            cargo_stations = train_service.get_cargo_stations()
        
            reload_route, reload_time = route_service.calculate_reload_route(delivery_route[-1][0], cargo_stations)

            full_route = delivery_route
            full_route.extend(reload_route)

            full_time = delivery_time + reload_time

            route = route_service.build_route_object(full_route, full_time)
            return route

        raise HTTPException(status_code=404, detail="Could not build graph of all lines.")
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# Get all route steps
@router.get("/route/steps")
def get_route_steps(start: str = Query(...), end: str = Query(...)):
    try:
        route_service = Route2Service(train_service, RELOAD_STATIONS)

        all_lines = []
        for line in train_repo.load_lines_v2()["lines"]:
            stations = train_service.get_all_line_stations(line["number"])
            stations.travel_time = 10
            all_lines.append(stations)

        graph, station_coords = route_service.build_graph(all_lines)

        start_id = train_service.get_station_id(start)
        end_id = train_service.get_station_id(end)
        path, total_time = route_service._dijkstra(start_id, end_id)
        if not path:
            raise HTTPException(status_code=404, detail="no route found.")

        # path ist eine Liste von (station_id, line_name)
        steps = [
            {"station_id": station_id, "line": line}
            for station_id, line in path
        ]
        return {"steps": steps, "total_time": total_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
