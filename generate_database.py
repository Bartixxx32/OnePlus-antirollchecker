import json
from pathlib import Path
from typing import Dict, List, Optional
from config import DEVICE_METADATA

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
            database[model] = {
                "device_name": device_name,
                "versions": {}
            }
        
        # Process history entries
        for entry in data.get("history", []):
            version_str = entry.get("version")
            if not version_str:
                continue

            # If version already exists, we might want to merge or check for consistency
            # For now, we assume the data is consistent or simply overwrite/append region info if we wanted to track regions per version.
            # The current requirement is just to look up by model and version.
            
            if version_str not in database[model]["versions"]:
                database[model]["versions"][version_str] = {
                    "arb": entry.get("arb", -1),
                    "major": entry.get("major", -1),
                    "minor": entry.get("minor", -1),
                    "md5": entry.get("md5"),
                    "status": entry.get("status"), # Keep the status from the file (current/archived) - though this might be region specific. 
                                                   # If a version is current in one region and archived in another, this might be ambiguous.
                                                   # But usually the version string is unique enough or we just care about the ARB.
                    "regions": [region]
                }
            else:
                # Append region if not already present
                if region not in database[model]["versions"][version_str]["regions"]:
                    database[model]["versions"][version_str]["regions"].append(region)
                
                # Update status? If it's current in ANY region, maybe we should mark it? 
                # Or just leave it as is. The user just wants to check fuse (arb).
                # ARB should be constant for the same version string.

    # Write to database.json
    output_path = Path("data/database.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, sort_keys=True)
    
    print(f"Generated {output_path} with {len(database)} models.")

if __name__ == "__main__":
    generate_database()
