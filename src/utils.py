import json


def read_data():
    with open("database.json", "r") as f:
        return json.load(f)


def write_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)
