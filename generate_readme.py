import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional
from config import DEVICE_ORDER, DEVICE_METADATA

def load_history(file_path: Path) -> Dict:
    """Load history from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_region_name(region_code: str) -> str:
    """Convert region code to human readable name."""
    names = {
        'GLO': 'Global',
        'EU': 'Europe',
        'IN': 'India',
        'CN': 'China',
        'NA': 'North America'
    }
    return names.get(region_code, region_code)

def generate_device_section(device_id: str, device_name: str, history_data: Dict) -> List[str]:
    """Generate Markdown section for a specific device."""
    lines = []
    
    # Get available variants
    variants = set()
    if device_id in DEVICE_METADATA:
        variants.update(DEVICE_METADATA[device_id]['models'].keys())
    for key in history_data:
        if key.startswith(f"{device_id}_"):
             variants.add(key.replace(f"{device_id}_", ""))
    
    preferred_order = ['GLO', 'EU', 'IN', 'NA', 'CN']
    def sort_key(v):
        try:
            return preferred_order.index(v)
        except ValueError:
            return len(preferred_order)
            
    sorted_variants = sorted(list(variants), key=sort_key)
    
    variant_rows = []
    for variant in sorted_variants:
        key = f"{device_id}_{variant}"
        if key not in history_data:
            continue
            
        data = history_data[key]
        current_entry = None
        for entry in data.get('history', []):
            if entry.get('status') == 'current':
                current_entry = entry
                break
        
        if not current_entry and data.get('history'):
            current_entry = data['history'][0]
            
        if current_entry:
            version = current_entry.get('version', 'Unknown')
            arb = current_entry.get('arb', -1)
            date = current_entry.get('last_checked', 'Unknown')
            region_name = get_region_name(variant)
            model = data.get('model', 'Unknown')
            status = "✅ Safe" if arb == 0 else "⛔ Protected" if arb > 0 else "❓ Unknown"
            
            variant_rows.append('    <tr>')
            variant_rows.append(f'      <td><b>{region_name}</b></td>')
            variant_rows.append(f'      <td><code>{model}</code></td>')
            variant_rows.append(f'      <td><code>{version}</code></td>')
            variant_rows.append(f'      <td align="center">{arb}</td>')
            variant_rows.append(f'      <td align="center">{status}</td>')
            variant_rows.append(f'      <td align="right">{date}</td>')
            variant_rows.append('    </tr>')

    if variant_rows:
        lines.append(f"### {device_name}")
        lines.append("")
        # Use HTML table with specific widths for alignment across sections
        lines.append('<table width="100%">')
        lines.append('  <thead>')
        lines.append('    <tr>')
        lines.append('      <th align="left" width="15%">Region</th>')
        lines.append('      <th align="left" width="12%">Model</th>')
        lines.append('      <th align="left" width="38%">Version</th>')
        lines.append('      <th align="center" width="5%">ARB</th>')
        lines.append('      <th align="center" width="15%">Status</th>')
        lines.append('      <th align="right" width="15%">Last Checked</th>')
        lines.append('    </tr>')
        lines.append('  </thead>')
        lines.append('  <tbody>')
        lines.extend(variant_rows)
        lines.append('  </tbody>')
        lines.append('</table>')
        lines.append("")
        
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

    for device_id in DEVICE_ORDER:
        if device_id not in DEVICE_METADATA:
            continue
        meta = DEVICE_METADATA[device_id]
        device_name = meta['name']
        
        device_lines = generate_device_section(device_id, device_name, history_data)
        if device_lines:
            lines.extend(device_lines)
            lines.append('---')
            lines.append('')
            
    lines.extend([
        '## 🤖 On-Demand ARB Checker',
        '',
        'You can check the ARB index of any OnePlus Ozip/Zip URL manually using our automated workflow.',
        '',
        '### How to use:',
        '1. Go to the [Actions Tab](https://github.com/Bartixxx32/OnePlus-antirollchecker/actions).',
        '2. Select **"Manual ARB Check"** from the sidebar.',
        '3. Click **"Run workflow"**.',
        '4. Paste the **Firmware Download URL** (direct link preferred, e.g., from Oxygen Updater).',
        '5. Click **Run workflow**.',
        '',
        'The bot will extract the payload, check the ARB index, and post the result as a comment on the workflow run summary (or you can view the logs).',
        '',
        '---',
        ''
    ])

    lines.extend([
        '## Credits',
        '',
        '- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by syedinsaf',
        '- **Fallback Extraction**: [payload-dumper-go](https://github.com/ssut/payload-dumper-go) by ssut',
        '- **ARB Extraction**: [arbextract](https://github.com/koaaN/arbextract) by koaaN',
        '',
        '---',
        f'*Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}*'
    ])
    
    return "\n".join(lines)

if __name__ == "__main__":
    history_dir = Path("data/history")
    if not history_dir.exists():
        exit(0)
    all_history = {}
    for f in history_dir.glob("*.json"):
        all_history[f.stem] = load_history(f)
    content = generate_readme(all_history)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md generated successfully")
