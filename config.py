import os
import sys
import json

def get_config_path():
    if getattr(sys, 'frozen', False):
        # EXE: рядом с исполняемым файлом
        return os.path.join(os.path.dirname(sys.executable), "config.json")
    else:
        # IDE/разработка
        return os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    path = get_config_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(data: dict):
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
