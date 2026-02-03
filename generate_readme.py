#!/usr/bin/env python3
"""
Generate README.md from JSON history files.
Matches the requested layout from main branch with all regions in one table per device.
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List
from config import DEVICE_METADATA, DeviceModels, DEVICE_ORDER, HISTORY_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_all_history(history_dir: Path) -> Dict[str, Dict]:
    """Load all JSON history files."""
    history_data = {}
    
    for json_file in history_dir.glob('*.json'):
        # Parse filename: e.g., "12_CN.json"
        name = json_file.stem
        
        try:
            with open(json_file, 'r') as f:
                history_data[name] = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {json_file}: {e}")
            continue
    
    return history_data

def get_region_name(variant: str) -> str:
    """Map variant code to display name for the table."""
    names = {
        'GLO': 'Global',
        'EU': 'Europe',
        'IN': 'India',
        'CN': 'China',
        'NA': 'NA'
    }
    return names.get(variant, variant)

def generate_device_section(device_id: str, device_name: str, history_data: Dict) -> List[str]:
    """Generate a single table for one device across all regions."""
    lines = [f'### {device_name}', '']
    # Check if we have any data for this device
    active_regions = []
    # Determine available regions for this device
    preferred_regions = ['GLO', 'EU', 'IN', 'NA', 'CN']
    available_regions = set(DEVICE_METADATA.get(device_id, {}).get('models', {}).keys())
    
    # Also check if there are history files for regions not in config
    for key in history_data:
        if key.startswith(f"{device_id}_"):
            available_regions.add(key.replace(f"{device_id}_", ""))
            
    # Order: preferred first, then others sorted
    regions = [r for r in preferred_regions if r in available_regions]
    others = sorted([r for r in available_regions if r not in preferred_regions])
    regions.extend(others)
    
    for variant in regions:
        key = f'{device_id}_{variant}'
        if key in history_data:
            active_regions.append(variant)
            
    if not active_regions:
        return []

    lines.append('| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |')
    lines.append('|--------|-------|------------------|-----------|-------------|--------------|------|')
    
    for variant in regions:
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
            f"Major: **{current_entry['major']}**,&nbsp;Minor: **{current_entry['minor']}** | "
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
        '**Website:** [https://bartixxx32.github.io/OnePlus-antirollchecker/](https://bartixxx32.github.io/OnePlus-antirollchecker/)',
        '',
        '## 📊 Current Status',
        ''
    ]
    
    # improved: Iterate over DEVICE_ORDER from config
    for device_id in DEVICE_ORDER:
        if device_id not in DEVICE_METADATA:
            continue
        meta = DEVICE_METADATA[device_id]
        device_name = meta['name']
        device_lines = generate_device_section(device_id, device_name, history_data)
        if device_lines:
            lines.extend(device_lines)
            # Add separator if it's not the last one (simple heuristic: always add, strip last later if needed, 
            # but here we can't easily peek ahead. Adding --- after each section is fine as long as there is one.
            # actually logic below attempts to do it only between items.
            lines.append('---')
            lines.append('')
            
    # Remove trailing separator if it exists
    if lines[-1] == '' and lines[-2] == '---':
        lines.pop()
        lines.pop()
    
    # Add On-Demand Checker section
    lines.extend([
        '',
        '## 🤖 On-Demand ARB Checker',
        '',
        'Want to check a specific firmware instantly? Our automated bot can help!',
        '',
        '1. **[Click here to open a new Issue](https://github.com/Bartixxx32/OnePlus-antirollchecker/issues/new)**',
        '2. Set the title to `[CHECK] Your Title Here`',
        '3. Paste a direct link to the firmware `.zip` in the description',
        '4. Submit!',
        '',
        'The bot will automatically:',
        '- 📥 Download the firmware',
        '- 🔍 Extract metadata (Version, Model, Patch Level)',
        '- 🎯 Calculate the ARB index',
        '- 💬 Reply with a detailed report in 3-5 minutes',
        '',
    ])

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
        '## 🛠️ Credits',
        '- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by [syedinsaf](https://github.com/syedinsaf) - for fast and reliable OTA extraction.',
        '',
        '## 🤖 Workflow Status',
        '[![Check ARB](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml/badge.svg)](https://github.com/Bartixxx32/Oneplus-antirollchecker/actions/workflows/check_arb.yml)'
    ])
    
    return '\n'.join(lines) + '\n'

def main():
    parser = argparse.ArgumentParser(description="Generate README.md from history.")
    parser.add_argument("history_dir", nargs="?", default="data/history", help="Directory containing history JSON files")
    
    args = parser.parse_args()
    
    history_dir = Path(args.history_dir)
    
    if not history_dir.exists():
        logger.error(f"History directory not found: {history_dir}")
        sys.exit(1)
    
    history_data = load_all_history(history_dir)
    readme_content = generate_readme(history_data)
    
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("README.md generated successfully")
    except Exception as e:
        logger.error(f"Failed to write README.md: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
