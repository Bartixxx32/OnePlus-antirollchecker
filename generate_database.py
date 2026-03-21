import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from config import DEVICE_METADATA, DEVICE_ORDER
from hardcode_rules import is_hardcode_protected, version_sort_key

def load_history(file_path: Path) -> Dict:
    """Load history from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



def generate_database():
    """Generates a unified database.json from history files."""
    history_dir = Path("data/history")
    if not history_dir.exists():
        print("History directory not found.")
        return

    database = {}

    # Iterate over all JSON files in the history directory
    for file_path in history_dir.glob("*.json"):
        data = load_history(file_path)
        if not data:
            continue

        device_id = data.get("device_id")
        model = data.get("model")
        device_name = data.get("device")
        region = data.get("region")

        if not model:
            continue
            
        # Initialize model entry if not exists
        if model not in database:
            try:
                order = DEVICE_ORDER.index(device_id)
            except ValueError:
                order = 999
            
            database[model] = {
                "device_name": device_name,
                "device_order": order,
                "versions": {}
            }
        
        # Process history entries
        for entry in data.get("history", []):
            version_str = entry.get("version")
            if not version_str:
                continue

            if version_str not in database[model]["versions"]:
                database[model]["versions"][version_str] = {
                    "arb": entry.get("arb", -1),
                    "major": entry.get("major", -1),
                    "minor": entry.get("minor", -1),
                    "md5": entry.get("md5"),
                    "first_seen": entry.get("first_seen"),
                    "last_checked": entry.get("last_checked"),
                    "status": entry.get("status"),
                    "is_hardcoded": is_hardcode_protected(device_id, version_str),
                    "regions": [region]
                }
            else:
                # Append region if not already present
                if region not in database[model]["versions"][version_str]["regions"]:
                    database[model]["versions"][version_str]["regions"].append(region)

    # Convert versions dict to sorted list (descending by firmware version number)
    output_database = {}
    for model, model_data in sorted(database.items()):
        sorted_versions = sorted(
            [{"version": v, **info} for v, info in model_data["versions"].items()],
            key=lambda x: version_sort_key(x["version"]),
            reverse=True
        )
        output_database[model] = {
            "device_name": model_data["device_name"],
            "device_order": model_data["device_order"],
            "versions": sorted_versions
        }

    # Write to database.json
    output_path = Path("data/database.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_database, f, indent=2)
    
    print(f"Generated {output_path} with {len(output_database)} models.")

if __name__ == "__main__":
    generate_database()
