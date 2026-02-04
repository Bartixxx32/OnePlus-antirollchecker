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

import shutil
import zipfile

def extract_ota_metadata(zip_path):
    """Peek into the zip to find META-INF/com/android/metadata"""
    metadata = {}
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            # 1. Try META-INF/com/android/metadata
            meta_path = 'META-INF/com/android/metadata'
            if meta_path in z.namelist():
                content = z.read(meta_path).decode('utf-8')
                for line in content.splitlines():
                    if '=' in line:
                        k, v = line.split('=', 1)
                        metadata[k.strip()] = v.strip()
            
            # 2. Try payload_properties.txt (shorter info)
            prop_path = 'payload_properties.txt'
            if prop_path in z.namelist():
                content = z.read(prop_path).decode('utf-8')
                for line in content.splitlines():
                    if '=' in line or ':' in line:
                        delim = '=' if '=' in line else ':'
                        k, v = line.split(delim, 1)
                        # Avoid overwriting metadata if already found
                        if k.strip() not in metadata:
                            metadata[k.strip()] = v.strip()
    except Exception as e:
        logger.warning(f"Failed to extract metadata from zip: {e}")
    return metadata

def analyze_firmware(zip_path, tools_dir, output_dir, final_dir=None):
    zip_path = Path(zip_path).resolve()
    tools_dir = Path(tools_dir).resolve()
    output_dir = Path(output_dir).resolve()
    final_dir = Path(final_dir).resolve() if final_dir else Path("firmware_data").resolve()
    
    otaripper = tools_dir / "otaripper"
    arbextract = tools_dir / "arbextract"
    
    final_img = final_dir / "xbl_config.img"
    
    # 0. Extract basic metadata (always try if zip is available)
    metadata = {}
    if zip_path and Path(zip_path).exists():
        metadata = extract_ota_metadata(zip_path)
    elif zip_path:
        logger.warning(f"Zip path provided but does not exist: {zip_path}")
    
    # 1. Skip extraction if image already exists (cache hit optimization)
    if final_img.exists():
        logger.info(f"Image already exists at {final_img}, skipping extraction.")
    else:
        if not zip_path or not Path(zip_path).exists():
            logger.error("Missing firmware.zip and no cached image found.")
            return None
        
        zip_path = Path(zip_path).resolve()

        # 2. Clean/Create directories for extraction
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)
        
        if not final_dir.exists():
            final_dir.mkdir(parents=True)
            
        # otaripper <zip> -p <partitions> -o <output>
        cmd_extract = [str(otaripper), str(zip_path), "-p", "xbl_config", "-o", str(output_dir), "-n"]
        logger.info("Attempting extraction with otaripper...")
        
        if not run_command(cmd_extract):
            logger.warning("otaripper failed, attempting fallback with payload-dumper-go...")
            
            # Fallback to payload-dumper-go
            # payload-dumper-go -p <partitions> -o <output> <zip>
            pdg = tools_dir / "payload-dumper-go"
            cmd_fallback = [str(pdg), "-p", "xbl_config", "-o", str(output_dir), str(zip_path)]
            
            if not run_command(cmd_fallback):
                logger.error("Both otaripper and payload-dumper-go failed to extract firmware.")
                return None
            
        # 3. Find extracted image recursively
        img_files = list(output_dir.rglob("*xbl_config*.img"))
        if not img_files:
            logger.error("xbl_config image not found in extraction output")
            return None
        
        # Move and rename
        src_img = img_files[0]
        logger.info(f"Found image: {src_img}")
        logger.info(f"Moving to: {final_img}")
        shutil.move(src_img, final_img)
        
        # Cleanup temp extraction
        shutil.rmtree(output_dir)
    
    # 3. Run arbextract on the FINAL file
    cmd_arb = [str(arbextract), str(final_img)]
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
        
    # Append metadata
    if metadata:
        result['ota_metadata'] = metadata

    return result

def main():
    parser = argparse.ArgumentParser(description="Analyze firmware ARB index.")
    parser.add_argument("zip_path", nargs="?", help="Path to firmware.zip (optional if image already exists in final-dir)")
    parser.add_argument("--tools-dir", default="tools", help="Directory containing payload-dumper and arbextract")
    parser.add_argument("--output-dir", default="extracted", help="Directory for extraction")
    parser.add_argument("--final-dir", default="firmware_data", help="Directory for final xbl_config.img")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    result = analyze_firmware(args.zip_path, args.tools_dir, args.output_dir, args.final_dir)
    
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
