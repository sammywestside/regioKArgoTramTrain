from src.main.service.train_service import TrainService
from src.main.repository.train_repository import TrainRepository
from src.main.model.models import Coordinates, Station

def test_get_line_data():
    repo = TrainRepository()
    service = TrainService(repo)
    result = service.get_all_line_stations("4")

    test_coords = Coordinates(lat="48.9489398993136", long="8.62017058434104")
    station_id = service.get_station_id_by_coords(test_coords)
    station: Station = service.get_station_by_id(station_id)
    # print("Station: ", first_station.name)
    # print("Coordinates: ", first_station.coordinates.lat, first_station.coordinates.long)

    # print(draw_result)
    print(f"Station name: {station.name}")
    
    assert station_id is not None
    assert result.line_name == "4"
    assert all(isinstance(station.name, str) for station in result.stations)
    assert all(hasattr(station.coordinates, "lat") and hasattr(station.coordinates, "long") for station in result.stations)
