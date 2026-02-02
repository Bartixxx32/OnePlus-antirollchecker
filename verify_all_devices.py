
import sys
import os
import subprocess
from config import DEVICE_METADATA

def verify_all():
    results = []
    print(f"{'Device':<20} | {'Region':<6} | {'Status':<10} | {'Result'}")
    print("-" * 60)

    for device_id, meta in DEVICE_METADATA.items():
        name = meta['name']
        for region, model in meta['models'].items():
            # Skip if region is not a target for checks (optional, but we want to check all)
            
            cmd = ["python", "fetch_firmware.py", device_id, region, "--url-only"]
            try:
                # Capture output
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    url = proc.stdout.strip()
                    if url.startswith("http"):
                        status = "OK"
                        msg = "URL Found"
                    else:
                        status = "FAIL"
                        msg = f"Invalid Output: {url[:30]}..."
                else:
                    status = "FAIL"
                    msg = "Command Failed"
            except subprocess.TimeoutExpired:
                 status = "FAIL"
                 msg = "Timeout"
            except Exception as e:
                status = "FAIL"
                msg = str(e)
            
            print(f"{name:<20} | {region:<6} | {status:<10} | {msg}")
            results.append((name, region, status, msg))

    print("-" * 60)
    failures = [r for r in results if r[2] != "OK"]
    if failures:
        print(f"\nFound {len(failures)} failures:")
        for f in failures:
            print(f"{f[0]} ({f[1]}): {f[3]}")
    else:
        print("\nAll devices passed verification!")

if __name__ == "__main__":
    verify_all()
