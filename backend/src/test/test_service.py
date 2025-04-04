import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from main.repository.train_repository import TrainRepository
from main.service.train_service import TrainService

class test_train_service(unittest.TestCase):
    repo = TrainRepository()
    service = TrainService(repo)

if __name__ == "__main__":
    print(test_train_service.service.get_all_line_station_coords("1"))