import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import re

from config import DEVICE_METADATA, DEVICE_ORDER
from hardcode_rules import is_hardcode_protected

def get_region_name(region_code: str) -> str:
    """Helper to get a readable region name from its code."""
    regions = {
        'IN': 'India',
        'EU': 'Europe',
        'GLO': 'Global',
        'NA': 'North America',
        'CN': 'China',
        'ID': 'Indonesia',
        'MY': 'Malaysia',
        'OCA': 'Oceania',
        'SG': 'Singapore',
        'TH': 'Thailand',
        'TW': 'Taiwan',
        'VN': 'Vietnam',
        'EG': 'Egypt',
        'SA': 'Saudi Arabia',
        'PH': 'Philippines',
        'MEA': 'Middle East',
        'APC': 'Asia-Pacific',
        'MX': 'Mexico',
        'EEA': 'Europe (EEA)'
    }
    return regions.get(region_code, region_code)

def github_slug(text: str) -> str:
    """Generate a GitHub-compatible anchor slug for a header."""
    # Special cases for emojis/symbols based on GitHub's anchor generation
    if "♠️ Ace Series" in text:
        return "️-ace-series"
    if "💬 Community & Support" in text:
        return "-community--support"
    if "📟 Tablets" in text:
        return "-tablets"

    # Standard GitHub slugification
    slug = text.lower().replace(' ', '-')
    slug = re.sub(r'[^\w-]', '', slug)
    return slug

