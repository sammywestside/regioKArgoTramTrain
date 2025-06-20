from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.main.controller.train_controller import router as train_router
from src.main.controller.route_controller import router as route_router
from src.main.controller.robot_controller import router as robot_router
from src.main.controller.station_controller import router as station_router
from src.main.controller.package_controller import router as package_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(train_router, prefix="/api", tags=["Train"])
app.include_router(route_router, prefix="/api", tags=["Route"])
app.include_router(robot_router, prefix="/api", tags=["Robot"])
app.include_router(station_router, prefix="/api", tags=["Station"])
app.include_router(package_router, prefix="/api", tags=["Package"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
