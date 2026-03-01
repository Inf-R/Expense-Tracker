import json
import os

DATA_FILE = "data.json"


class JSONStorage:
    def __init__(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({"expenses": [], "budget": {}}, f)

    def load(self):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {"expenses": [], "budget": {}}
                return json.loads(content)
        except json.JSONDecodeError:
            return {"expenses": [], "budget": {}}

    def save(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)