from src.main.controller.train_controller import TrainController
from fastapi import FastAPI
import uvicorn

app = FastAPI()

controller = TrainController()

app.include_router(controller.router, prexix="/api", tags=["route"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)