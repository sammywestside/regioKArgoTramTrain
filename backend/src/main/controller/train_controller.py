from ast import Return
from fastapi import APIRouter, HTTPException
from src.main.service.train_service import TrainService
from src.main.repository.repository_container import train_repo_singleton as train_repo
from src.main.model.models import LineData

router = APIRouter()
train_service = TrainService(train_repo)


# Get all lines
@router.get("/lines")
def get_all_lines():
    try:
        lines_data = train_repo.load_lines_v2()
        return lines_data.get("lines", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get line coords
@router.get("/line/coords/{line_id}")
def get_line_coords(line_id: str):
    try:
        coords = train_service.get_line_draw_coords(line_id)
        if not coords:
            raise HTTPException(status_code=404, detail="Line not found or has no coordinates.")
        return {"lines_id": line_id, "coordinates": coords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get all stations from a line
@router.get("/line/stations/{lines_id}", response_model=LineData)
def get_all_line_stations(line_id: str):
    try:
        line_data = train_service.get_all_line_stations(line_id)
        if line_data is None:
            raise HTTPException(status_code=404, detail="Line not found")
        return line_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))