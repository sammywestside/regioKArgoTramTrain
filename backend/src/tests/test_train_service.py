from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository

def test_get_line_data():
    repo = TrainRepository()
    service = TrainService(repo)
    result = service.get_all_line_stations("1")
    
    first_station = result.stations[0]
    print("Station: ", first_station.name)
    print("Coordinates: ", first_station.coordinates.lat, first_station.coordinates.long)

    assert result.line_name == "1"
    assert all(isinstance(station.name, str) for station in result.stations)
    assert all(hasattr(station.coordinates, "lat") and hasattr(station.coordinates, "long") for station in result.stations)