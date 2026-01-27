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

DEVICE_METADATA = {
    "15": {"name": "OnePlus 15", "models": {"GLO": "CPH2747", "EU": "CPH2747", "IN": "CPH2745", "CN": "PLK110"}},
    "15R": {"name": "OnePlus 15R", "models": {"GLO": "CPH2741", "EU": "CPH2741", "IN": "CPH2741"}},
    "13": {"name": "OnePlus 13", "models": {"GLO": "CPH2649", "EU": "CPH2649", "IN": "CPH2649", "CN": "PJZ110"}},
    "12": {"name": "OnePlus 12", "models": {"GLO": "CPH2573", "EU": "CPH2573", "IN": "CPH2573", "CN": "PJD110"}}
}

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

def update_history_entry(history: Dict, version: str, arb: int, major: int, minor: int) -> bool:
    """
    Update or add a version to history.
    Returns True if this is a new current version.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if version already exists
    for entry in history['history']:
        if entry['version'] == version:
            # Update last_checked
            entry['last_checked'] = today
            return False
    
    # New version - add it
    new_entry = {
        "version": version,
        "arb": arb,
        "major": major,
        "minor": minor,
        "first_seen": today,
        "last_checked": today,
        "status": "current"
    }
    
    # Mark all existing as archived
    for entry in history['history']:
        entry['status'] = 'archived'
    
    # Insert new at beginning
    history['history'].insert(0, new_entry)
    
    return True

def main():
    if len(sys.argv) < 6:
        print("Usage: update_history.py <device_short> <variant> <version> <arb> <major> <minor>")
        sys.exit(1)
    
    device_short = sys.argv[1]
    variant = sys.argv[2]
    version = sys.argv[3]
    arb = int(sys.argv[4])
    major = int(sys.argv[5])
    minor = int(sys.argv[6])
    
    # Determine history file path
    history_file = Path(f"data/history/{device_short}_{variant}.json")
    
    # Load history
    history = load_history(history_file)
    
    # Initialize metadata if new file
    if not history.get('device'):
        metadata = DEVICE_METADATA.get(device_short, {})
        history['device'] = metadata.get('name', f'OnePlus {device_short}')
        history['device_id'] = device_short
        history['region'] = variant
        history['model'] = metadata.get('models', {}).get(variant, 'Unknown')
    
    # Update history
    is_new = update_history_entry(history, version, arb, major, minor)
    
    # Save
    save_history(history_file, history)
    
    if is_new:
        print(f"Added new version: {version}")
    else:
        print(f"Updated existing version: {version}")

if __name__ == '__main__':
    main()
