import sys
import pdb
from collections import defaultdict
from src.main.repository.train_repository import TrainRepository
from src.main.model.models import LineData, Station, Coordinates


class TrainService:

    def __init__(self, train_repo: TrainRepository):
        self.train_repo = train_repo
        self.lines: list[LineData] = self.load_all_line_data()


    def get_station_id(self, station_name):
        station_data = self.train_repo.load_stations_data()

        station_id = ""

        for station in station_data:
            if station["name"] == station_name:
                station_id = station["triasID"]

        return station_id
    

    def get_station_name(self, station_id):
        stations_data = self.train_repo.load_stations_data()

        station_name = ""

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
                    coords = Coordinates(
                        lat=station_coords["lat"], long=station_coords["long"])

            return coords
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")


    def get_line(self, station_id):
        try:
            line_data = self.train_repo.load_lines_v2()

            if not line_data or "lines" not in line_data:
                print("Error: No lines found in the loaded data")
                return None
            
            for line in line_data["lines"]:
                line_stations = line.get("stations", [])
                for id in line_stations:
                    if id == station_id:
                        return line["name"]
            
            print(f"Error: Station {station_id} not found in any line")
            return None
        except KeyError as e:
            print(f"KeyError occurred: {e}")
        except Exception as e:
            exc_tb = sys.exc_info()
            print(f"An error occurred on line: {exc_tb.tb_lineno}: {e}")
            return None


    def get_line_travel_time(self, line_name) -> int:
        try:
            time = 0

            transit_information = self.train_repo.load_transit_data()

            for line_data in transit_information:
                if line_data["lineName"] == line_name:
                    time = line_data["travelTime"]

            # print(f"TravelTime: {time}")
            return time
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def get_all_line_stations(self, line: str) -> LineData:
        try:
            stations = []

            line_json = self.train_repo.load_lines_v2()

            for item in line_json["lines"]:
                if item["number"] == line:
                    line_name = item["name"]
                    line_stations = item["stations"]
                    for station_id in line_stations:
                        # print(station_id)
                        station_name = self.get_station_name(station_id)
                        station_coords = self.get_station_coords(station_id)
                        stations.append(
                            Station(id=station_id, name=station_name, coordinates=station_coords))

            travel_time = self.get_line_travel_time(line_name)
            return LineData(line_name=line, stations=stations, travel_time=travel_time)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def load_all_line_data(self) -> list[LineData]:
        try:
            all_lines = []

            all_lines_json = self.train_repo.load_lines_v2()

            for line in all_lines_json["lines"]:
                number = line["number"]
                all_lines.append(self.get_all_line_stations(number))
            
            return all_lines
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def build_station_map(self) -> defaultdict[str, Station]:
        try:
            station_map = {}

            for line in self.lines:
                for station in line.stations:
                    station_map[station.id] = station
            
            return station_map
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def get_line_draw_coords(self, line_id) -> list:
        try:
            coordinates = []

            coordinates_data = self.train_repo.load_kvv_geo_data()
            features = coordinates_data["features"]

            for line in features:
                # print(line)
                properties = line["properties"]
                line_name = properties["name"]
                # print(properties)

                if line_name == line_id:
                    line_geometry = line["geometry"]
                    line_coords = line_geometry["coordinates"]
                    coordinates.append(line_coords)

            return coordinates

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def get_all_station_names(self) -> list:
        try:
            all_stations = []

            stations_data = self.train_repo.load_stations_data()

            for station in stations_data:
                name = station["triasName"]
                all_stations.append(name)

            return all_stations
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")
