import sys
from src.main.repository.train_repository import TrainRepository
from src.main.model.models import LineData, Station, Coordinates


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
    
    def get_station_coords(self, station_id) -> Coordinates:
        try:
            stations_data = self.train_repo.load_stations_data()

            for station in stations_data:
                if station["triasID"] == station_id:
                    station_coords = station["coordPositionWGS84"]
                    coords = Coordinates(lat=station_coords["lat"], long=station_coords["long"])

            return coords
        except Exception as e: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def get_all_line_stations(self, line: str) -> LineData:
        try:
            stations = []

            line_json= self.train_repo.load_lines_v2()

            for item in line_json["lines"]:
                if item["number"] == line:
                    line_stations = item["stations"]
                    for station_id in line_stations:
                        station_name = self.get_station_name(station_id)
                        station_coords = self.get_station_coords(station_id)
                        stations.append(Station(name=station_name, coordinates=station_coords))
                    
            return LineData(line_name=line, stations=stations)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")
    
    
