import json
import re
from pathlib import Path

def test_readme_order():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Find a few devices and check their region order
    devices = ["OnePlus 15", "OnePlus 12", "OnePlus Nord 4"]
    priority = ['Global', 'Europe', 'India', 'North America', 'China']

    for device in devices:
        start_idx = content.find(f"#### {device}")
        if start_idx == -1:
            print(f"Device {device} not found in README")
            continue

        # Get the table content for this device
        end_idx = content.find("---", start_idx)
        table_content = content[start_idx:end_idx]

        # Find all regions in the table
        found_regions = []
        for region in priority:
            if f"| {region} |" in table_content:
                found_regions.append(region)

        # Extract the regions in the order they appear
        lines = table_content.split('\n')
        actual_order = []
        for line in lines:
            for region in priority:
                if f"| {region} |" in line:
                    actual_order.append(region)
                    break

        expected_order = sorted(found_regions, key=lambda x: priority.index(x))
        if actual_order == expected_order:
            print(f"Order for {device} is CORRECT: {actual_order}")
        else:
            print(f"Order for {device} is INCORRECT!")
            print(f"  Expected: {expected_order}")
            print(f"  Actual:   {actual_order}")

if __name__ == "__main__":
    test_readme_order()
