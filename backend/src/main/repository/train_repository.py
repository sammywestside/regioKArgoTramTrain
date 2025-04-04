import json
from pathlib import Path

class TrainRepository:
    kvv_lines_geo_coords_file_path = 'C:/Users/samue/regioKArgoTramTRain/json/KVVLinesGeoJSON.json'
    lines_v2_path = 'C:/Users/samue/regioKArgoTramTRain/json/lines_v2.json'
    stations_data_path = 'C:/Users/samue/regioKArgoTramTRain/json/haltestellen_v2-1.json'

    def load_kvv_lines(self):
        with open (self.kvv_lines_geo_coords_file_path, 'r') as f:
             return json.load(f)
            
    def load_lines_v2(self):
        with open (self.lines_v2_path, 'r') as f:
            return json.load(f)
        
    def load_stations_data(self):
        with open (self.stations_data_path, 'r') as f:
            return json.load(f)


