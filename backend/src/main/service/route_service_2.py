import sys
import itertools
import heapq
from collections import defaultdict
from src.main.model import models
from src.main.service.train_service import TrainService


TRANSFER_PENALTY = 5
counter = itertools.count()

class Route2Service:
    def __init__(self, train_service: TrainService, reload_stations: list[str]):
        self.train_service = train_service
        self.graph = {}
        self.reload_stations = set(reload_stations)
        self.current_route = []
        self.current_station_index = 0
        self.station_coords = {}

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

            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")

### NEW APPROACH!!!
    def _dijkstra_all(self, start_id: str) -> dict[str, float]:
        heap = [(0, next(counter), start_id)]
        visited = set()
        distances = {}

        while heap:
            cost, _, node = heapq.heappop(heap)

            if node in visited:
                continue

            visited.add(node)
            distances[node] = cost
            
            for neighbor, weight, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + weight, next(counter), neighbor))
        
        return distances
    
    def _count_line_changes(self, path) -> int:
        changes = 0
        last_line = None
        for _, line in path:
            if last_line is not None and line != last_line:
                changes += 1
            
            last_line = line
        
        return changes

    def _build_distance_matrix(self, stations: list[str]) -> dict[tuple[str, str], float]:
        distance_matrix = {}

        for start in stations:
            # distances = self._dijkstra_all(start)
            for dest in stations:
                if start == dest:
                    continue
                cost, path = self._dijkstra(start, dest)
                line_changes = self._count_line_changes(path)
                adjusted_cost = cost + line_changes * TRANSFER_PENALTY
                distance_matrix[(start, dest)] = adjusted_cost
        
        return distance_matrix

    def _solve_tsp(self, start: str, targets: list[str], distances: dict[tuple[str, str], float]) -> list[str]:
        best_cost = float("inf")
        best_path = []

        for perm in itertools.permutations(targets):
            cost = 0.0
            path = [start]
            current = start

            for node in perm:
                cost += distances[(current, node)]
                current = node
                path.append(node)

            if cost < best_cost:
                best_cost = cost
                best_path = path
        
        return best_path

    def _dijkstra(self, start_id: str, dest_id: str):
        heap = [(0,next(counter), start_id, None)]
        visited = set()
        parent = {}
        cost_map = {}

        if start_id not in self.graph:
            print(f"Start node {start_id} missing in graph")
        if dest_id not in self.graph:
            print(f"Destination node {dest_id} missing in graph")


        while heap:
            cost, _, node, current_line = heapq.heappop(heap)

            if (node, current_line) in visited:
                continue
            
            visited.add((node, current_line))
            
            if node == dest_id:
                path = []
                key = (node, current_line)
                while key in parent:
                    prev_node, prev_line = parent[key]
                    path.append((key[0], key[1]))
                    key = (prev_node, prev_line)
                return cost, path[::-1]

            for neighbor, weight, neighbor_line in self.graph.get(node, []):
                line_changed = current_line is not None and neighbor_line != current_line
                transfer_cost = TRANSFER_PENALTY if line_changed else 0

                new_cost = cost + weight + transfer_cost
                neighbor_key = (neighbor, neighbor_line)

                if neighbor_key not in cost_map or new_cost < cost_map[neighbor_key]:
                    cost_map[neighbor_key] = new_cost
                    parent[neighbor_key] = (node, current_line)
                    heapq.heappush(heap, (new_cost, next(counter), neighbor, neighbor_line))

        print(f"Dijkstra failed: no path from {start_id} to {dest_id}")
        return float("inf"), []

    def _get_shortest_path(self, start: str, end: str) -> list[str]:
        _, path = self._dijkstra(start, end)
        return path
            
    def calculate_delivery_route(self, current_station_id: str, delivery_targets: list[str]):
        all_stations = [current_station_id] + delivery_targets
        distances = self._build_distance_matrix(all_stations)
        tsp_order = self._solve_tsp(current_station_id, delivery_targets, distances)

        delivery_path: list[tuple] = []
        prev_station = None
        total_cost = 0.0

        for station in tsp_order:
            if prev_station == None:
                prev_station = station
                continue

            segment_cost, segment_path = self._dijkstra(prev_station, station)
            delivery_path.extend(segment_path)
            prev_station = station
            total_cost += segment_cost

        return delivery_path, total_cost

    def calculate_reload_route(self, current_station_id: str, station_package_counts: dict[str, int]) -> list[str]:
        candidates = [
            s for s in self.reload_stations if station_package_counts.get(s, 0) > 0
        ]
        print(f"candidates: {candidates}")
        if not candidates:
            return []
        
        best_score = -1
        best_path = []
        best_path_cost = 0.0

        for s in candidates:
            path_cost, path = self._dijkstra(current_station_id, s)
            packages = station_package_counts[s]
            score = packages / path_cost

            if score > best_score:
                best_score = score
                best_path = path 
                best_path_cost = path_cost
        
        path_to_best = best_path
        return path_to_best, best_path_cost

    def build_route_object(self, full_path: list[tuple], total_cost) -> models.Route:
        try:
            stations: list[models.Station] = []
            transfer: list[models.Station] = []
            segments = []
            current_segment = []
            last_line = None

            for i, (station_id, line) in enumerate(full_path):
                station = self.train_service.get_station_by_id(station_id)
                stations.append(station)

                if last_line is None or line == last_line:
                    current_segment.append(station)
                else:
                    segments.append(current_segment)
                    current_segment = [station]
                    transfer.append(station)

                last_line = line
            
            if current_segment:
                segments.append(current_segment)

            route = models.Route(
                stations=stations,
                stops=len(stations) - 1,
                transfer=transfer,
                travel_time=total_cost,
                transfer_time=TRANSFER_PENALTY * len(transfer),
                segments=segments
            )

            return route
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"An error occured on line: {exc_tb.tb_lineno}; Type: {exc_type}: {e}")
