#!/usr/bin/env python3
"""
Generate README.md from JSON history files.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

def load_all_history(history_dir: Path) -> Dict[str, Dict]:
    """Load all JSON history files."""
    history_data = {}
    
    for json_file in history_dir.glob('*.json'):
        # Parse filename: e.g., "15_GLO.json"
        name = json_file.stem  # "15_GLO"
        
        with open(json_file, 'r') as f:
            history_data[name] = json.load(f)
    
    return history_data

def get_region_name(variant: str) -> str:
    """Map variant code to display name."""
    names = {
        'GLO': 'Global',
        'EU': 'Europe',
        'IN': 'India',
        'CN': 'China'
    }
    return names.get(variant, variant)

def generate_device_section(device_id: str, device_name: str, history_data: Dict) -> List[str]:
    """Generate README section for one device across all regions."""
    lines = []
    
    for variant in ['GLO', 'EU', 'IN', 'CN']:
        key = f'{device_id}_{variant}'
        
        if key not in history_data:
            continue
        
        data = history_data[key]
        region_name = get_region_name(variant)
        model = data.get('model', 'Unknown')
        
        lines.append(f'### {device_name} - {region_name} ({model})')
        lines.append('')
        lines.append('| Version | ARB Index | OEM Version | First Seen | Last Checked | Status | Safe |')
        lines.append('|---------|-----------|-------------|------------|--------------|--------|------|')
        
        for entry in data.get('history', []):
            status_icon = "🟢 Current" if entry['status'] == 'current' else "⚫ Archived"
            safe_icon = "✅" if entry['arb'] == 0 else "❌"
            
            lines.append(
                f"| {entry['version']} | **{entry['arb']}** | "
                f"Major: **{entry['major']}**, Minor: **{entry['minor']}** | "
                f"{entry['first_seen']} | {entry['last_checked']} | {status_icon} | {safe_icon} |"
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
        '## 📊 Current Status & History',
        ''
    ]
    
    from config import DEVICE_ORDER, DEVICE_CONFIG

    # Device order and names
    devices = [
        (device_id, DEVICE_CONFIG[device_id]['name'])
        for device_id in DEVICE_ORDER
    ]
    
    for i, (device_id, device_name) in enumerate(devices):
        device_lines = generate_device_section(device_id, device_name, history_data)
        lines.extend(device_lines)
        
        # Add separator between devices (except last)
        if i < len(devices) - 1:
            lines.append('---')
            lines.append('')
    
    # Add footer
    lines.extend([
        '---',
        '',
        '## 📈 Legend',
        '',
        '- 🟢 **Current**: Latest firmware detected',
        '- ⚫ **Archived**: Previous firmware version',
        '- ✅ **Safe**: ARB = 0 (downgrade possible)',
        '- ❌ **Protected**: ARB > 0 (anti-rollback active)',
        '',
        '## 🛠 How it works',
        '',
        '1. **Check Update**: Checks for new firmware using the `oosdownloader` API',
        '2. **Download & Extract**: Downloads firmware and extracts `xbl_config.img`',
        '3. **Analyze**: Uses `arbextract` to read ARB index',
        '4. **Store History**: Saves to JSON in `data/history/`',
        '5. **Generate README**: Rebuilds this document from JSON',
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
    
    # Write to README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("README.md generated successfully")

if __name__ == '__main__':
    main()
