# utils/storage.py
import json
import os

def save_metadata(data, path="metadata.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_metadata(path="metadata.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def export_metadata(data, export_path):
    try:
        with open(export_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Metadata exported to {export_path}")
    except Exception as e:
        print("Export failed:", e)

def import_metadata(import_path):
    try:
        with open(import_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Import failed:", e)
        return None