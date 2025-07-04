import pytest
from collections import defaultdict
from src.main.model.models import Station, Route, Robot, Package, PackageSize
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


def test_app(test_lines):
    # first get lines plus serive class
    lines, train_service = test_lines
    
    # define reload-stations
    reload_stations = ["de:08212:606", "de:08215:35082", "de:08236:1793"]
    
    # create route service
    route_service = Route2Service(train_service=train_service, reload_stations=reload_stations)

    # then build graph for the application
    graph, station_coords = route_service.build_graph(lines)

    # create robots for simulation
    robot_one = Robot(id="1", name="hermes",
                      position=Station(id=reload_stations[0],
                                       name=train_service.get_station_name(
                                           reload_stations[0]),
                                       coordinates=train_service.get_station_coords(reload_stations[0])),
                      battery_level=100.0, status="ready", num_packages=0)
    robot_two = Robot(id="2", name="Luke",
                      position=Station(id=reload_stations[1],
                                       name=train_service.get_station_name(
                                           reload_stations[1]),
                                       coordinates=train_service.get_station_coords(reload_stations[1])),
                      battery_level=100.0, status="ready", num_packages=0)

    # add packages to the simulation
    package_one = Package(id="pkg_one", start=train_service.get_station_by_id(reload_stations[0]), destination=train_service.get_station_by_id(train_service.get_station_id("Ostendstr.")), weight=2.0, size=PackageSize.M)
    package_two = Package(id="pkg_two", start=train_service.get_station_by_id(reload_stations[2]), destination=train_service.get_station_by_id(train_service.get_station_id("Wilhelm-Leuschner-Str.")), weight=0.5, size=PackageSize.S)

    #calculate route for package delivery
    delivery_route, delivery_time = route_service.calculate_delivery_route(reload_stations[0], [package_one.destination.id, package_two.destination.id])
    reload_route, reload_time = route_service.calculate_reload_route(delivery_route[-1][0], {reload_stations[0]: 3, reload_stations[1]: 4, reload_stations[2]: 2})
    full_route = delivery_route
    full_route.extend(reload_route)
    full_time = delivery_time + reload_time

    route = route_service.build_route_object(full_route, full_time)

    #test results
    assert graph is not None
    assert station_coords is not None
    assert delivery_route is not None
    assert reload_route is not None
    assert full_route is not None
    assert route is not None
    assert route.stops >= 1
    assert route.travel_time > 0
    assert all(isinstance(s, Station) for s in route.stations)

    # print results in terminal
    print(f"Delivery: {delivery_route}")
    print(f"reload: {reload_route}")
    print(f"Full path: {full_route}")
    print("Route station names:", [s.name for s in route.stations])
    print("Transfers:", [s.name for s in route.transfer])
    print("Total time:", route.travel_time)
    print("Transfer time:", route.transfer_time)