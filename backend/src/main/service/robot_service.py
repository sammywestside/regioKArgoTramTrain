import math
import sys
from typing import Optional
from src.main.model.models import Robot, Package


class RobotService:
    MAX_CARRY_WEIGHT = 100.0  # Maximum weight in kg
    MAX_NUMBER_PACKAGES = 10

    def __init__(self, robot: Robot):
        self.robot = robot

    def get_capacity(self):
        return self.MAX_NUMBER_PACKAGES
        
    # Checks whether a new package can still be carried based on total weight
    def isAtCapacity(self, new_package_weight: float) -> bool:
        current_weight = sum(p.weight for p in self.robot.packages)
        return (current_weight + new_package_weight) <= self.MAX_CARRY_WEIGHT

    # Adds a package to the robot if the weight limit is not exceeded
    def add_package_to_robot(self, package: Package) -> int: 
        try:       
            if self.isAtCapacity(package.weight):
                self.robot.packages.append(package)
                self.robot.num_packages += 1
                print(f"Package {package.id} added to robot {self.robot.name}.")
                return self.robot.num_packages
            else:
                print(f"Cannot add package {package.id} — capacity exceeded.")
                return self.robot.num_packages
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    # Removes a package from the robot based on its ID
    def remove_one_package_from_robot(self) -> int:
        if self.robot.packages:
            removed_package = self.robot.packages.pop()  # entfernt das letzte Paket, du kannst hier andere Logik machen
            self.robot.num_packages -= 1
            print(f"Package {removed_package.id} removed from robot {self.robot.name}.")
        else:
            print(f"No packages to remove from robot {self.robot.name}.")
        return self.robot.num_packages
    
    # Removes all packages from the robot
    def remove_all_packages_from_robot(self) -> int:
        count = len(self.robot.packages)
        self.robot.packages.clear()
        self.robot.num_packages = 0
        print(f"All {count} packages removed from robot {self.robot.name}.")
        return self.robot.num_packages
        
    # Returns a total weight of current packages
    def get_total_package_weight(self) -> float:
        return sum(p.weight for p in self.robot.packages)
    
    # Finds a package by ID
    def get_package_by_id(self, package_id: str) -> Optional[Package]:
        return next((p for p in self.robot.packages if p.id == package_id), None)

    # fully recharges the robot
    def charge_robot(self) -> bool:
        self.robot.battery_level = 100.0
        return True

    # Returns a formatted status string of the robot
    def get_robot_information(self) -> dict:
        status = {
            "id": self.robot.id,
            "name": self.robot.position.name if self.robot.position else None,
            "position": self.robot.position,
            "battery": self.robot.battery_level,
            "num_packages": self.robot.num_packages,
            "packages": self.robot.packages,
            "status": self.robot.status,
            "route": self.robot.route
        }
        return status
    
    # Get all robots
    def get_all_robots(self) -> list[Robot]:
        return list(self.robots.values())
