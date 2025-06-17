import pytest
from src.main.model.models import Station, Package
from src.main.service.route_service_2 import Route2Service
from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository

@pytest.fixture
def test_lines():
    repo = TrainRepository()
    service = TrainService(repo)

    lines = []
    # for line_name in ["4", "5"]:
    #     lines.append(service.get_all_line_stations(line_name))
    lines = service.load_all_line_data()

    return lines, service


def test_route2(test_lines):
    lines, train_service = test_lines
    reload_stations = ["de:08212:606"]
    service = Route2Service(train_service, reload_stations)
    graph, station_coords = service.build_graph(lines)

    package_one = Package(id="pkg_one", destination=train_service.get_station_by_id(train_service.get_station_id("Ostendstr.")), weight=2.0, size=(10, 10, 2))
    package_two = Package(id="pkg_two", destination=train_service.get_station_by_id(train_service.get_station_id("Wilhelm-Leuschner-Str.")), weight=0.5, size=(5, 5, 2))

    delivery_route, delivery_time = service.calculate_delivery_route(reload_stations[0], [package_one.destination.id, package_two.destination.id])
    reload_route, reload_time = service.calculate_reload_route(delivery_route[-1][0], {reload_stations[0]: 3})
    
    full_route = delivery_route
    full_route.extend(reload_route)
    full_time = delivery_time + reload_time

    route = service.build_route_object(full_route, full_time)

    assert graph is not None
    assert station_coords is not None
    assert delivery_route is not None
    assert reload_route is not None
    assert full_route is not None
    assert route is not None
    assert route.stops >= 1
    assert route.travel_time > 0
    assert all(isinstance(s, Station) for s in route.stations)

    print(f"Delivery: {delivery_route}")
    print(f"reload: {reload_route}")
    print(f"Full path: {full_route}")
    print("Route station names:", [s.name for s in route.stations])
    print("Transfers:", [s.name for s in route.transfer])
    print("Total time:", route.travel_time)
    print("Transfer time:", route.transfer_time)
