import json
from pathlib import Path
from src.main.repository.robot_repository import RobotRepository

robot_repo = RobotRepository()

class TrainRepository:
    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent
        self.json_path = base_path / "json"

        self.kvv_lines_geo_cords_file_path = self.json_path / "KVVLinesGeoJSON.json"
        self.lines_v2_path = self.json_path / "lines_v2.json"
        self.stations_data_path = self.json_path / "haltestellen_v2-1.json"
        self.transit_data_path = self.json_path / "KVV_Transit_Information.json"
        self.cargo_stations = self.json_path / "CargoStations.json"

    def load_lines_v2(self):
        with open(self.lines_v2_path, 'r') as f:
            return json.load(f)

    def load_stations_data(self):
        with open(self.stations_data_path, 'r') as f:
            return json.load(f)

    def load_kvv_geo_data(self):
        with open(self.kvv_lines_geo_cords_file_path, 'r') as f:
            return json.load(f)

    def load_transit_data(self):
        with open(self.transit_data_path, 'r') as f:
            return json.load(f)
    
    def load_cargo_stations(self):
        with open(self.cargo_stations, "r") as f:
            return json.load(f)
        
    def save_cargo_station_data(self, data):
        with open(self.cargo_stations, "w") as f:
            json.dump(data, f, indent=4)

