import csv
import json

stations = "../json\haltestellen_v2-1.json"

with open (stations) as f:
    reader = csv.DictReader(f)

    for row in reader:
        row["name"]

