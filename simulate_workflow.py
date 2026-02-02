import os
import sys
import json
import shutil
import subprocess
from unittest.mock import MagicMock, patch
from pathlib import Path
from io import StringIO

# Ensure current directory is in sys.path
sys.path.append(os.getcwd())

import fetch_firmware
import analyze_firmware
import update_history
import generate_site
import generate_matrix

def main():
    print("--- Starting Workflow Simulation ---")

    # 1. Setup Environment
    print("[1] Setting up simulation environment...")
    base_dir = Path("simulation_output")
    if base_dir.exists():
        shutil.rmtree(base_dir)
    base_dir.mkdir()

    # Create tools directory and dummy tools
    tools_dir = base_dir / "tools"
    tools_dir.mkdir()

    # Dummy otaripper - using bash and ensuring args are handled
    otaripper = tools_dir / "otaripper"
    with open(otaripper, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("echo 'Simulating otaripper...'\n")
        f.write("OUT_DIR='.'\n")
        f.write("while [[ $# -gt 0 ]]; do\n")
        f.write("  case $1 in\n")
        f.write("    -o)\n")
        f.write("      OUT_DIR=\"$2\"\n")
        f.write("      shift\n")
        f.write("      shift\n")
        f.write("      ;;\n")
        f.write("    *)\n")
        f.write("      shift\n")
        f.write("      ;;\n")
        f.write("  esac\n")
        f.write("done\n")
        f.write("mkdir -p \"$OUT_DIR\"\n")
        f.write("touch \"$OUT_DIR/xbl_config.img\"\n")
    otaripper.chmod(0o755)

    # Dummy arbextract
    arbextract = tools_dir / "arbextract"
    with open(arbextract, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("echo 'ARB (Anti-Rollback): 2'\n")
        f.write("echo 'Major Version: 1'\n")
        f.write("echo 'Minor Version: 0'\n")
    arbextract.chmod(0o755)

    # Dummy firmware.zip
    fw_zip = base_dir / "firmware.zip"
    with open(fw_zip, "w") as f:
        f.write("dummy zip content")

    # 2. Simulate Matrix Generation
    print("[2] Generating Matrix (and picking a target)...")
    # We capture stdout to see what generate_matrix outputs
    with patch('sys.stdout', new=StringIO()) as fake_out:
        generate_matrix.generate_matrix()
        matrix_output = fake_out.getvalue()

    target_device = "15"
    target_variant = "GLO"
    target_device_short = "15"

    print(f"    Target selected: Device={target_device}, Variant={target_variant}")

    # 3. Simulate Fetch Firmware
    print("[3] Fetching Firmware (Mocked)...")

    mock_url = "http://example.com/firmware.zip"
    mock_version = "CPH2747_16.0.0.100(EX01)"

    # Patch requests in fetch_firmware module to return our mocked data
    with patch('fetch_firmware.requests.get') as mock_get:
        # We need to simulate the response structure expected by get_from_oos_api
        mock_resp_url = MagicMock()
        mock_resp_url.status_code = 200
        mock_resp_url.text = mock_url
        mock_resp_url.raise_for_status = MagicMock()

        mock_resp_ver = MagicMock()
        mock_resp_ver.status_code = 200
        mock_resp_ver.text = mock_version
        mock_resp_ver.raise_for_status = MagicMock()

        mock_get.side_effect = [mock_resp_url, mock_resp_ver]

        fetched_info = fetch_firmware.get_from_oos_api(target_device, target_variant)

        if fetched_info:
            print(f"    Fetched successfully: {fetched_info}")
        else:
            print("    Fetch failed!")
            sys.exit(1)

    # 4. Analyze Firmware (Using dummy tools)
    print("[4] Analyzing Firmware...")

    extract_dir = base_dir / "extracted"
    # Call the actual analysis function which calls our dummy tools
    analysis_result = analyze_firmware.analyze_firmware(
        fw_zip,
        tools_dir,
        extract_dir
    )

    print(f"    Analysis Result: {analysis_result}")

    expected_arb = '2'
    if analysis_result and analysis_result.get('arb_index') == expected_arb:
        print("    Analysis verification passed.")
    else:
        print(f"    Analysis failed or mismatch. Expected {expected_arb}")
        sys.exit(1)

    # 5. Update History
    print("[5] Updating History...")

    sim_history_dir = base_dir / "data" / "history"
    sim_history_dir.mkdir(parents=True, exist_ok=True)

    history_file = sim_history_dir / f"{target_device_short}_{target_variant}.json"

    # Load (will be empty)
    history_data = update_history.load_history(history_file)

    # Inject metadata manually as update_history.py main() does
    if not history_data.get('device'):
        history_data['device'] = "OnePlus 15" # Hardcoded for sim
        history_data['device_id'] = target_device_short
        history_data['region'] = target_variant
        history_data['model'] = "CPH2747"

    # Update entry
    is_new = update_history.update_history_entry(
        history_data,
        mock_version,
        int(analysis_result['arb_index']),
        int(analysis_result.get('major', 0)),
        int(analysis_result.get('minor', 0))
    )

    update_history.save_history(history_file, history_data)
    print(f"    History updated. New entry: {is_new}")

    # Verify file exists and has content
    if history_file.exists():
        with open(history_file, 'r') as f:
            saved_json = json.load(f)
            if saved_json['history'][0]['version'] == mock_version:
                 print("    History file verification passed.")
            else:
                 print("    History file verification failed (content mismatch).")
                 sys.exit(1)
    else:
        print("    History file creation failed.")
        sys.exit(1)

    # 6. Generate Site
    print("[6] Generating Site...")

    output_page_dir = base_dir / "page"
    template_dir = Path("templates") # Use real templates from repo

    # We call the generate function directly
    try:
        generate_site.generate(
            sim_history_dir,
            output_page_dir,
            template_dir
        )
    except Exception as e:
        print(f"    Site generation failed with exception: {e}")
        sys.exit(1)

    # Verify index.html exists
    index_html = output_page_dir / "index.html"
    if index_html.exists():
        print(f"    Site generated at {index_html}")
        # Check content roughly
        with open(index_html, 'r') as f:
            content = f.read()
            if mock_version in content:
                print("    Site content verification passed (version found).")
            else:
                print("    Site content verification warning: version string not found in HTML.")
    else:
        print("    Site generation failed (no index.html).")
        sys.exit(1)

    print("\n--- Simulation Complete: SUCCESS ---")
    print(f"All outputs located in: {base_dir}")

if __name__ == "__main__":
    main()
