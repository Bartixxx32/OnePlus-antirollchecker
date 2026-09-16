import json
import os
from config import DEVICE_METADATA

def generate_matrix():
    include_list = []
    
    # Optional filtering from workflow_dispatch inputs
    target_device = os.environ.get('TARGET_DEVICE', '').strip()
    target_variant = os.environ.get('TARGET_VARIANT', '').strip()
    
    # Temporary exclusions for failing devices
    EXCLUDE = [
        # Oppo Find
        ("Find X8 Pro", "IN"), ("Find X8 Pro", "EU"), ("Find X8 Pro", "CN"),
        ("Find X8", "CN"), ("Find X8", "IN"),
        ("Find N3", "IN"), ("Find N3", "SG"), ("Find N3", "VN"), ("Find N3", "OCA"),
        ("Find N3", "TH"), ("Find N3", "ID"), ("Find N3", "MY"), ("Find N3", "TW"),
        ("Find N5", "MY"), ("Find N5", "CN"), ("Find N5", "APC"), ("Find N5", "MX"),
        ("Find N5", "TH"), ("Find N5", "ID"), ("Find N5", "SG"),
        ("Find X8 Ultra", "CN"),
        ("Find X5", "CN"), ("Find X5", "SA"), ("Find X5", "EG"), ("Find X5", "EU"), ("Find X5", "OCA"),
        ("Find X5 Pro", "CN"), ("Find X5 Pro", "EU"), ("Find X5 Pro", "SG"),
        ("Find X5 Pro", "EG"), ("Find X5 Pro", "TW"), ("Find X5 Pro", "OCA"),
        ("Find X3 Pro", "TW"), ("Find X3 Pro", "EU"), ("Find X3 Pro", "SG"),
        # Oppo Reno
        ("Reno10 Pro", "ID"), ("Reno10 Pro", "APC"), ("Reno10 Pro", "MEA"),
        ("Reno10 Pro", "IN"), ("Reno10 Pro", "MY"), ("Reno10 Pro", "OCA"),
        ("Reno10 Pro", "PH"), ("Reno10 Pro", "SA"), ("Reno10 Pro", "SG"),
        ("Reno10 Pro", "VN"), ("Reno10 Pro", "TH"), ("Reno10 Pro", "TW"),
        # Oppo Pad
        ("Pad 3", "NA"),
        # OnePlus legacy 7/7T
        ("7", "GLO"), ("7", "EU"), ("7", "IN"),
        ("7 Pro", "GLO"), ("7 Pro", "IN"), ("7 Pro", "EU"),
        ("7T", "IN"), ("7T", "EU"), ("7T", "GLO"),
        ("7T Pro", "IN"), ("7T Pro", "EU"), ("7T Pro", "GLO"),
        # OnePlus 8/8T
        ("8", "NA"), ("8", "IN"), ("8", "EU"),
        ("8 Pro", "NA"), ("8 Pro", "IN"), ("8 Pro", "EU"),
        ("8T", "IN"), ("8T", "EU"), ("8T", "NA"),
        # OnePlus 9/9 Pro/9RT
        ("9", "NA"), ("9", "EU"), ("9", "IN"),
        ("9 Pro", "NA"), ("9 Pro", "EU"), ("9 Pro", "IN"),
        ("9RT", "IN"),
        ("9R", "IN"),
        # OnePlus 10/11/12/13
        ("10 Pro", "NA"), ("10T", "NA"), ("10R", "IN"),
        ("11", "NA"),
        ("12", "NA"),
        ("12R", "NA"),
        ("13", "NA"),
        # OnePlus Open
        ("Open", "NA"),
        # OnePlus Nord
        ("Nord CE 2 Lite", "IN"), ("Nord CE 2 Lite", "EU"), ("Nord CE 2 Lite", "GLO"),
        ("Nord 1", "IN"), ("Nord 1", "EU"),
        ("Nord N30", "NA"), ("Nord N20", "NA"), ("Nord N200 5G", "NA"),
        # Misc
        ("Ace 5 Ultimate", "CN"),
    ]

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
