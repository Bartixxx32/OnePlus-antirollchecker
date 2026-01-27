#!/usr/bin/env python3
import requests
import json
import html
import sys
import re
from bs4 import BeautifulSoup
from config import DEVICE_ID_TO_NAME

def get_signed_url(device_id, region, target_version=None):
    """
    Fetches a signed download URL from roms.danielspringer.at
    If target_version is None, fetches the newest (index 0).
    """
    base_url = "https://roms.danielspringer.at/index.php?view=ota"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    session = requests.Session()
    
    device_name = DEVICE_ID_TO_NAME.get(device_id, device_id.replace("_", " ").upper())
    
    # print(f"[*] Fetching mapping for {device_name} ({region})...", file=sys.stderr)
    try:
        response = session.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    device_select = soup.find('select', {'id': 'device'})
    if not device_select:
        print("Could not find device select element", file=sys.stderr)
        return None

    devices_json = device_select.get('data-devices')
    if not devices_json:
        print("Could not find data-devices attribute", file=sys.stderr)
        return None

    devices_data = json.loads(html.unescape(devices_json))
    
    if device_name not in devices_data:
        # Try fuzzy match
        found = False
        for d in devices_data:
            if device_name in d or d in device_name:
                device_name = d
                found = True
                break
        if not found:
            print(f"Device {device_name} not found in available data", file=sys.stderr)
            return None

    if region not in devices_data[device_name]:
        print(f"Region {region} not found for {device_name}", file=sys.stderr)
        return None
        
    versions = devices_data[device_name][region]
    version_index = "0"
    
    if target_version:
        # Find index for target version
        found_idx = -1
        for i, v in enumerate(versions):
            if target_version in v:
                found_idx = i
                break
        
        if found_idx == -1:
            print(f"Version {target_version} not found for {device_name} {region}", file=sys.stderr)
            return None
        version_index = str(found_idx)
    
    # print(f"[*] Retrieving signed URL for index {version_index} ({versions[int(version_index)]})...", file=sys.stderr)
    
    form_data = {
        'device': device_name,
        'region': region,
        'version_index': version_index,
    }
    
    post_headers = headers.copy()
    post_headers.update({
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': base_url,
    })
    
    try:
        response = session.post(base_url, data=form_data, headers=post_headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Form submission failed: {e}", file=sys.stderr)
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    result_div = soup.find('div', {'id': 'resultBox'})
    
    if result_div and result_div.get('data-url'):
        download_url = html.unescape(result_div.get('data-url'))
        # Return just the URL to stdout
        return download_url
    else:
        print("No download URL found in the response", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: fetch_firmware.py <device_id> <region> [target_version]")
        sys.exit(1)
        
    device_id = sys.argv[1]
    region = sys.argv[2]
    target_version = sys.argv[3] if len(sys.argv) > 3 else None
    
    url = get_signed_url(device_id, region, target_version)
    if url:
        print(url)
    else:
        sys.exit(1)
