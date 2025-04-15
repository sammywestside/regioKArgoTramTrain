from fastapi import APIRouter, HTTPException, Query
from src.main.service.route_service import RouteService
from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository
from src.main.model.models import LineData, Route


router = APIRouter()

train_repo = TrainRepository()
train_service = TrainService(train_repo)
route_service = RouteService(train_repo, train_service)


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

# get the line by station_id
@router.get("/station/{station_id}/line", response_model=LineData)
def get_line_by_station(station_id: str):
    try:
        line_name = train_service.get_line(station_id)
        if not line_name:
            raise HTTPException(status_code=404, detail="Line not found")
        return line_name
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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


