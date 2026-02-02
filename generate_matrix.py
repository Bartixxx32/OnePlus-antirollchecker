import json
import os
from config import DEVICE_METADATA

def generate_matrix():
    include_list = []
    
    for device_id, meta in DEVICE_METADATA.items():
        # Get all valid regions from the 'models' dictionary keys
        valid_regions = meta.get('models', {}).keys()
        
        for region in valid_regions:
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
