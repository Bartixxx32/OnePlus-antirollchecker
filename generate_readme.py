import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional
from config import DEVICE_ORDER, DEVICE_METADATA, REGION_MAPPING
import re
from hardcode_rules import is_hardcode_protected, version_sort_key

def load_history(file_path: Path) -> Dict:
    """Load history from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_region_name(variant: str) -> str:
    """Map compact region codes to human-readable labels."""
    return REGION_MAPPING.get(variant, variant)

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
            
            is_hardcoded = is_hardcode_protected(device_id, version)
                
            date = current_entry.get('last_checked', 'Unknown')
            major = current_entry.get('major', '?')
            minor = current_entry.get('minor', '?')
            region_name = get_region_name(variant)
            model = data.get('model', 'Unknown')
            
            # Status icon
            if is_hardcoded:
                safe_icon = "⚠️"
            elif arb == 0:
                safe_icon = "✅"
            elif isinstance(arb, int) and arb > 0:
                safe_icon = "❌"
            else:
                safe_icon = "❓"
                
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
            
            # Sort history by firmware version descending (parse numeric parts for correct ordering)
            history_entries.sort(key=lambda x: version_sort_key(x.get('version', '')), reverse=True)
            
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
                    
                    hist_is_hardcoded = is_hardcode_protected(device_id, v)
                        
                    maj = entry.get('major', '?')
                    min_ = entry.get('minor', '?')
                    ls = entry.get('last_checked', 'Unknown')
                    
                    if hist_is_hardcoded:
                        s_icon = "⚠️"
                    elif a == 0:
                        s_icon = "✅"
                    elif isinstance(a, int) and a > 0:
                        s_icon = "❌"
                    else:
                        s_icon = "❓"
                    
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
        '<!-- Badges -->',
        '![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Bartixxx32/OnePlus-antirollchecker/check_arb.yml?style=flat-square&logo=github&label=ARB%20Checking)',
        '![GitHub stars](https://img.shields.io/github/stars/Bartixxx32/OnePlus-antirollchecker?style=flat-square&color=yellow)',
        '![GitHub forks](https://img.shields.io/github/forks/Bartixxx32/OnePlus-antirollchecker?style=flat-square)',
        '![GitHub last commit](https://img.shields.io/github/last-commit/Bartixxx32/OnePlus-antirollchecker?style=flat-square)',
        '![Python Version](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)',
        '![Views](https://visitor-badge.laobi.icu/badge?page_id=Bartixxx32.OnePlus-antirollchecker)',
        '---',
        '',
        'Automated ARB (Anti-Rollback) index tracker for OnePlus devices. This repository monitors firmware updates and tracks ARB changes over time.',
        '',
        '**🌐 ARB Info Website:** [https://oparb.pages.dev/](https://oparb.pages.dev/)',
        '',
        '## 🤖 OnePlus ARB Checker Bot',
        '',
        'Our Telegram bot allows you to check the Anti-Rollback (ARB) index of any OnePlus firmware instantly.',
        '',
        '- **Bot Username:** [@oparbcheckerbot](https://t.me/oparbcheckerbot)',
        '- **Group:** [@oneplusarbchecker](https://t.me/oneplusarbchecker)',
        '- **Supported Commands:**',
        '  - `/check <url>` - Analyze a firmware file (Direct Download Link required)',
        '  - `/download <device> [region]` - Fetch latest firmware & auto-check ARB',
        '  - `/devicestatus <device>` - Show current firmware & ARB info',
        '  - `/latest` - Show the 5 most recently discovered firmwares',
        '  - `/help` - Show usage instructions',
        '  - `/about` - Bot version and stats',
        '',
        '> **Note:** The bot **only** works within the [@oneplusarbchecker](https://t.me/oneplusarbchecker) group. DM checks are disabled. Checks are powered by GitHub Actions and may take a minute to process.',
        '',
        '### 🍻 Support the Project',
        'If you find this tool helpful, consider buying me a beer! Your support keeps the updates coming.',
        '',
        '[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=bartixxx32&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/bartixxx32)',
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
        '',
    ])

    lines.extend([
        '## 🌐 OOS Downloader API',
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
        '- **Playback & Validation**: [payload-dumper-go](https://github.com/ssut/payload-dumper-go) by ssut',
        '- **ARB Extraction**: [arbextract](https://github.com/koaaN/arbextract) by koaaN',
        '- **API for CN variants**: [roms.danielspringer.at](https://roms.danielspringer.at/) by Daniel Springer',
        '',
        '---',
        '',
    ])

    lines.extend([
        '## 📱 Android App',
        '',
        'Prefer a native mobile experience? We have an official Android app on F-Droid! Check firmware statuses, view ARB indices, and stay protected directly from your phone.',
        '',
        '[<img src="https://f-droid.org/badge/get-it-on.png"',
        '    alt="Get it on F-Droid"',
        '    height="80">](https://f-droid.org/packages/com.bartixxx.oneplusarbchecker/)',
        '',
        '## 💬 Community & Support',
        '',
        '- **Telegram Group:** [@oneplusarbchecker](https://t.me/oneplusarbchecker)',
        '',
        '> **Important:** The bot **only** works within this group to prevent spam and ensure availability. DM checks are disabled.',
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
