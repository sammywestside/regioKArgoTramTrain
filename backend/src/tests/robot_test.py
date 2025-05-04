from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository
from src.main.service.robot_service import RobotService
from src.main.model.models import Robot, Package, Station, Coordinates


def test_robot():
    repo = TrainRepository()
    service = TrainService(repo)
    robot_service = RobotService()

    robot = Robot(id="r2d2", name="R2D2", dis_charge_time=10,
                  dissipation_factor=1.1, status="charging")
    dest_coordinates = Coordinates(lat=49.0008522250264, long=8.31194064405395)
    destination = Station(id="de:08212:307", name="Altrheinbrücke", coordinates=dest_coordinates)
    test_package_one = Package(id="1", weight=2.0, size=50, destination=destination)

    capacity = robot_service.calculate_robot_capacity(robot, 2.2)
    assert isinstance(capacity, bool)

    add_package = robot_service.add_package_to_robot(robot, test_package_one)
    assert isinstance(add_package, bool)

    current_status = robot_service.get_robot_status(robot)
    assert isinstance(current_status, str)
    print(current_status)
    
    old_battery = robot.battery_level
    robot_service.discharge_robot(robot)
    assert robot.battery_level != old_battery
    current_status = robot_service.get_robot_status(robot)
    print(current_status)
