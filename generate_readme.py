#!/usr/bin/env python3
"""
Generate README.md from JSON history files.
Matches the requested layout from main branch with all regions in one table per device.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from config import REGIONS, DEVICE_ORDER_LIST

def load_all_history(history_dir: Path) -> Dict[str, Dict]:
    """Load all JSON history files."""
    history_data = {}
    
    for json_file in history_dir.glob('*.json'):
        # Parse filename: e.g., "12_CN.json"
        name = json_file.stem
        
        try:
            with open(json_file, 'r') as f:
                history_data[name] = json.load(f)
        except Exception:
            continue
    
    return history_data

def get_region_name(variant: str) -> str:
    """Map variant code to display name for the table."""
    return REGIONS.get(variant, variant)

def generate_device_section(device_id: str, device_name: str, history_data: Dict) -> List[str]:
    """Generate a single table for one device across all regions."""
    lines = [f'### {device_name}', '']
    
    # Check if we have any data for this device
    active_regions = []
    for variant in REGIONS:
        key = f'{device_id}_{variant}'
        if key in history_data:
            active_regions.append(variant)
            
    if not active_regions:
        return []

    lines.append('| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |')
    lines.append('|--------|-------|------------------|-----------|-------------|--------------|------|')
    
    for variant in REGIONS:
        key = f'{device_id}_{variant}'
        if key not in history_data:
            continue
            
        data = history_data[key]
        region_name = get_region_name(variant)
        model = data.get('model', 'Unknown')
        
        # Get only the current version for the main table
        current_entry = None
        for entry in data.get('history', []):
            if entry['status'] == 'current':
                current_entry = entry
                break
        
        if not current_entry:
            # Fallback if no current is explicitly marked
            if data.get('history'):
                current_entry = data['history'][0]
            else:
                lines.append(f'| {region_name} | {model} | *Waiting for scan...* | - | - | - | - |')
                continue

        safe_icon = "✅" if current_entry['arb'] == 0 else "❌"
        ver = current_entry.get('version', '')
        if not ver:
            ver = "*Unknown*"
            
        lines.append(
            f"| {region_name} | {model} | {ver} | **{current_entry['arb']}** | "
            f"Major: **{current_entry['major']}**, Minor: **{current_entry['minor']}** | "
            f"{current_entry['last_checked']} | {safe_icon} |"
        )
    
    lines.append('')
    return lines

def generate_readme(history_data: Dict) -> str:
    """Generate complete README content."""
    lines = [
        '# OnePlus Anti-Rollback (ARB) Checker',
        '',
        'Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.',
        '',
        '## 📊 Current Status',
        ''
    ]
    
    for i, (device_id, device_name) in enumerate(DEVICE_ORDER_LIST):
        device_lines = generate_device_section(device_id, device_name, history_data)
        if device_lines:
            lines.extend(device_lines)
            if i < len(DEVICE_ORDER_LIST) - 1:
                lines.append('---')
                lines.append('')
    
    # Add footer
    lines.extend([
        '',
        '> [!IMPORTANT]',
        '> This status is updated automatically by GitHub Actions. Some device/region combinations may not be available and will show as "Waiting for scan...".',
        '',
        '## 📈 Legend',
        '',
        '- ✅ **Safe**: ARB = 0 (downgrade possible)',
        '- ❌ **Protected**: ARB > 0 (anti-rollback active)',
        '',
        '## 🤖 Workflow Status',
        '[![Check ARB](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml)'
    ])
    
    return '\n'.join(lines) + '\n'

def main():
    history_dir = Path('data/history')
    
    if len(sys.argv) > 1:
        history_dir = Path(sys.argv[1])
    
    if not history_dir.exists():
        print(f"Error: History directory not found: {history_dir}", file=sys.stderr)
        sys.exit(1)
    
    history_data = load_all_history(history_dir)
    readme_content = generate_readme(history_data)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully")

if __name__ == '__main__':
    main()
