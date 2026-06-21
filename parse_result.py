import sys
import json
import os

def main():
    try:
        if not os.path.exists('result.json'):
            print("result.json not found")
            return

        with open('result.json', 'r') as f:
            data = json.load(f)

        meta = data.get('ota_metadata', {})
        is_img_check = not meta  # true if no ota_metadata (direct .img check)
        
        # Extract fields
        if is_img_check:
            device = 'Direct .img Check'
            product = 'N/A'
            version = 'N/A'
            patch = 'N/A'
            build = 'N/A'
        else:
            device = meta.get('pre-device', meta.get('post-device', 'Unknown Device'))
            if ',' in device:
                device = device.split(',')[0]
            
            product = meta.get('product_name', 'Unknown')
            
            # Version logic
            version = meta.get('version_name_show', meta.get('display-version', meta.get('post-build-incremental', 'Unknown Version')))
            
            patch = meta.get('post-security-patch-level', meta.get('security_patch', 'Unknown'))
            build = meta.get('post-build', 'Unknown')
        
        arb = data.get('arb_index', 'Unknown')
        
        # Output to file for shell sourcing
        print(f"Parsing successful. Device: {device}, Version: {version}")
        with open('fw_env', 'w') as f:
            f.write(f'DETECTED_DEVICE="{device}"\n')
            f.write(f'DETECTED_PRODUCT="{product}"\n')
            f.write(f'DETECTED_VERSION="{version}"\n')
            f.write(f'DETECTED_PATCH="{patch}"\n')
            f.write(f'DETECTED_BUILD="{build}"\n')
            f.write(f'DETECTED_ARB="{arb}"\n')
            f.write(f'IMAGE_CHECK="{str(is_img_check).lower()}"\n')
            
    except Exception as e:
        print(f"Error parsing metadata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
