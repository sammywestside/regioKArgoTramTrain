import sys
import heapq
import itertools
import pdb
from collections import defaultdict

from fastapi import HTTPException
from src.main.repository.train_repository import TrainRepository
from src.main.model import models
from src.main.service.train_service import TrainService

#global variables
counter = itertools.count()
TRANSFER_PENALTY = 5


class RouteService:
    def __init__(self, train_service: TrainService):
        self.train_service = train_service

    # Create a python readable visualisation of the linesystem
    def build_graph(lines: list[models.LineData]) -> defaultdict:
        graph = defaultdict(list)

        try:
            # Loop through each line of the system
            for line in lines:
                station_objs = line.stations  # get list of all stations on current line
                # print(station_objs)
                total_time = line.travel_time  # get total travel time of current line
                line_name = line.line_name  # get name of current line
                # print(line_name)

                # Amount of actual travel between 2 stations on the line
                segments = len(station_objs) - 1
                if segments == 0:
                    continue  # In case a line with only one station exists

                # The mathematical time of travel between 2 stations
                segment_time = total_time / segments
                # print(f"total time: {total_time} / segments: {segments} = segment_time: {segment_time}")

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
            exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}: {e}")

    def find_fastest_route(graph: defaultdict, start_id: str, dest_id: str):
        if start_id == dest_id:
            print("start- and dest-station are the same...")
            return [], 0

        if start_id not in graph or dest_id not in graph:
            print("Start or Dest not in graph.")
            return None, None

        try:
            # (total time, _, current_station, path_taken)
            queue = [(0,next(counter), start_id, [])]

            visited_set = set()

            while queue:
                current_time, _, current_station, path = heapq.heappop(queue)

                if current_station in visited_set:
                    continue

                visited_set.add(current_station)

                if current_station == dest_id:
                    total_time = sum(step["time"]
                                     for step in path if step["time"] is not None)
                    return path, total_time
                else:
                    keys = graph.get(current_station, [])
                    for neighbor, time, line_name in keys:
                        if neighbor not in visited_set:
                            new_step = {
                                "from": current_station,
                                "to": neighbor,
                                "line": line_name,
                                "time": time,
                            }
                            heapq.heappush(
                                queue, (current_time + time, next(counter), neighbor, path + [new_step]))

            return None, None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def calculate_route(self, graph: defaultdict, start_station_name: str, target_station_name: str) -> models.Route:
        try:
            # get station IDs
            start_id = self.train_service.get_station_id(
                start_station_name)
            target_id = self.train_service.get_station_id(
                target_station_name)
            

            route_steps, total_time = self.find_fastest_route(
                graph, start_id, target_id)

            station_map = self.train_service.build_station_map()

            stations = [station_map[route_steps[0]["from"]]] + \
                [station_map[step["to"]] for step in route_steps]
            
            stops = len(stations) - 1

            transfers = []
            last_line = None
            for step in route_steps:
                if last_line and step["line"] != last_line:
                    transfers.append(station_map[step["from"]])
                last_line = step["line"]

            transfer_time = TRANSFER_PENALTY 	#Simulated Value can be changed for more realistic times

            return models.Route(
                stations=stations,
                stops=stops,
                transfer=transfers,
                travel_time=total_time + transfer_time,
                transfer_time=transfer_time
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")
   
