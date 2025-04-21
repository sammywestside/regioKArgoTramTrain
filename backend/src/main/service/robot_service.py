import math
from src.main.model import models


class RobotService:
    MAX_CARRY_WEIGHT = 100.0  # Max. Gewicht in kg

    def calculate_robot_capacity(self, robot: models.Robot, new_package_weight: float) -> bool:
        """
        Prüft, ob das neue Paket gewichtstechnisch noch transportiert werden kann.
        """
        current_weight = sum(p.weight for p in robot.packages)
        return (current_weight + new_package_weight) <= self.MAX_CARRY_WEIGHT

    def add_package_to_robot(self, robot: models.Robot, package: models.Package) -> bool:
        """
        Fügt dem Roboter ein Paket hinzu, wenn es vom Gewicht her passt.
        """
        if self.calculate_robot_capacity(robot, package.weight):
            robot.packages.append(package)
            print(f"Package {package.id} added to robot {robot.name}.")
            return True
        else:
            print(f"Cannot add package {package.id} — capacity exceeded.")
            return False

    def remove_package_from_robot(self, robot: models.Robot, package_id: str) -> bool:
        """
        Entfernt ein Paket anhand seiner ID.
        """
        for pkg in robot.packages:
            if pkg.id == package_id:
                robot.packages.remove(pkg)
                print(f"Package {package_id} removed from robot {robot.name}.")
                return True
        print(f"Package {package_id} not found on robot {robot.name}.")
        return False

    def dis_charge_robot(self, robot: models.Robot):
        """
        Simuliert Akkuverbrauch anhand Zeit und Dissipation-Faktor.
        """
        original = robot.battery_level
        robot.battery_level *= (1 - robot.dissipation_factor * math.sqrt(robot.dis_charge_time))
        robot.battery_level = max(robot.battery_level, 0)

        print(f"{robot.name}: Battery went from {original:.2f}% → {robot.battery_level:.2f}%")

        if robot.battery_level <= 10:
            print(f"{robot.name} is running low on battery!")
        if robot.battery_level == 0:
            print(f"{robot.name} has no battery left!")

    def charge_robot(self, robot: models.Robot):
        """
        Lädt den Roboter vollständig auf.
        """
        robot.battery_level = 100.0
        print(f"🔌 {robot.name} is now fully charged.")

    def get_robot_status(self, robot: models.Robot) -> str:
        return (
            f"Robot '{robot.name}'\n"
            f"   • Position: ({robot.position.lat}, {robot.position.long})\n"
            f"   • Battery: {robot.battery_level:.1f}%\n"
            f"   • Packages: {len(robot.packages)} (Total weight: {sum(p.weight for p in robot.packages):.1f} kg)\n"
            f"   • Status: {robot.status}"
        )