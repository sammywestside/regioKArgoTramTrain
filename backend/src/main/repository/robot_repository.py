from typing import Dict, Optional, List
from src.main.model.models import Robot, Station

class RobotRepository:
    def __init__(self):
        self.robots_by_id: Dict[str, Robot] = {}

    def get_robot_by_id(self, robot_id: str) -> Optional[Robot]:
        return self.robots_by_id.get(robot_id)

    def get_all_robots(self) -> List[Robot]:
        return list(self.robots_by_id.values())

    def add_robot(self, robot: Robot):
        self.robots_by_id[robot.id] = robot

    def update_robot(self, robot_id: str, robot: Robot):
        if robot_id in self.robots_by_id:
            self.robots_by_id[robot_id] = robot
        else:
            raise KeyError(f"Robot mit ID {robot_id} existiert nicht")

    def remove_robot(self, robot_id: str):
        if robot_id in self.robots_by_id:
            del self.robots_by_id[robot_id]
        else:
            raise KeyError(f"Robot mit ID {robot_id} existiert nicht")
        
    def remove_all_robots(self):
        self.robots_by_id.clear()

    def assign_stations_to_robot(self, robot_id: str, stations: List[Station]):
        robot = self.get_robot_by_id(robot_id)
        if not robot:
            raise KeyError(f"Robot mit ID {robot_id} existiert nicht")
        robot.route.stations = stations
