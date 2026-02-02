#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path
from config import DEVICE_METADATA

def create_dummy_history(history_dir: Path):
    if history_dir.exists():
        shutil.rmtree(history_dir)
    history_dir.mkdir(parents=True)

    print(f"Creating dummy history in {history_dir}...")

    regions = ['GLO', 'EU', 'IN', 'CN']

    for device_id, meta in DEVICE_METADATA.items():
        for region in regions:
            # Skip some random combinations to test robustness
            if device_id == '15R' and region == 'CN':
                continue

            filename = f"{device_id}_{region}.json"
            model = meta['models'].get(region, 'UnknownModel')

            # Create dummy data
            # Mix of safe and protected
            # deterministic pseudo-random
            is_safe = ((len(device_id) + len(region)) % 2 == 0)
            arb_val = 0 if is_safe else 1

            data = {
                "device_id": device_id,
                "region": region,
                "model": model,
                "history": [
                    {
                        "status": "current",
                        "version": f"Dummy_{model}_16.0.0.100({region}01)",
                        "arb": arb_val,
                        "major": 3,
                        "minor": 0,
                        "last_checked": "2026-01-01 12:00:00"
                    }
                ]
            }

            with open(history_dir / filename, 'w') as f:
                json.dump(data, f, indent=2)

def main():
    history_dir = Path("temp_history")
    output_dir = Path("page_preview")

    try:
        # 1. Create Data
        create_dummy_history(history_dir)

        # 2. Run Generator
        print(f"Running generate_site.py -> {output_dir}...")
        cmd = [
            sys.executable, "generate_site.py",
            "--history-dir", str(history_dir),
            "--output-dir", str(output_dir)
        ]
        subprocess.check_call(cmd)

        # 3. Verify
        index_file = output_dir / "index.html"
        if not index_file.exists():
            print("Error: index.html not found!")
            sys.exit(1)

        content = index_file.read_text(encoding='utf-8')

        # Check for some expected strings
        if "OnePlus ARB Checker" not in content:
            print("Error: Title not found in HTML")
            sys.exit(1)

        if "Dummy_" not in content:
            print("Error: Dummy data not found in HTML")
            sys.exit(1)

        print("Verification successful!")
        print(f"Preview generated at: {index_file}")
        print("You can open this file in your browser to inspect the design.")

    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    finally:
        # Cleanup history but keep the page for viewing
        if history_dir.exists():
            shutil.rmtree(history_dir)

if __name__ == '__main__':
    main()
