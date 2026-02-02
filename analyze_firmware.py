#!/usr/bin/env python3
"""
Analyze firmware zip to extract ARB index.
Wraps payload-dumper-go and arbextract usage.
"""

import shlex
import sys
import json
import argparse
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, cwd=None):
    # Log valid shell-escaped command for reproducibility/safety
    safe_cmd_str = ' '.join(shlex.quote(str(arg)) for arg in cmd)
    logger.info(f"Running: {safe_cmd_str}")
    
    # shell=False is default but explicit is better for audit
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=False)
    if result.returncode != 0:
        logger.error(f"Command failed ({result.returncode}): {result.stderr}")
        return None
    return result.stdout

def analyze_firmware(zip_path, tools_dir, output_dir):
    zip_path = Path(zip_path).resolve()
    tools_dir = Path(tools_dir).resolve()
    output_dir = Path(output_dir).resolve()
    
    otaripper = tools_dir / "otaripper"
    arbextract = tools_dir / "arbextract"
    
    # 1. Extract xbl_config
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        
    # otaripper <zip> -p <partitions> -o <output>
    # Add -n to prevent opening folder
    cmd_extract = [str(otaripper), str(zip_path), "-p", "xbl_config", "-o", str(output_dir), "-n"]
    if not run_command(cmd_extract):
        return None
        
    # 2. Find extracted image
    # pattern: matches anything with xbl_config inside extracted folder
    # Use rglob to search recursively because otaripper creates a subdirectory
    img_files = list(output_dir.rglob("*xbl_config*.img"))
    if not img_files:
        logger.error("xbl_config image not found in extraction output")
        return None
    
    img_file = img_files[0]
    
    # 3. Run arbextract
    cmd_arb = [str(arbextract), str(img_file)]
    output = run_command(cmd_arb)
    if not output:
        return None
        
    # 4. Parse Output
    # Expected output format from arbextract:
    # ARB (Anti-Rollback): 1
    # Major Version: 3
    # Minor Version: 0
    
    result = {}
    for line in output.splitlines():
        if "ARB (Anti-Rollback)" in line:
            result['arb_index'] = line.split(':')[-1].strip()
        elif "Major Version" in line:
            result['major'] = line.split(':')[-1].strip()
        elif "Minor Version" in line:
            result['minor'] = line.split(':')[-1].strip()
            
    if 'arb_index' not in result:
        logger.error("Could not parse ARB index from arbextract output")
        return None
        
    return result

def main():
    parser = argparse.ArgumentParser(description="Analyze firmware ARB index.")
    parser.add_argument("zip_path", help="Path to firmware.zip")
    parser.add_argument("--tools-dir", default="tools", help="Directory containing payload-dumper and arbextract")
    parser.add_argument("--output-dir", default="extracted", help="Directory for extraction")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    result = analyze_firmware(args.zip_path, args.tools_dir, args.output_dir)
    
    if result:
        if args.json:
            print(json.dumps(result))
        else:
            print(f"ARB Index: {result['arb_index']}")
            print(f"Major: {result.get('major', '0')}")
            print(f"Minor: {result.get('minor', '0')}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
