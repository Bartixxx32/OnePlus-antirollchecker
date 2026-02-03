#!/usr/bin/env python3
import requests
import json
import html
import sys
import argparse
import logging
import time
from bs4 import BeautifulSoup
from config import BASE_URL, OOS_API_URL, USER_AGENT, SPRING_MAPPING, OOS_MAPPING

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def requests_get_with_retry(url, retries=3, delay=10, timeout=10):
    """
    Helper to perform requests.get with retries.
    """
    last_exception = None
    for i in range(retries):
        try:
            response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            last_exception = e
            if i < retries - 1:
                logger.warning(f"Request failed: {e}. Retrying in {delay} seconds... ({i+1}/{retries})")
                time.sleep(delay)

    # If we get here, all retries failed
    raise last_exception

def get_from_oos_api(device_id: str, region: str) -> dict:
    """
    Fetch latest firmware URL and version from oosdownloader-gui.fly.dev API.
    Returns dict with 'url' and 'version' keys, or None if failed.
    """
    mapped_id = OOS_MAPPING.get(device_id, f"oneplus_{device_id}")
    
    # Skip OOS API for CN region as per user request
    if region == "CN":
        return None
        
    # Determine brand
    brand = "oneplus"
    if mapped_id.startswith("oppo_") or mapped_id.startswith("find_"):
         brand = "oppo"

    # Map GLO/IN to EU for Oppo as OOS API often only has EU for these standard global variants
    if brand == "oppo" and region in ["GLO", "IN"]:
        region = "EU"

    # API endpoints
    # OOS_API_URL is now .../api
    url_endpoint = f"{OOS_API_URL}/{brand}/{mapped_id}/{region}/full"
    ver_endpoint = f"{OOS_API_URL}/{brand}/{mapped_id}/{region}/full/version"
    
    logger.info(f"Checking OOS API: {url_endpoint}")
    
    try:
        # Fetch URL
        resp_url = requests_get_with_retry(url_endpoint)
        download_url = resp_url.text.strip()
        
        if not download_url or not download_url.startswith("http"):
            logger.warning(f"OOS API returned invalid URL: {download_url}")
            return None
            
        # Fetch Version
        resp_ver = requests_get_with_retry(ver_endpoint)
        version_str = resp_ver.text.strip()
        
        return {
            "url": download_url,
            "version": version_str
        }
            
    except Exception as e:
        logger.warning(f"OOS API check failed: {e}")
        return None

def get_springer_versions(device_id: str, region: str, session=None) -> list:
    """
    Fetches available versions for a device/region from roms.danielspringer.at
    """
    headers = {
        'User-Agent': USER_AGENT,
    }
    
    if not session:
        session = requests.Session()
    
    # Map input device ID to website's expected name via OOS_MAPPING (snake_case)
    key = OOS_MAPPING.get(device_id, f"oneplus_{device_id}")
    
    mapped_name = SPRING_MAPPING.get(key)
    if not mapped_name:
         mapped_name = f"OP {device_id}"

    if key in SPRING_MAPPING:
        mapped_name = SPRING_MAPPING[key]
    
    try:
        response = session.get(BASE_URL, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error fetching page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    device_select = soup.find('select', {'id': 'device'})
    if not device_select:
        logger.error("Could not find device select element")
        return None

    devices_json = device_select.get('data-devices')
    if not devices_json:
        logger.error("Could not find data-devices attribute")
        return None

    devices_data = json.loads(html.unescape(devices_json))
    
    # Device name resolution
    device_name = mapped_name
    if device_name not in devices_data:
        # Try stricter fuzzy match
        found = False
        for d in devices_data:
            if device_name.upper() == d.upper() or d.upper().startswith(device_name.upper() + " "):
                device_name = d
                found = True
                break
        if not found:
            logger.error(f"Device {device_name} not found in available data")
            return None

    if region not in devices_data[device_name]:
        logger.error(f"Region {region} not found for {device_name}")
        return None
        
    return devices_data[device_name][region]

def get_signed_url_springer(device_id: str, region: str, target_version: str = None) -> dict:
    """
    Fetches a signed download URL from roms.danielspringer.at
    Returns dict with 'url' and 'version' (if known).
    """
    headers = {
        'User-Agent': USER_AGENT,
    }
    
    session = requests.Session()
    
    versions = get_springer_versions(device_id, region, session)
    if not versions:
        return None
        
    version_index = "0"
    
    if target_version:
        # Find index for target version
        found_idx = -1
        for i, v in enumerate(versions):
            if target_version in v:
                found_idx = i
                break
        
        if found_idx == -1:
            logger.error(f"Version {target_version} not found for {device_name} {region}")
            return None
        version_index = str(found_idx)
    
    found_version_name = versions[int(version_index)]

    form_data = {
        'device': device_name,
        'region': region,
        'version_index': version_index,
    }
    
    post_headers = headers.copy()
    post_headers.update({
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': BASE_URL,
    })
    
    try:
        response = session.post(BASE_URL, data=form_data, headers=post_headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Form submission failed: {e}")
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    result_div = soup.find('div', {'id': 'resultBox'})
    
    if result_div and result_div.get('data-url'):
        download_url = html.unescape(result_div.get('data-url'))
        return {
            "url": download_url,
            "version": found_version_name
        }
    else:
        logger.error("No download URL found in the response")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch signed firmware URL and version.")
    parser.add_argument("device_id", help="Device ID (e.g., 15, 15R)")
    parser.add_argument("region", help="Region code (e.g., CN, EU, GLO, IN)")
    parser.add_argument("target_version", nargs="?", help="Target version string (optional)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    parser.add_argument("--version-only", action="store_true", help="Output only the version string")
    parser.add_argument("--url-only", action="store_true", help="Output only the URL (default behavior otherwise)")
    parser.add_argument("--output", help="Write result JSON to file instead of stdout")
    
    args = parser.parse_args()
    
    # Strip 'oneplus_' prefix
    clean_device_id = args.device_id.replace("oneplus_", "")
    
    result = None
    
    if not args.target_version:
        result = get_from_oos_api(clean_device_id, args.region)
        if result:
            logger.info("Found via OOS API")
    
    if not result:
        logger.info("Falling back to Springer (roms.danielspringer.at)...")
        result = get_signed_url_springer(clean_device_id, args.region, args.target_version)
    
    if result:
        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f)
        elif args.json:
            print(json.dumps(result))
        elif args.version_only:
            print(result['version'])
        else:
            # Default: print URL
            print(result['url'])
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
