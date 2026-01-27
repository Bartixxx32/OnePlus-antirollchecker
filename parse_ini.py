#!/usr/bin/env python3
"""
Parse firmware history from INI file and extract top N versions for each device/region.
"""

import sys
import re
from typing import List, Dict
from config import DEVICE_SHORT_TO_NAME

def get_section_name(device_short: str, variant: str) -> str:
    """Map device + variant to INI component name."""
    device_name = DEVICE_SHORT_TO_NAME.get(device_short, device_short)
    return f"{device_name} {variant}"

def parse_ini_section(ini_content: str, section_name: str, max_versions: int = 4) -> List[Dict[str, str]]:
    """
    Parse a section from INI using regex for robustness.
    """
    # Find the section index
    # Sections are like [OP 15 CN]
    section_regex = re.compile(rf'^\[{re.escape(section_name)}\]', re.IGNORECASE | re.MULTILINE)
    match = section_regex.search(ini_content)
    if not match:
        return []
    
    # Get the content until the next section
    start_pos = match.end()
    next_section = re.search(r'^\[', ini_content[start_pos:], re.MULTILINE)
    if next_section:
        section_block = ini_content[start_pos:start_pos + next_section.start()]
    else:
        section_block = ini_content[start_pos:]
        
    results = []
    # Extract url and version pairs. They appear in sequence.
    # url=...
    # version=...
    # We find all keys and values first
    kv_pairs = re.findall(r'^(\w+)=(.*)$', section_block, re.MULTILINE)
    
    current_url = None
    for key, value in kv_pairs:
        key = key.lower()
        if key == 'url':
            current_url = value.strip()
        elif key == 'version':
            version = value.strip()
            if version and current_url:
                if not any(r['version'] == version for r in results):
                    results.append({'version': version, 'url': current_url})
                current_url = None
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
    
    try:
        with open(ini_file, 'r', encoding='utf-8', errors='ignore') as f:
            ini_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    results = parse_ini_section(ini_content, section_name)
    
    # Output as pipe-separated version|url
    for r in results:
        print(f"{r['version']}|{r['url']}")

if __name__ == '__main__':
    main()
