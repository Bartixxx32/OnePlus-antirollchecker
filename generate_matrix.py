import json
import os
from config import DEVICE_METADATA

# Temporary exclusions for failing devices
EXCLUDE = [
    ("Find X8 Pro", "IN"), ("Find X8 Pro", "EU"), ("Find X8 Pro", "CN"),
    ("Find X8", "CN"), ("Find X8", "IN"),
    ("Find X8 Ultra", "CN"),
    ("Find N5", "CN"),
    ("Find N3", "IN"),  # Fails in check-variant
    ("9R", "IN"),
    ("10R", "IN"),
    ("Ace 5 Ultimate", "CN"),
    ("Find X5", "CN"),
    ("Find X5 Pro", "CN"),
    ("8T", "IN"),
]


def build_matrix(target_device='', target_variant=''):
    """Return every device/region configuration that should be checked."""
    include_list = []
    target_device = (target_device or '').strip()
    target_variant = (target_variant or '').strip()

    for device_id, meta in DEVICE_METADATA.items():
        # Filter by device if specified
        if target_device and device_id != target_device:
            continue

        # Get all valid regions from the 'models' dictionary keys
        valid_regions = meta.get('models', {}).keys()

        for region in valid_regions:
            # Filter by variant if specified
            if target_variant and region != target_variant:
                continue

            if (device_id, region) in EXCLUDE:
                continue

            include_list.append({
                "device": device_id,
                "variant": region,
                "device_short": device_id,
                "device_name": meta['name']
            })

    return include_list


def generate_matrix():
    include_list = build_matrix(
        target_device=os.environ.get('TARGET_DEVICE', ''),
        target_variant=os.environ.get('TARGET_VARIANT', ''),
    )

    # Output for GitHub Actions
    matrix_json = json.dumps({"include": include_list})

    # Write to GITHUB_OUTPUT if available, else print
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"matrix={matrix_json}\n")
    else:
        print(f"Generated {len(include_list)} matrix entries.")
        print(matrix_json)


if __name__ == "__main__":
    generate_matrix()
