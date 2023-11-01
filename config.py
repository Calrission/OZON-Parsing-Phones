import json

with open("config.json", "r") as file:
    config = json.loads(file.read())