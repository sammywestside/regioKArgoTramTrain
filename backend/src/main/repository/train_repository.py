import json
from pathlib import Path

class TrainRepository:
    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent
        self.json_path = base_path / "json"

        self.kvv_lines_geo_cords_file_path = self.json_path / "KVVLinesGeoJSON.json"
        self.lines_v2_path = self.json_path / "lines_v2.json"
        self.stations_data_path = self.json_path / "haltestellen_v2-1.json"

    def load_lines_v2(self):
        with open (self.lines_v2_path, 'r') as f:
            return json.load(f)
    
    def load_stations_data(self):
        with open (self.stations_data_path, 'r') as f:
            return json.load(f)