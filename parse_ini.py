#!/usr/bin/env python3
"""
Parse firmware history from INI file and extract top N versions for each device/region.
"""

import sys
from typing import List, Dict

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
    
    return f'[{device_name} {variant}]'

def parse_ini_section(ini_content: str, section_name: str, max_versions: int = 4) -> List[Dict[str, str]]:
    """
    Parse a section from INI and extract versions and URLs.
    """
    lines = ini_content.split('\n')
    results = []
    in_section = False
    current_url = None
    
    for line in lines:
        line = line.strip()
        
        # Check if we're entering the target section
        if line == section_name:
            in_section = True
            continue
        
        # Check if we've entered a different section
        if line.startswith('[') and in_section:
            break
        
        if not in_section:
            continue
        
        # Parse URL and version lines
        if line.startswith('url='):
            current_url = line.split('=', 1)[1].strip()
        elif line.startswith('version='):
            version = line.split('=', 1)[1].strip()
            if version and current_url:
                # Avoid duplicates
                if not any(r['version'] == version for r in results):
                    results.append({'version': version, 'url': current_url})
                current_url = None # Reset for next pair
                if len(results) >= max_versions:
                    break
    
    return results

def main():
    if len(sys.argv) < 4:
        print("Usage: parse_ini.py <ini_file> <device_short> <variant>")
        sys.exit(1)
    
    ini_file = sys.argv[1]
    device_short = sys.argv[2]
    variant = sys.argv[3]
    
    section_name = get_section_name(device_short, variant)
    
    if not section_name:
        print(f"Unknown device: {device_short}", file=sys.stderr)
        sys.exit(1)
    
    # Read INI file
    with open(ini_file, 'r', encoding='utf-8', errors='ignore') as f:
        ini_content = f.read()
    
    results = parse_ini_section(ini_content, section_name)
    
    # Output as pipe-separated version|url
    for r in results:
        print(f"{r['version']}|{r['url']}")

if __name__ == '__main__':
    main()
