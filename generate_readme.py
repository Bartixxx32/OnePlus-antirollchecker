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
        'NA': 'NA',
        'VISIBLE': 'Visible USA'
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
    
    # Determine region order based on device type
    if device_name.startswith("Oppo"):
        # Oppo devices use different regional codes
        preferred_order = ['EU', 'SG', 'TW', 'MY', 'ID', 'TH', 'VN', 'APC', 'OCA', 'EG', 'SA', 'MX', 'CN']
    else:
        # OnePlus devices use standard regions
        preferred_order = ['GLO', 'EU', 'IN', 'NA', 'VISIBLE', 'CN']
    
    def sort_key(v):
        try:
            return preferred_order.index(v)
        except ValueError:
            return len(preferred_order)
            
    sorted_variants = sorted(list(variants), key=sort_key)
    
    has_data = False
    rows = []
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
            has_data = True
            version = current_entry.get('version', 'Unknown')
            arb = current_entry.get('arb', -1)
            date = current_entry.get('last_checked', 'Unknown')
            major = current_entry.get('major', '?')
            minor = current_entry.get('minor', '?')
            region_name = get_region_name(variant)
            model = data.get('model', 'Unknown')
            
            # Status icon
            safe_icon = "✅" if arb == 0 else "❌" if arb > 0 else "❓"
                
            # MD5 formating
            md5 = current_entry.get('md5')
            md5_str = ""
            if md5:
                md5_str = f"<br><details><summary>MD5</summary><code>{md5}</code></details>"

            rows.append(f"| {region_name} | {model} | {version}{md5_str} | **{arb}** | Major: {major}, Minor: {minor} | {date} | {safe_icon} |")

    if has_data:
        lines.append(f"### {device_name}")
        lines.append("")
        lines.append("| Region | Model | Firmware Version | ARB Index | OEM Version | Last Checked | Safe |")
        lines.append("|:---|:---|:---|:---|:---|:---|:---|")
        lines.extend(rows)
        lines.append("")
        
        # Add History Section
        history_lines = []
        for variant in sorted_variants:
            key = f"{device_id}_{variant}"
            if key not in history_data:
                continue
            
            data = history_data[key]
            # Filter out 'current' version from history to avoid redundancy
            history_entries = [e for e in data.get('history', []) if e.get('status') != 'current']
            
            # Sort history by date descending
            history_entries.sort(key=lambda x: (x.get('last_checked', ''), x.get('version', '')), reverse=True)
            
            if history_entries: # Only show history if there's actual old versions
                region_name = get_region_name(variant)
                history_lines.append(f"<details>")
                history_lines.append(f"<summary>📜 <b>{region_name} History</b> (click to expand)</summary>")
                history_lines.append("")
                history_lines.append("| Firmware Version | ARB | OEM Version | Last Seen | Safe |")
                history_lines.append("|:---|:---|:---|:---|:---|")
                for entry in history_entries:
                    v = entry.get('version', 'Unknown')
                    a = entry.get('arb', -1)
                    maj = entry.get('major', '?')
                    min_ = entry.get('minor', '?')
                    ls = entry.get('last_checked', 'Unknown')
                    s_icon = "✅" if a == 0 else "❌" if a > 0 else "❓"
                    ls = entry.get('last_checked', 'Unknown')
                    s_icon = "✅" if a == 0 else "❌" if a > 0 else "❓"
                    
                    md5_hist = entry.get('md5')
                    md5_hist_str = ""
                    if md5_hist:
                        md5_hist_str = f"<br><details><summary>MD5</summary><code>{md5_hist}</code></details>"
                        
                    history_lines.append(f"| {v}{md5_hist_str} | {a} | Major: {maj}, Minor: {min_} | {ls} | {s_icon} |")
                history_lines.append("")
                history_lines.append("</details>")
                history_lines.append("")

        if history_lines:
            lines.extend(history_lines)
            lines.append("")
            
    return lines

def generate_readme(history_data: Dict) -> str:
    """Generate complete README content."""
    lines = [
        '# OnePlus Anti-Rollback (ARB) Checker',
        '',
        'Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.',
        '',
        '**🌐 Live Tracker:** [oneplusantiroll.netlify.app](https://oneplusantiroll.netlify.app/)',
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
        '1. Go to the [Issues Tab](https://github.com/Bartixxx32/OnePlus-antirollchecker/issues).',
        '2. Click **"New Issue"**.',
        '3. Set the **Title** to start with `[CHECK]` (e.g., `[CHECK] OnePlus 12 Update`).',
        '4. Paste the **Firmware Download URL** (direct link ending in `.zip`) in the description.',
        '5. Click **"Submit New Issue"**.',
        '',
        'The bot will automatically pick up the request, analyze the firmware, and post the results as a comment on your issue.',
        '',
        '---',
        ''
    ])

    lines.extend([
        '## 🔗 OOS Downloader API',
        '',
        'Need direct download URLs for OnePlus firmware? Use our **OOS Downloader API**!',
        '',
        '🌐 **API Endpoint**: [https://oosdownloader-gui.fly.dev/](https://oosdownloader-gui.fly.dev/)',
        '',
        'This API helps you get direct, signed download URLs for OnePlus OTA firmware files.',
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
