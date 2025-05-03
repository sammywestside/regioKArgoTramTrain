import sys
import itertools
import heapq
from collections import defaultdict
from src.main.model import models
from src.main.service.train_service import TrainService

TRANSFER_PENALTY = 5


class Route2Service:
    def __init__(self, train_service: TrainService):
        self.train_service = train_service
        self.graph = {}
        self.station_coords = {}
        self.current_route = []
        self.current_station_index = 0
        self.pickup_drop_stations = set()

    def build_graph(self, lines: list[models.LineData]):
        graph = defaultdict(list)
        station_coords = {}

        try:
            for line in lines:
                stations = line.stations  # get line stations as list

                total_time = line.travel_time  # get total travel time of current line
                line_name = line.line_name  # get name of current line
                # print(line_name)

                # Amount of actual travel between 2 stations on the line
                segments = len(stations) - 1
                if segments == 0:
                    continue  # In case a line with only one station exists

                # The mathematical time of travel between 2 stations
                segment_time = total_time / segments
                # print(f"total time: {total_time} / segments: {segments} = segment_time: {segment_time}")

                # Loop through the whole line
                for i in range(segments):
                    current_station = stations[i].id
                    current_coords = stations[i].coordinates

                    if current_station not in station_coords:
                        station_coords[current_station] = current_coords

                    if i < len(stations) - 1:
                        next_station = stations[i + 1].id
                        next_coords = stations[i + 1].coordinates

                        if next_station not in station_coords:
                            station_coords[next_station] = next_coords

                        graph[current_station].append(
                            (next_station, segment_time, line_name))
                        graph[next_station].append(
                            (current_station, segment_time, line_name))

            self.graph = graph
            self.station_coords = station_coords

            return graph, station_coords
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def dijkstra(self, start_id, dest_id):
        try:
            heap = [(0, start_id, [])]
            visited = set()

            while heap:
                (cost, node, path) = heapq.heappop(heap)

                if node in visited:
                    continue

                path = path + [node]
                if node == dest_id:
                    return cost, path
                visited.add(node)

                for neighbor, weight, line in self.graph.get(node, []):
                    if neighbor not in visited:
                        heapq.heappush(heap, (cost + weight, neighbor, path))

            return float('inf'), []
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def build_distance_matrix(self, stations):
        try:
            matrix = {}
            for i in stations:
                matrix[i] = {}
                for j in stations:
                    if i != j:
                        dist, _ = self.dijkstra(i, j)
                        matrix[i][j] = dist
            return matrix
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def tsp_brute_force(self, matrix: dict, start: str):
        nodes = list(matrix.keys())
        nodes.remove(start)
        best_cost = float("inf")
        best_path = []

        for perm in itertools.permutations(nodes):
            cost = 0
            path = [start]
            current = start

            for node in perm:
                cost += matrix[current][node]
                current = node
                path.append(node)

            if cost < best_cost:
                best_cost = cost
                best_path = path

        return best_path, best_cost

    def calculate_travel_order(self, pick_up_station: models.Station, drop_off_station: models.Station):
        try:
            pick_up_station_id = pick_up_station.id
            drop_off_station_id = drop_off_station.id

            self.pickup_drop_stations.add(pick_up_station_id)
            self.pickup_drop_stations.add(drop_off_station_id)

            if not self.current_route:
                start_station = pick_up_station_id
                self.current_route = [pick_up_station_id]
                self.current_station_index = 0
            else:
                start_station = self.current_route[self.current_station_index]

            important_stations = list(self.pickup_drop_stations)
            if start_station not in important_stations:
                important_stations.insert(0, start_station)

            distance_matrix = self.build_distance_matrix(important_stations)

            travel_order, _ = self.tsp_brute_force(
                distance_matrix, start_station)

            full_path = []

            for i in range(len(travel_order) - 1):
                _, segment = self.dijkstra(
                    travel_order[i], travel_order[i + 1])
                if i > 0:
                    segment = segment[1:]

                full_path.extend(segment)

            self.current_route = full_path
            self.current_station_index = 0

            return full_path

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

    def build_route_object(self, full_path: list[str]) -> models.Route:
        try:
            stations: list[models.Station] = []
            transfer: list[models.Station] = []
            travel_time = 0.0
            last_line = None

            for i in range(len(full_path)):
                station_id = full_path[i]
                stations.append(
                    self.train_service.get_station_by_id(station_id))

                if i < len(full_path) - 1:
                    next_station = full_path[i+1]

                    next_hops = self.graph[station_id]
                    edge_data = next(
                        filter(lambda x: x[0] == next_station, next_hops), None)

                    if edge_data:
                        segment_time = edge_data[1]
                        line_name = edge_data[2]
                        travel_time += segment_time
                    else:
                        print(
                            f"No segment found between {station_id} and {next_station}")
                        continue

                    if last_line is not None and line_name != last_line:
                        transfer.append(
                            self.train_service.get_station_by_id(station_id))

                    last_line = line_name

            route = models.Route(
                stations=stations,
                stops=len(stations) - 1,
                transfer=transfer,
                travel_time=travel_time,
                transfer_time=TRANSFER_PENALTY
            )

            return route
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")
