import os
import json

CONFIG_PATH = os.path.expanduser("~/.context-cli/config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {"url": "http://localhost:6333", "api_key": None}

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)