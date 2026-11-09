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

def coerce_int(value, default: int = -1) -> int:
    """Parse an int from CLI/JSON values, treating Unknown as ``default``."""
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    text = str(value).strip().lower()
    if text in ("", "none", "null", "unknown", "?", "error", "n/a"):
        return default
    try:
        return int(text)
    except ValueError:
        try:
            return int(float(text))
        except ValueError:
            return default


def normalize_package_type(value):
    """Return ``incremental``/``full`` or ``None`` for unknown values."""
    if not value:
        return None
    value = str(value).strip().lower()
    if value in ("incremental", "delta", "incremental_ota", "incremental-ota"):
        return "incremental"
    if value in ("full", "full_ota", "full-ota"):
        return "full"
    return None


def update_history_entry(
    history: Dict,
    version: str,
    arb: int,
    major: int,
    minor: int,
    is_historical: bool = False,
    md5: str = None,
    package_type: str = None,
) -> bool:
    """
    Update or add a version to history.

    ``arb`` may be ``-1`` when a package is valid but its ARB record cannot
    be parsed; such entries are kept and marked ``arb_detected: false``.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    package_type = normalize_package_type(package_type)
    arb_detected = arb is not None and int(arb) >= 0

    # Check if version already exists
    for entry in history['history']:
        if entry['version'] == version:
            entry['last_checked'] = today
            # Update MD5 if provided and check for changes
            if md5:
                if entry.get('md5') and entry['md5'] != md5:
                    print(f"WARNING: MD5 changed for version {version}: {entry['md5']} -> {md5}")
                entry['md5'] = md5

            # A later run may learn the package type or recover an ARB value
            # that an older parser could not read.
            if package_type:
                entry['package_type'] = package_type
            if arb_detected and coerce_int(entry.get('arb'), -1) < 0:
                entry['arb'] = int(arb)
                entry['major'] = int(major)
                entry['minor'] = int(minor)
                entry['arb_detected'] = True
            elif (
                not arb_detected
                and coerce_int(entry.get('arb'), -1) < 0
            ):
                entry['arb_detected'] = False

            # If it's already in history, we don't change its status/position
            # to avoid demoting a newer 'current' version by re-checking an old one.

            # Sort before returning
            history['history'].sort(key=lambda x: (x['status'] == 'current', x['first_seen'], x['version']), reverse=True)
            return False

    # New version - add it
    new_entry = {
        "version": version,
        "arb": int(arb),
        "major": int(major),
        "minor": int(minor),
        "arb_detected": arb_detected,
        "first_seen": today,
        "last_checked": today,
        "status": "archived" if is_historical else "current"
    }

    if package_type:
        new_entry["package_type"] = package_type

    if md5:
        new_entry["md5"] = md5
    
    if not is_historical:
        # Mark all existing as archived because we found a NEW current version
        for entry in history['history']:
            entry['status'] = 'archived'
        history['history'].insert(0, new_entry)
    else:
        # Just append historical to the end, sorting will fix position
        history['history'].append(new_entry)
    
    # Final sorting: status 'current' first, then first_seen DESC, then version DESC
    history['history'].sort(key=lambda x: (x['status'] == 'current', x['first_seen'], x['version']), reverse=True)
    return not is_historical

def main():
    parser = argparse.ArgumentParser(description="Update firmware history JSON.")
    
    # Mode 1: Detailed Arguments
    parser.add_argument("device_short", nargs='?', help="Device short code (e.g., 15)")
    parser.add_argument("variant", nargs='?', help="Region variant (CN, EU, GLO, IN)")
    parser.add_argument("version", nargs='?', help="Firmware version string")
    parser.add_argument("arb", nargs='?', help="ARB index (or ? when undetectable)")
    parser.add_argument("major", nargs='?', help="Keymaster major version")
    parser.add_argument("minor", nargs='?', help="Keymaster minor version")
    
    parser.add_argument("--md5", help="MD5 checksum of the firmware", default=None)
    parser.add_argument(
        "--package-type",
        choices=["incremental", "full", "unknown"],
        default=None,
        help="OTA package type (incremental/full/unknown)",
    )
    
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
    package_type = args.package_type
    
    if args.json_file:
        try:
            with open(args.json_file, 'r') as f:
                data = json.load(f)
            # Keys might vary, let's normalize
            # Expecting: device_short, variant, version, arb_index (or arb), major, minor
            device_short = data.get('device_short') or device_short
            variant = data.get('variant') or variant
            version = data.get('version') or version
            arb_value = data.get('arb_index')
            if arb_value is None:
                arb_value = data.get('arb')
            arb = coerce_int(arb_value, -1)
            major = coerce_int(data.get('major'), 0)
            minor = coerce_int(data.get('minor'), 0)
            package_type = package_type or data.get('package_type')
            if not args.md5 and data.get('md5'):
                args.md5 = data.get('md5')
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            sys.exit(1)
    else:
        arb = coerce_int(arb, -1)
        major = coerce_int(major, 0)
        minor = coerce_int(minor, 0)

    if not all([device_short, variant, version]):
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
    
    is_new = update_history_entry(
        history,
        version,
        int(arb),
        int(major),
        int(minor),
        args.historical,
        md5=args.md5,
        package_type=package_type,
    )
    save_history(history_file, history)
    
    if is_new:
        print(f"Added new version: {version}")
        # Write to GITHUB_OUTPUT if available
        import os
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("is_new=true\n")
    else:
        print(f"Updated existing version: {version}")

if __name__ == '__main__':
    main()
