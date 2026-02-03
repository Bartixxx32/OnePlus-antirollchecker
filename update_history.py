#!/usr/bin/env python3
"""
Update JSON history files with new ARB check results.
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict
from config import DEVICE_METADATA, get_display_name, get_model_number

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
        # Just append historical to the end
        history['history'].append(new_entry)
        return False

def main():
    parser = argparse.ArgumentParser(description="Update firmware history JSON.")
    
    # Mode 1: Detailed Arguments
    parser.add_argument("device_short", nargs='?', help="Device short code (e.g., 15)")
    parser.add_argument("variant", nargs='?', help="Region variant (CN, EU, GLO, IN)")
    parser.add_argument("version", nargs='?', help="Firmware version string")
    parser.add_argument("arb", nargs='?', type=int, help="ARB index")
    parser.add_argument("major", nargs='?', type=int, help="Keymaster major version")
    parser.add_argument("minor", nargs='?', type=int, help="Keymaster minor version")
    
    # Mode 2: JSON Input
    parser.add_argument("--json-file", help="Path to result.json containing the data")
    
    parser.add_argument("--historical", action="store_true", help="Flag to indicate historical data backfill")
    
    args = parser.parse_args()
    
    # Data extraction logic
    device_short = args.device_short
    variant = args.variant
    version = args.version
    arb = args.arb
    major = args.major
    minor = args.minor
    
    if args.json_file:
        try:
            with open(args.json_file, 'r') as f:
                data = json.load(f)
            # Keys might vary, let's normalize
            # Expecting: device_short, variant, version, arb_index (or arb), major, minor
            device_short = data.get('device_short') or device_short
            variant = data.get('variant') or variant
            version = data.get('version') or version
            arb = int(data.get('arb_index') if data.get('arb_index') is not None else data.get('arb'))
            major = int(data.get('major', 0))
            minor = int(data.get('minor', 0))
            
            if not all([device_short, variant, version, arb is not None]):
                print("Error: Missing required fields in JSON file")
                sys.exit(1)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            sys.exit(1)
    
    if not all([device_short, variant, version, arb is not None]):
        parser.print_help()
        sys.exit(1)

    history_file = Path(f"data/history/{device_short}_{variant}.json")
    history = load_history(history_file)
    
    if not history.get('device'):
        history['device'] = get_display_name(device_short)
        history['device_id'] = device_short
        history['region'] = variant
        
        model_num = get_model_number(device_short, variant)
        if model_num == "Unknown" and version and "_" in version:
            # Try to extract from version string (e.g., PKG110_16...)
            extracted = version.split("_")[0]
            if extracted.isalnum() and len(extracted) > 3:
                model_num = extracted
        
        history['model'] = model_num
    
    is_new = update_history_entry(history, version, int(arb), int(major), int(minor), args.historical)
    save_history(history_file, history)
    
    if is_new:
        print(f"Added new version: {version}")
    else:
        print(f"Updated existing version: {version}")

if __name__ == '__main__':
    main()
