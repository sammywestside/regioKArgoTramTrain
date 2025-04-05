from service.train_service import TrainServie

class TrainController: 
    def __init__(self, train_service: TrainServie):
        self.train_service = train_service