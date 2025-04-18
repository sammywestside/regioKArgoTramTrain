import sys
import heapq
from collections import defaultdict

from fastapi import HTTPException
from src.main.repository.train_repository import TrainRepository
from src.main.model import models
from src.main.service.train_service import TrainService


class RouteService:
    def __init__(self, train_repo: TrainRepository, train_service: TrainService):
        self.train_repo = train_repo
        self.train_service = train_service

    # Create a python readable visualisation of the linesystem
    @staticmethod
    def build_graph(lines: list[models.LineData]) -> defaultdict:
        graph = defaultdict(list)

        try:
            # Loop through each line of the system
            for line in lines:
                station_objs = line.stations  # get list of all stations on current line
                total_time = line.travel_time  # get total travel time of current line
                line_name = line.line_name  # get name of current line

                # Amount of actual travel between 2 stations on the line
                segments = len(station_objs) - 1
                if segments == 0:
                    continue  # In case a line with only one station exists

                # The mathematical time of travel between 2 stations
                segment_time = total_time / segments

                # Loop through the whole line
                for i in range(segments):
                    current_station = station_objs[i].id
                    next_station = station_objs[i+1].id

                    # Add both directions into the graph
                    graph[current_station].append(
                        (next_station, segment_time, line_name))
                    graph[next_station].append(
                        (current_station, segment_time, line_name))

            return graph

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if exc_tb is not None:  # Prüfen, ob exc_tb vorhanden ist
                print(f"An error occurred on line: {exc_tb.tb_lineno}: {e}")
            else:
                print(f"Error occurred: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    
    def find_fastest_route(graph: defaultdict, start_id: str, dest_id: str):
        if start_id == dest_id:
            return [], 0

        if start_id not in graph or dest_id not in graph:
            return None, None

        try:
            # (total time, current_station, path_taken)
            queue = [(0, start_id, [])]

            visited = set()

            while queue:
                current_time, current_station, path = heapq.heappop(queue)

                if current_station in visited:
                    continue

                visited.add(current_station)

                if path:
                    prev_station = path[-1]["to"]
                else:
                    prev_station = None

                if prev_station:
                    path = path + \
                        [{"from": prev_station, "to": current_station,
                            "line": None, "time": None}]
                else:
                    path = path

                if current_station == dest_id:
                    for step in path:
                        for neighbor, time, line in graph[step["from"]]:
                            if neighbor == step["to"]:
                                step["line"] = line
                                step["time"] = time
                                break

                    total_time = sum(step["time"]
                                     for step in path if step["time"] is not None)
                    return path, total_time

                for neighbor, time, line_name in graph.get(current_station, []):
                    if neighbor not in visited:
                        heapq.heappush(
                            queue, (current_time + time, neighbor, path))

            return None, None

        except Exception as e:
            exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def calculate_route(self,graph: defaultdict, start_station_name: str, target_station_name: str) -> models.Route:
        try:

            # get station IDs
            start_id = self.train_service.get_station_id(
                start_station_name)
            target_id = self.train_service.get_station_id(
                target_station_name)
            
            route_steps, total_time = self.find_fastest_route(graph, start_id, target_id)

            if route_steps is None:
                return None
            
            #!!WIRD WEITER GESCHRIEBEN WENN DATENBANK FRAGE GEKLÄRT IST!!

        except Exception as e:
            exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")
