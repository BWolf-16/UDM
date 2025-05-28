import json
import os

def save_metadata(data, path="metadata.json"):
    """Save metadata dictionary to a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_metadata(path="metadata.json"):
    """Load metadata from a JSON file, or return empty dict if not found."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def export_metadata(data, export_path):
    """Export metadata to user-specified JSON path."""
    try:
        with open(export_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Export failed:", e)

def import_metadata(import_path):
    """Import metadata from JSON file."""
    try:
        with open(import_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Import failed:", e)
        return None
