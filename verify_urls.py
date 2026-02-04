
import json
import subprocess
from config import DEVICE_METADATA

def verify_firmware():
    results = {
        "found": [],
        "missing": []
    }
    
    for device_id, meta in DEVICE_METADATA.items():
        name = meta["name"]
        print(f"Checking {name} ({device_id})...")
        for region in meta["models"].keys():
            print(f"  Region: {region}...", end=" ", flush=True)
            try:
                # Use fetch_firmware.py to check
                # We use --json to get structured output
                cmd = ["python", "fetch_firmware.py", device_id, region, "--json"]
                process = subprocess.run(cmd, capture_output=True, text=True)
                
                if process.returncode == 0:
                    data = json.loads(process.stdout)
                    if data.get("url"):
                        print("OK")
                        results["found"].append(f"{device_id}_{region}")
                    else:
                        print("MISSING URL")
                        results["missing"].append(f"{device_id}_{region}")
                else:
                    print(f"FAILED (Exit {process.returncode})")
                    results["missing"].append(f"{device_id}_{region}")
                    
            except Exception as e:
                print(f"ERROR: {e}")
                results["missing"].append(f"{device_id}_{region}")
                
    return results

if __name__ == "__main__":
    results = verify_firmware()
    print("\nVerification Summary:")
    print(f"Found: {len(results['found'])}")
    print(f"Missing: {len(results['missing'])}")
    if results["missing"]:
        print("\nMissing Variants:")
        for m in results["missing"]:
            print(f"  - {m}")
    
    with open("verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
