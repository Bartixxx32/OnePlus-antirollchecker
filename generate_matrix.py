import json
import os
from config import DEVICE_METADATA

def generate_matrix():
    include_list = []
    
    # Temporary exclusions for failing devices
    EXCLUDE = [
        ("Find X8 Pro", "IN"), ("Find X8 Pro", "EU"), ("Find X8 Pro", "CN"),
        ("Find X8", "CN"), ("Find X8", "IN"),
        ("Find N3", "IN"), # Fails in check-variant
        ("9R", "IN"),
        ("10R", "IN"),
        ("Ace 5 Ultimate", "CN")
    ]

    for device_id, meta in DEVICE_METADATA.items():
        # Get all valid regions from the 'models' dictionary keys
        valid_regions = meta.get('models', {}).keys()
        
        for region in valid_regions:
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
        print(matrix_json)

if __name__ == "__main__":
    generate_matrix()
