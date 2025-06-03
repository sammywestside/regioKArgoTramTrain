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
    def remove_package_from_robot(self, package_id: str) -> int:
        try:
            for pkg in self.robot.packages:
                if pkg.id == package_id:
                    self.robot.packages.remove(pkg)
                    self.robot.num_packages -= 1
                    print(f"Package {package_id} removed from robot {self.robot.name}.")
                    return self.robot.num_packages
            print(f"Package {package_id} not found on robot {self.robot.name}.")
            return self.robot.num_packages
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")
        
    # Returns a total weight of current packages
    def get_total_package_weight(self) -> float:
        return sum(p.weight for p in self.robot.packages)
    
    # Finds a package by ID
    def get_package_by_id(self, package_id: str) -> Optional[Package]:
        return next((p for p in self.robot.packages if p.id == package_id), None)

    # Simulates battery drain based on time and dissipation factor
    # def discharge_robot(self, robot: Robot):
    #     try: 
    #         if self.robot.dis_charge_time < 0:
    #             print(f"Warning: discharge time < 0 on robot {robot.name}, skipping battery calculation.")
    #             return

    #         original = robot.battery_level
    #         robot.battery_level *= (1 - self.robot.dissipation_factor * math.sqrt(robot.dis_charge_time))
    #         robot.battery_level = max(robot.battery_level, 0)

    #         print(f"{robot.name}: Battery went from {original:.2f}% → {robot.battery_level:.2f}%")

    #         if robot.battery_level <= 10:
    #             print(f"{robot.name} is running low on battery!")
    #         if robot.battery_level == 0:
    #             print(f"{robot.name} has no battery left!")
    #     except Exception as e:
    #         print(f"Error during battery discharge: {e}")

    # fully recharges the robot
    def charge_robot(self) -> bool:
        self.robot.battery_level = 100.0
        return True

    # Returns a formatted status string of the robot
    def get_robot_information(self) -> dict:
        status = {
            "id": self.robot.id,
            "name": self.robot.name,
            "position": self.robot.position,
            "battery": self.robot.battery_level,
            "num_packages": self.robot.num_packages,
            "packages": self.robot.packages,
            "status": self.robot.status,
            "route": self.robot.route
        }

        return status