def load_history(filepath: Path) -> Dict:
    """Load history data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def version_sort_key(version: str) -> List[Any]:
    """Create a sort key for firmware versions to handle numeric parts correctly."""
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', version)]

def generate_device_section(device_id: str, device_name: str, history_data: Dict) -> List[str]:
    """Generate Markdown for a single device section."""
    lines = []
    rows = []
    
    # Map device ID to the one used in hardcode_rules
    device_id_mapped = device_id.lower().replace(" ", "_")
    if device_id_mapped == "12r": device_id_mapped = "oneplus_12r"
    elif device_id_mapped == "11r": device_id_mapped = "oneplus_11r"
    elif "nord_ce_4_lite" in device_id_mapped: device_id_mapped = "oneplus_nord_ce_4_lite"

    # Pre-sort variants based on priority (GLO > EU > IN > NA > CN)
    priority = {'GLO': 0, 'EU': 1, 'IN': 2, 'NA': 3, 'CN': 4}
    models_dict = DEVICE_METADATA[device_id].get('models', {})
    sorted_variants = sorted(models_dict.keys(),
                             key=lambda x: priority.get(x, 99))

    has_data = False
    for variant in sorted_variants:
        key = f"{device_id}_{variant}"
        if key in history_data:
            data = history_data[key]
            current_entry = None
            
            # Find the 'current' entry
            for entry in data.get('history', []):
                if entry.get('status') == 'current':
                    current_entry = entry
                    break
            
            if not current_entry:
                continue

            has_data = True
            region_name = get_region_name(variant)

            # Model detection with fallback
            model = current_entry.get('model')
            if not model or model == "Unknown":
                model = DEVICE_METADATA[device_id]['models'].get(variant, 'Unknown')

            version = current_entry.get('version', 'Unknown')
            arb = current_entry.get('arb', -1)
            
            # Check hardcoded rules
            is_hardcoded = is_hardcode_protected(device_id_mapped, version)

            # For hardcoded entries, show ? for ARB value
            display_arb = '?' if is_hardcoded else (arb if arb is not None and arb >= 0 else '?')

            major = current_entry.get('major', '?')
            minor = current_entry.get('minor', '?')
            date = current_entry.get('last_checked', 'Unknown')
            
            if is_hardcoded:
                safe_icon = "⚠️ Undetectable protected"
            elif arb == 0:
                safe_icon = "✅ Safe"
            elif isinstance(arb, int) and arb > 0:
                safe_icon = "❌ Protected"
            else:
                safe_icon = "❓ Unknown"

            # MD5 formating
            md5 = current_entry.get('md5')
            md5_str = ""
            if md5:
                md5_str = f"<br><details><summary>MD5</summary><code>{md5}</code></details>"

            rows.append(f"| {region_name} | {model} | {version}{md5_str} | **{display_arb}** | Major: {major}, Minor: {minor} | {date} | {safe_icon} |")

    if has_data:
        lines.append(f"#### {device_name}")
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
            history_entries = [e for e in data.get('history', []) if e.get('status') != 'current']
            history_entries.sort(key=lambda x: version_sort_key(x.get('version', '')), reverse=True)
            
            if history_entries:
                region_name = get_region_name(variant)
                history_lines.append(f"<details>")
                history_lines.append(f"<summary>📜 <b>{region_name} History</b> (click to expand)</summary>")
                history_lines.append("")
                history_lines.append("| Firmware Version | ARB | OEM Version | Last Seen | Safe |")
                history_lines.append("|:---|:---|:---|:---|:---|")
                for entry in history_entries:
                    v = entry.get('version', 'Unknown')
                    a = entry.get('arb', -1)
                    hist_is_hardcoded = is_hardcode_protected(device_id_mapped, v)
                    display_a = '?' if hist_is_hardcoded else (a if a is not None and a >= 0 else '?')
                    maj = entry.get('major', '?')
                    min_ = entry.get('minor', '?')
                    ls = entry.get('last_checked', 'Unknown')
                    
                    if hist_is_hardcoded:
                        s_icon = "⚠️ Undetectable protected"
                    elif a == 0:
                        s_icon = "✅ Safe"
                    elif isinstance(a, int) and a > 0:
                        s_icon = "❌ Protected"
                    else:
                        s_icon = "❓ Unknown"
                    
                    md5_hist = entry.get('md5')
                    md5_hist_str = ""
                    if md5_hist:
                        md5_hist_str = f"<br><details><summary>MD5</summary><code>{md5_hist}</code></details>"
                    history_lines.append(f"| {v}{md5_hist_str} | {display_a} | Major: {maj}, Minor: {min_} | {ls} | {s_icon} |")
                history_lines.append("")
                history_lines.append("</details>")
                history_lines.append("")

        if history_lines:
            lines.extend(history_lines)
            lines.append("")
            
    return lines

def generate_readme(history_data: Dict) -> str:
    """Generate complete README content with improved UI."""

    # Define logical groups
    GROUPS = {
        "📱 Numbered Series": ["15", "15R", "13", "13R", "13T", "13s", "12", "12R", "11", "11R", "10 Pro", "10T", "9 Pro", "9", "9RT", "9R", "8T", "8 Pro", "8", "7T Pro", "7T", "7 Pro", "7"],
        "📖 Foldables": ["Open"],
        "⚡ Nord Series": ["Nord 5", "Nord 4", "Nord CE 4 Lite", "Nord CE 4", "Nord CE 3", "Nord CE 3 Lite", "Nord CE 2 Lite", "Nord N30", "Nord N20", "Nord 1", "Nord N200 5G"],
        "♠️ Ace Series": ["Ace 6T", "Ace 6", "Ace 5 Pro", "Ace 5", "Ace 3 Pro", "Ace 3V", "Ace 3"],
        "📟 Tablets": ["Pad 3", "Pad 2 Pro", "Pad 2"],
        "🌐 Oppo Series": ["Find N5", "Find N3", "Reno10 Pro", "Find X8 Ultra", "Find X5 Pro", "Find X5", "Find X3 Pro"]
    }

    # Header section
    lines = [
        '<div align="center">',
        '  <h1>OnePlus Anti-Rollback (ARB) Checker</h1>',
        '  <p><b>Automated tracker for firmware updates and ARB indices across the OnePlus ecosystem.</b></p>',
        '',
        '  <!-- Badges -->',
        '  <p>',
        '    <img src="https://img.shields.io/github/actions/workflow/status/Bartixxx32/OnePlus-antirollchecker/check_arb.yml?style=for-the-badge&logo=github&label=Monitoring" alt="Workflow Status">',
        '    <img src="https://img.shields.io/github/stars/Bartixxx32/OnePlus-antirollchecker?style=for-the-badge&color=yellow" alt="Stars">',
        '    <img src="https://img.shields.io/github/last-commit/Bartixxx32/OnePlus-antirollchecker?style=for-the-badge" alt="Last Commit">',
        '    <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python">',
        '    <img src="https://visitor-badge.laobi.icu/badge?page_id=Bartixxx32.OnePlus-antirollchecker" alt="Views">',
        '  </p>',
        '</div>',
        '',
        '---',
        '',
        '## 📑 Table of Contents',
        f'- [🤖 Telegram Bot](#{github_slug("🤖 OnePlus ARB Checker Bot")})',
        f'- [📊 Current Status](#{github_slug("📊 Current Status")})',
    ]

    # Add groups to TOC
    for group_name in GROUPS.keys():
        lines.append(f"  - [{group_name}](#{github_slug(group_name)})")

    lines.extend([
        f'- [🤖 On-Demand Checker](#{github_slug("🤖 On-Demand ARB Checker")})',
        f'- [🌐 OOS Downloader API](#{github_slug("🌐 OOS Downloader API")})',
        f'- [📱 Android App](#{github_slug("📱 Android App")})',
        f'- [💬 Community](#{github_slug("💬 Community & Support")})',
        f'- [🙏 Credits](#credits)',
        '',
        '---',
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
        '> [!IMPORTANT]',
        '> The bot **only** works within the [@oneplusarbchecker](https://t.me/oneplusarbchecker) group. DM checks are disabled. Checks are powered by GitHub Actions and may take a minute to process.',
        '',
        '### 🍻 Support the Project',
        'If you find this tool helpful, consider buying me a beer! Your support keeps the updates coming.',
        '',
        '[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=bartixxx32&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/bartixxx32)',
        '',
        '---',
        '',
        '## 📊 Current Status',
        '',
        'Find the latest Anti-Rollback (ARB) status for your device below, organized by series. **Check the legend for status meanings.**',
        '',
        '### 🛡️ Legend',
        '- ✅ **Safe**: ARB index is 0. Standard flashing is safe.',
        '- ❌ **Protected**: ARB index > 0. Downgrading will brick your device.',
        '- ⚠️ **Undetectable**: Uses newer protection where ARB cannot be read normally, but it is **known to be protected**.',
        '- ❓ **Unknown**: Status could not be verified.',
        '',
        '---',
        ''
    ])

    # Generate grouped device sections
    processed_devices = set()
    for group_name, device_ids in GROUPS.items():
        group_lines = []
        for device_id in device_ids:
            if device_id in DEVICE_METADATA:
                processed_devices.add(device_id)
                device_name = DEVICE_METADATA[device_id]['name']
                device_lines = generate_device_section(device_id, device_name, history_data)
                if device_lines:
                    group_lines.extend(device_lines)
                    group_lines.append('---')
                    group_lines.append('')
        
        if group_lines:
            lines.append(f"### {group_name}")
            lines.append("")
            lines.extend(group_lines)

    # Handle any devices in DEVICE_ORDER that weren't in a group
    other_devices = [d for d in DEVICE_ORDER if d not in processed_devices]
    if other_devices:
        other_lines = []
        for device_id in other_devices:
            if device_id in DEVICE_METADATA:
                device_name = DEVICE_METADATA[device_id]['name']
                device_lines = generate_device_section(device_id, device_name, history_data)
                if device_lines:
                    other_lines.extend(device_lines)
                    other_lines.append('---')
                    other_lines.append('')

        if other_lines:
            lines.append(f"### 📁 Other Devices")
            lines.append("")
            lines.extend(other_lines)
            
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
        '## 🌐 OOS Downloader API',
        '',
        'Need direct download URLs for OnePlus firmware? Use our **OOS Downloader API**!',
        '',
        '🌐 **API Endpoint**: [https://oosdownloader-gui.fly.dev/](https://oosdownloader-gui.fly.dev/)',
        '',
        'Our OOS Downloader API provides direct, signed download URLs for OnePlus OTA firmware files by leveraging the [Oxygen Updater API](https://play.google.com/store/apps/details?id=com.arjanvlek.oxygenupdater).',
        '',
        '---',
        '',
        '## Credits',
        '',
        '- **Payload Extraction**: [otaripper](https://github.com/syedinsaf/otaripper) by syedinsaf',
        '- **Playback & Validation**: [payload-dumper-go](https://github.com/ssut/payload-dumper-go) by ssut',
        '- **ARB Extraction**: [arbextract](https://github.com/koaaN/arbextract) by koaaN',
        '- **API for CN variants**: [roms.danielspringer.at](https://roms.danielspringer.at/) by Daniel Springer',
        '- **Firmware API source**: [Oxygen Updater](https://play.google.com/store/apps/details?id=com.arjanvlek.oxygenupdater)',
        '',
        '---',
        '',
        '## 📱 Android App',
        '',
        'Prefer a native mobile experience? We have an official Android app on F-Droid! Check firmware statuses, view ARB indices, and stay protected directly from your phone.',
        '',
        '[<img src="https://f-droid.org/badge/get-it-on.png" alt="Get it on F-Droid" height="80">](https://f-droid.org/packages/com.bartixxx.oneplusarbchecker/)',
        '',
        '## 💬 Community & Support',
        '',
        '- **Telegram Group:** [@oneplusarbchecker](https://t.me/oneplusarbchecker)',
        '',
        '> [!IMPORTANT]',
        '> The bot **only** works within this group to prevent spam and ensure availability. DM checks are disabled.',
        '',
        '---',
        f'<div align="center"><i>Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</i></div>'
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
