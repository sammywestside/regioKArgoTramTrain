import pytest
import pdb
from collections import defaultdict
from src.main.model.models import Station, LineData, Route
from src.main.service.route_service import RouteService
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


def test_route(test_lines):
    lines, train_service = test_lines
    route_service = RouteService(train_service=train_service)

    graph = route_service.build_graph(lines)
    # for station, connections in graph.items():
        # print(f"{station}: {[n for n, _, _ in connections]}")

    start_station = "Albert-Braun-Str."
    dest_station = "Sinsheimer Str."

    route = route_service.calculate_route(graph, start_station, dest_station)

    assert route is not None
    assert isinstance(route, Route)
    assert route.stops >= 1
    assert route.travel_time > 0
    assert all(isinstance(s, Station) for s in route.stations)

    print("Route station names:", [s.name for s in route.stations])
    print("Transfers:", [s.name for s in route.transfer])
    print("Total time:", route.travel_time)
    print("Transfer time:", route.transfer_time)

    # MANY CONFUSING ERRORS 
    # ASK CHATGPT IN A NEW CHAT ABOUT DIJKAS-ALGORITHM
    # ASK FOR EXPLENATIONS ON NODES,EDGES AND DISTANCES
    # TRANSLATE THOUGHS TO OUR CLASS VARIABLES