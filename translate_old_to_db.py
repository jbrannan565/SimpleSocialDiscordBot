import os
import json
from db.mongo import create_resource

directory = './resources'

for filename in os.listdir(directory):
    path = f"{directory}/{filename}"
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            create_resource(filename, data)
