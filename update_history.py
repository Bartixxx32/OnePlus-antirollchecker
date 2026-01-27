#!/usr/bin/env python3
"""
Update JSON history files with new ARB check results.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from config import get_device_metadata

DEVICE_METADATA = get_device_metadata()

def load_history(history_file: Path) -> Dict:
    """Load existing history JSON or create new structure."""
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return {"history": []}

def save_history(history_file: Path, data: Dict):
    """Save history JSON."""
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with open(history_file, 'w') as f:
        json.dump(data, f, indent=2)

def update_history_entry(history: Dict, version: str, arb: int, major: int, minor: int, is_historical: bool = False) -> bool:
    """
    Update or add a version to history.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if version already exists
    for entry in history['history']:
        if entry['version'] == version:
            entry['last_checked'] = today
            if not is_historical and entry['status'] == 'archived':
                # Promote to current
                for e in history['history']:
                    e['status'] = 'archived'
                entry['status'] = 'current'
                # Move to top
                history['history'].remove(entry)
                history['history'].insert(0, entry)
                return True
            return False
    
    # New version - add it
    new_entry = {
        "version": version,
        "arb": arb,
        "major": major,
        "minor": minor,
        "first_seen": today,
        "last_checked": today,
        "status": "archived" if is_historical else "current"
    }
    
    if not is_historical:
        # Mark all existing as archived
        for entry in history['history']:
            entry['status'] = 'archived'
        # Insert new at beginning
        history['history'].insert(0, new_entry)
        return True
    else:
        # Just append historical to the end (or keep sorted by version)
        history['history'].append(new_entry)
        # Optional: Sort history by some logic (e.g. version string)
        return False

def main():
    args = sys.argv[1:]
    is_historical = False
    if "--historical" in args:
        is_historical = True
        args.remove("--historical")

    if len(args) < 6:
        print("Usage: update_history.py [--historical] <device_short> <variant> <version> <arb> <major> <minor>")
        sys.exit(1)
    
    device_short = args[0]
    variant = args[1]
    version = args[2]
    arb = int(args[3])
    major = int(args[4])
    minor = int(args[5])
    
    # ... rest of the logic ...
    history_file = Path(f"data/history/{device_short}_{variant}.json")
    history = load_history(history_file)
    
    if not history.get('device'):
        metadata = DEVICE_METADATA.get(device_short, {})
        history['device'] = metadata.get('name', f'OnePlus {device_short}')
        history['device_id'] = device_short
        history['region'] = variant
        history['model'] = metadata.get('models', {}).get(variant, 'Unknown')
    
    is_new = update_history_entry(history, version, arb, major, minor, is_historical)
    save_history(history_file, history)
    
    if is_new:
        print(f"Added new version: {version}")
    else:
        print(f"Updated existing version: {version}")

if __name__ == '__main__':
    main()
