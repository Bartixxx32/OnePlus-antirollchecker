#!/usr/bin/env python3
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from config import DEVICE_METADATA

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_all_history(history_dir: Path):
    """Load all JSON history files."""
    history_data = {}
    if not history_dir.exists():
        return {}

    for json_file in history_dir.glob('*.json'):
        name = json_file.stem
        try:
            with open(json_file, 'r') as f:
                history_data[name] = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {json_file}: {e}")
            continue
    return history_data

def get_region_name(variant: str) -> str:
    names = {
        'GLO': 'Global',
        'EU': 'Europe',
        'IN': 'India',
        'CN': 'China'
    }
    return names.get(variant, variant)

def process_data(history_data):
    """Process raw history data into a structure suitable for the template."""
    devices_list = []

    # Iterate over devices in the order defined in config
    for device_id, meta in DEVICE_METADATA.items():
        device_entry = {
            'name': meta['name'],
            'variants': []
        }

        # Standard regions order
        regions = ['GLO', 'EU', 'IN', 'CN']

        for variant in regions:
            key = f'{device_id}_{variant}'
            if key not in history_data:
                continue

            data = history_data[key]

            # Find current entry
            current_entry = None
            for entry in data.get('history', []):
                if entry.get('status') == 'current':
                    current_entry = entry
                    break

            # Fallback
            if not current_entry and data.get('history'):
                current_entry = data['history'][0]

            if not current_entry:
                continue

            # Shorten last_checked to date only if possible
            last_checked = current_entry.get('last_checked', 'Unknown')
            if ' ' in last_checked:
                last_checked = last_checked.split(' ')[0]

            variant_entry = {
                'region_name': get_region_name(variant),
                'model': data.get('model', 'Unknown'),
                'version': current_entry.get('version', 'Unknown'),
                'arb': current_entry.get('arb', -1),
                'major': current_entry.get('major', '?'),
                'minor': current_entry.get('minor', '?'),
                'last_checked': last_checked
            }
            # Add helper for status
            # ARB 0 means safe (downgrade possible), >0 means protected
            variant_entry['is_safe'] = (variant_entry['arb'] == 0)

            variant_entry['short_version'] = variant_entry['version']

            device_entry['variants'].append(variant_entry)

        if device_entry['variants']:
             devices_list.append(device_entry)

    return devices_list

def generate(history_dir: Path, output_dir: Path, template_dir: Path):
    """Core logic to generate the site."""
    if not history_dir.exists():
        logger.warning(f"History directory not found: {history_dir}. Generating empty site.")
        history_data = {}
    else:
        history_data = load_all_history(history_dir)

    devices = process_data(history_data)

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    try:
        template = env.get_template('index.html')
    except Exception as e:
        logger.error(f"Failed to load template: {e}")
        return

    # Render
    output_html = template.render(
        devices=devices,
        generated_at=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    )

    # Write output
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(output_html)
        logger.info(f"Site generated successfully at {output_dir}/index.html")
    except Exception as e:
        logger.error(f"Failed to write output: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate static site from history.")
    parser.add_argument("--history-dir", default="data/history", help="Directory containing history JSON files")
    parser.add_argument("--output-dir", default="page", help="Output directory for the website")
    parser.add_argument("--template-dir", default="templates", help="Directory containing templates")

    args = parser.parse_args()

    generate(
        Path(args.history_dir),
        Path(args.output_dir),
        Path(args.template_dir)
    )

if __name__ == '__main__':
    main()
