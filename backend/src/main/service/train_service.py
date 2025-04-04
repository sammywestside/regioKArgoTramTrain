import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from main.repository.train_repository import TrainRepository

class TrainService:
    def __init__(self, train_repo: TrainRepository):
        self.train_repo = train_repo
    
    def get_station_name(self, station_id):
        stations_data = self.train_repo.load_stations_data()

        station_name = None
    	
        for station in stations_data:
            if station["triasID"] == station_id:
                station_name = station["name"]
        
        return station_name

    
    def get_station_id(self, line_number, station_number):
        stations_data = self.train_repo.load_lines_v2()

        # line_name = [item["stations"] for item in stations_data["lines"] if item["number"] == line_number]
        station_id = None

        for item in stations_data["lines"]:
            if item["number"] == line_number:
                line_name = item["stations"]
                station_id = line_name[station_number]
                break

        return station_id

    def get_all_line_station_coords(self, number):
        line_coord_data = self.train_repo.load_kvv_lines()

        line_coordinates = []

        features = line_coord_data["features"]
        for entry in features:

            line_name = entry["properties"]["name"]
            if line_name == number:
                print(f"Correct line: {line_name}")
                coordinates = entry["geometry"]["coordinates"]

                for index, coords in enumerate(coordinates):
                    station_id = self.get_station_id(line_name, index)
                    station_name = self.get_station_name(station_id)
                    print(station_id, coords)
                    line_coordinates.append([station_name, coords])

        return "done."

    


