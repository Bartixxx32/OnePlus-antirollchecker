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
import hashlib
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

def calculate_md5(file_path):
    """Calculate MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

import shutil
import zipfile

def detect_file_type(path: Path) -> str:
    """Detect file type by magic bytes, returns '.7z', '.zip', '.img' or ''."""
    try:
        with open(path, 'rb') as f:
            header = f.read(8)
        if header[:2] == b'PK':
            return '.zip'
        if header[:6] == b'\x37\x7a\xbc\xaf\x27\x1c':
            return '.7z'
        if header[:2] == b'\x7f\x45':  # ELF (xbl_config.img is an ELF binary)
            return '.img'
        if header[:4] == b'\x41\x4e\x44\x52':  # ANDROID! (boot image)
            return '.img'
    except Exception:
        pass
    return ''

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
    
    # --- Handle direct .img input ---
    if zip_path.suffix.lower() == '.img':
        logger.info("Input is a direct .img file, using it as xbl_config...")
        if zip_path != final_img:
            final_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(zip_path, final_img)
        else:
            logger.info("File is already at the target location, skipping copy.")
        logger.info("Calculating MD5 checksum...")
        md5_sum = calculate_md5(zip_path)
        metadata = {}
    else:
        metadata = {}
        if zip_path and Path(zip_path).exists():
            md5_sum = calculate_md5(zip_path)
        
        # 1. Skip extraction if image already exists (cache hit optimization)
        if final_img.exists():
            logger.info(f"Image already exists at {final_img}, skipping extraction.")
        else:
            if not zip_path or not Path(zip_path).exists():
                logger.error("Missing firmware file and no cached image found.")
                return None
            
            zip_path = Path(zip_path).resolve()

            # 2. Clean/Create directories for extraction
            if output_dir.exists():
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True)
            
            if not final_dir.exists():
                final_dir.mkdir(parents=True)
            
            suffix = zip_path.suffix.lower()
            
            # Detect by magic bytes if extension is unknown
            if suffix not in ('.7z', '.zip', '.img'):
                detected = detect_file_type(zip_path)
                if detected:
                    logger.info(f"Detected file type '{detected}' by magic bytes (extension: '{suffix}')")
                    suffix = detected
            
            # --- Handle .img files (detected by magic bytes) ---
            if suffix == '.img':
                logger.info("Detected as a direct .img file...")
                if zip_path != final_img:
                    final_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(zip_path, final_img)
                else:
                    logger.info("File is already at the target location, skipping copy.")
                metadata = {}
                
            # --- Handle .7z archives (fastboot image packages) ---
            elif suffix == '.7z':
                logger.info("Input is a .7z archive, extracting with 7z...")
                cmd_7z = ["7z", "x", str(zip_path), f"-o{output_dir}", "-y"]
                if not run_command(cmd_7z):
                    logger.error("7z extraction failed.")
                    return None
                
                img_files = list(output_dir.rglob("*xbl_config*.img"))
                if not img_files:
                    logger.error("xbl_config.img not found in .7z archive")
                    return None
                
                src_img = img_files[0]
                logger.info(f"Found image: {src_img}")
                logger.info(f"Moving to: {final_img}")
                shutil.move(src_img, final_img)
                shutil.rmtree(output_dir)
                
            # --- Handle .zip archives (OTA payload packages) ---
            elif suffix == '.zip':
                metadata = extract_ota_metadata(zip_path)
                
                extracted_direct = None
                try:
                    with zipfile.ZipFile(zip_path, 'r') as z:
                        for info in z.infolist():
                            if info.is_dir():
                                continue
                            path_obj = Path(info.filename)
                            if 'xbl_config' in path_obj.stem and path_obj.suffix == '.img':
                                logger.info(f"Found {info.filename} directly in zip. Extracting...")
                                extracted_direct = Path(z.extract(info, path=output_dir))
                                break
                except Exception as e:
                    logger.warning(f"Direct extraction search failed: {e}")
                    
                if extracted_direct:
                    src_img = extracted_direct
                    logger.info(f"Found image directly: {src_img}")
                    logger.info(f"Moving to: {final_img}")
                    shutil.move(src_img, final_img)
                    shutil.rmtree(output_dir)
                else:
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
                        
                    # Find extracted image recursively
                    img_files = list(output_dir.rglob("*xbl_config*.img"))
                    if not img_files:
                        logger.error("xbl_config image not found in extraction output")
                        return None
                    
                    src_img = img_files[0]
                    logger.info(f"Found image: {src_img}")
                    logger.info(f"Moving to: {final_img}")
                    shutil.move(src_img, final_img)
                    shutil.rmtree(output_dir)
            else:
                logger.error(f"Unsupported file format: {suffix}")
                return None
    
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
        
    if 'md5_sum' in locals():
        result['md5'] = md5_sum

    return result

def main():
    parser = argparse.ArgumentParser(description="Analyze firmware ARB index.")
    parser.add_argument("zip_path", help="Path to firmware.zip")
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
