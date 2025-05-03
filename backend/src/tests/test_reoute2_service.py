import pytest
import pdb
from collections import defaultdict
from src.main.model.models import Station, Coordinates, Route
from src.main.service.route_service_2 import Route2Service
from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository


@pytest.fixture
def test_lines():
    repo = TrainRepository()
    service = TrainService(repo)

    lines = []
    for line_name in ["4", "5"]:
        lines.append(service.get_all_line_stations(line_name))

    return lines, service


def test_route2(test_lines):
    lines, train_service = test_lines
    service = Route2Service(train_service)
    graph, station_coords = service.build_graph(lines)

    pickup_station_one = Station(id="de:08212:608", name="Albert-Braun-Str.", coordinates=Coordinates(lat=48.9891289173621,
                                                                                                      long="8.36354885712662"))
    dropoff_station_one = Station(id="de:08212:622", name="Ostendstr.", coordinates=Coordinates(lat=49.0050363474168,
                                                                                                long=8.41629793061011))

    path = service.calculate_travel_order(pickup_station_one, dropoff_station_one)
    route = service.build_route_object(path)

    assert graph is not None
    assert path is not None
    assert route is not None
    assert isinstance(route, Route)
    assert route.stops >= 1
    assert route.travel_time > 0
    assert all(isinstance(s, Station) for s in route.stations)


    print(f"Full path: {path}")
    print("Route station names:", [s.name for s in route.stations])
    print("Transfers:", [s.name for s in route.transfer])
    print("Total time:", route.travel_time)
    print("Transfer time:", route.transfer_time)
