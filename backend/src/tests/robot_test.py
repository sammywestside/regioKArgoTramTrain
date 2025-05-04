from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository
from src.main.service.robot_service import RobotService
from src.main.model.models import Robot, Package, Station, Coordinates


def test_robot():
    repo = TrainRepository()
    service = TrainService(repo)

    robot = Robot(id="r2d2", name="R2D2")
    robot_service = RobotService(robot)

    current_status = robot_service.get_robot_information()
    assert isinstance(current_status, dict)
    print(current_status)
    
    station = "Ostendstr."
    station_id = service.get_station_id(station)
    destination = service.get_station_by_id(station_id)

    test_package_one = Package(id="1", weight=2.0, size=(10.0, 10.0, 2.5), destination=destination)
    assert isinstance(test_package_one.size, list)

    capacity = robot_service.isAtCapacity(2.0)
    assert isinstance(capacity, bool)

    add_package = robot_service.add_package_to_robot(test_package_one)
    assert isinstance(add_package, int)

    current_status = robot_service.get_robot_information()
    assert isinstance(current_status, dict)
    print(current_status)

    assert robot.num_packages is not None
    assert robot.packages is not None
