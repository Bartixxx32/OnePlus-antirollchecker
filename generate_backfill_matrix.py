#!/usr/bin/env python3
import json
import os
import requests
from config import DEVICE_METADATA
from fetch_firmware import get_springer_versions

def split_into_shards(items, shard_count=4):
    """Split items into balanced shards for GitHub Actions matrices."""
    return [items[i::shard_count] for i in range(shard_count)]


def generate_backfill_matrix():
    include_list = []
    
    target_device = os.environ.get("TARGET_DEVICE", "").strip().lower()
    target_variant = os.environ.get("TARGET_VARIANT", "").strip().lower()
    
    session = requests.Session()
    
    for device_id, meta in DEVICE_METADATA.items():
        if target_device and target_device != device_id.lower() and target_device != meta['name'].lower():
            continue
            
        valid_regions = meta.get('models', {}).keys()
        
        for region in valid_regions:
            if target_variant and target_variant != region.lower():
                continue
                
            print(f"Checking versions for {device_id} {region}...")
            res = get_springer_versions(device_id, region, session)
            
            if not res:
                continue
            
            versions, _ = res
            
            # Take top 5 versions (Springer usually lists newest first)
            target_versions = versions[:5]
            
            for version in target_versions:
                # We need to extract the version string carefully 
                # as Springer might return "Version (Date)"
                # But fetch_firmware.py handles substrings so it's fine
                
                include_list.append({
                    "device": device_id,
                    "variant": region,
                    "device_short": device_id,
                    "device_name": meta['name'],
                    "version": version
                })
                
    # Split into shards so no single GitHub Actions matrix exceeds the
    # hard limit of 256 jobs. Four shards support up to 1024 configurations.
    SHARD_COUNT = 4
    shards = split_into_shards(include_list, SHARD_COUNT)
    
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            for i, shard in enumerate(shards, 1):
                if shard:
                    f.write(f"matrix_{i}={json.dumps({'include': shard})}\n")
                else:
                    f.write(f"matrix_{i}=\n")
        print(f"Generated {len(include_list)} configurations in {sum(1 for s in shards if s)} shard(s).")
    else:
        for i, shard in enumerate(shards, 1):
            print(f"Shard {i}: {len(shard)} configurations")
            print(json.dumps({"include": shard}))

if __name__ == "__main__":
    generate_backfill_matrix()
