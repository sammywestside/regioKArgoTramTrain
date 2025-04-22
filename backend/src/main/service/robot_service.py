import math
from typing import Optional
from src.main.model.models import Robot, Package


class RobotService:
    MAX_CARRY_WEIGHT = 100.0  # Maximum weight in kg

    # Checks whether a new package can still be carried based on total weight
    def calculate_robot_capacity(self, robot: Robot, new_package_weight: float) -> bool:
        current_weight = sum(p.weight for p in robot.packages)
        return (current_weight + new_package_weight) <= self.MAX_CARRY_WEIGHT

    # Adds a package to the robot if the weight limit is not exceeded
    def add_package_to_robot(self, robot: Robot, package: Package) -> bool: 
        try:       
            if self.calculate_robot_capacity(robot, package.weight):
                robot.packages.append(package)
                print(f"Package {package.id} added to robot {robot.name}.")
                return True
            else:
                print(f"Cannot add package {package.id} — capacity exceeded.")
                return False
        except Exception as e:
            print(f"Error adding package, {e}")
            return False

    # Removes a package from the robot based on its ID
    def remove_package_from_robot(self, robot: Robot, package_id: str) -> bool:
        try:
            for pkg in robot.packages:
                if pkg.id == package_id:
                    robot.packages.remove(pkg)
                    print(f"Package {package_id} removed from robot {robot.name}.")
                    return True
            print(f"Package {package_id} not found on robot {robot.name}.")
            return False
        except Exception as e:
            print(f"Error removing package: {e}")
            return False
        
    # Returns a total weight of current packages
    def get_total_package_weight(self, robot: Robot) -> float:
        return sum(p.weight for p in robot.packages)
    
    # Finds a package by ID
    def get_package_by_id(self, robot: Robot, package_id: str) -> Optional[Package]:
        return next((p for p in robot.packages if p.id == package_id), None)

    # Simulates battery drain based on time and dissipation factor
    def discharge_robot(self, robot: Robot):
        try: 
            if robot.dis_charge_time < 0:
                print(f"Warning: discharge time < 0 on robot {robot.name}, skipping battery calculation.")
                return

            original = robot.battery_level
            robot.battery_level *= (1 - robot.dissipation_factor * math.sqrt(robot.dis_charge_time))
            robot.battery_level = max(robot.battery_level, 0)

            print(f"{robot.name}: Battery went from {original:.2f}% → {robot.battery_level:.2f}%")

            if robot.battery_level <= 10:
                print(f"{robot.name} is running low on battery!")
            if robot.battery_level == 0:
                print(f"{robot.name} has no battery left!")
        except Exception as e:
            print(f"Error during battery discharge: {e}")

    # fully recharges the robot
    def charge_robot(self, robot: Robot):
        robot.battery_level = 100.0
        print(f"🔌 {robot.name} is now fully charged.")

    # Returns a formatted status string of the robot
    def get_robot_status(self, robot: Robot) -> str:
        return (
            f"Robot '{robot.name}'\n"
            f"   • Position: ({robot.position.lat}, {robot.position.long})\n"
            f"   • Battery: {robot.battery_level:.1f}%\n"
            f"   • Packages: {len(robot.packages)} (Total weight: {sum(p.weight for p in robot.packages):.1f} kg)\n"
            f"   • Status: {robot.status}"
        )