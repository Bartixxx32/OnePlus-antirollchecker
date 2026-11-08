#!/usr/bin/env python3
import json
import os
import sys
import requests
from config import DEVICE_METADATA
from fetch_firmware import get_springer_versions

DEFAULT_MAX_VERSIONS = 10
MAX_CONFIGS_PER_SHARD = 256


def parse_max_versions(value):
    """Parse the max-versions input. 0/empty/all means every available version."""
    value = (value or "").strip().lower()
    if value in ("", "all", "wszystko"):
        return None
    try:
        parsed = int(value)
    except ValueError:
        return DEFAULT_MAX_VERSIONS
    return None if parsed <= 0 else parsed


def select_versions(versions, max_versions):
    """Return the newest N versions, or all versions when max_versions is None/0."""
    if max_versions is None or max_versions <= 0:
        return list(versions)
    return list(versions[:max_versions])


def split_into_shards(items, shard_count=4):
    """Split items into balanced shards for GitHub Actions matrices."""
    return [items[i::shard_count] for i in range(shard_count)]


def generate_backfill_matrix():
    include_list = []
    
    target_device = os.environ.get("TARGET_DEVICE", "").strip().lower()
    target_variant = os.environ.get("TARGET_VARIANT", "").strip().lower()
    max_versions = parse_max_versions(os.environ.get("MAX_VERSIONS", str(DEFAULT_MAX_VERSIONS)))

    print(f"Max versions per region: {'all' if max_versions is None else max_versions}")
    
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
            
            # Springer lists newest first. MAX_VERSIONS controls how many we take.
            target_versions = select_versions(versions, max_versions)
            
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

    if any(len(shard) > MAX_CONFIGS_PER_SHARD for shard in shards):
        print(
            f"ERROR: {len(include_list)} configurations exceed "
            f"{SHARD_COUNT * MAX_CONFIGS_PER_SHARD} slots "
            f"({MAX_CONFIGS_PER_SHARD} per shard). Increase SHARD_COUNT.",
            file=sys.stderr,
        )
        sys.exit(1)
    
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
