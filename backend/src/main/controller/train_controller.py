from service.train_service import TrainService
from fastapi import APIRouter

class TrainController: 
    def __init__(self, train_service: TrainService):
        self.train_service = train_service
        self.router = APIRouter()
        print("DONE.")