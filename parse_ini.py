#!/usr/bin/env python3
"""
Parse firmware history from INI file and extract top N versions for each device/region.
"""

import configparser
import sys
from typing import Dict, List, Tuple

def parse_ini_file(ini_path: str) -> configparser.ConfigParser:
    """Load and parse the INI file."""
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf-8')
    return config

def get_section_name(device_short: str, variant: str) -> str:
    """Map device + variant to INI section name."""
    device_map = {
        '15': 'OP 15',
        '15R': 'OP 15R',
        '13': 'OP 13',
        '12': 'OP 12'
    }
    
    device_name = device_map.get(device_short, '')
    if not device_name:
        return None
    
    return f'{device_name} {variant}'

def extract_versions(config: configparser.ConfigParser, section: str, max_versions: int = 4) -> List[Dict]:
    """Extract top N versions from a section."""
    if section not in config:
        print(f"Warning: Section [{section}] not found in INI", file=sys.stderr)
        return []
    
    versions = []
    current_version = None
    
    for key in config[section]:
        if key == 'version':
            # This is a simple parser - assumes version appears before url/patch
            current_version = config[section][key]
        elif key == 'url' and current_version:
            versions.append({
                'version': current_version,
                'url': config[section].get(f'url', ''),
                'patch': config[section].get('patch', '')
            })
            current_version = None
    
    # Return top N versions
    return versions[:max_versions]

def main():
    if len(sys.argv) < 4:
        print("Usage: parse_ini.py <ini_file> <device_short> <variant>")
        sys.exit(1)
    
    ini_file = sys.argv[1]
    device_short = sys.argv[2]
    variant = sys.argv[3]
    
    config = parse_ini_file(ini_file)
    section = get_section_name(device_short, variant)
    
    if not section:
        print(f"Unknown device: {device_short}", file=sys.stderr)
        sys.exit(1)
    
    versions = extract_versions(config, section)
    
    # Output as newline-separated versions
    for v in versions:
        print(v['version'])

if __name__ == '__main__':
    main()
