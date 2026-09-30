import sys
from fetch_firmware import get_from_oos_api, get_signed_url_springer

devices = [
    ("7 Pro", ["GLO", "EU", "IN"]),
    ("7", ["GLO", "EU", "IN"]),
    ("7T", ["GLO", "EU", "IN"]),
    ("7T Pro", ["GLO", "EU", "IN"]),
    ("8", ["NA", "IN", "EU"]),
    ("8 Pro", ["NA", "IN", "EU"]),
    ("8T", ["NA", "IN", "EU"]),
    ("9", ["NA", "EU", "IN"]),
    ("9 Pro", ["NA", "EU", "IN"]),
    ("9RT", ["IN"]),
    ("13", ["NA"]),
    ("12", ["NA"]),
    ("11", ["NA"]),
    ("12R", ["NA"]),
    ("10 Pro", ["NA"]),
    ("10T", ["NA"]),
    ("Open", ["NA"]),
    ("Nord CE 2 Lite", ["IN", "EU", "GLO"]),
    ("Nord 1", ["IN", "EU"]),
    ("Nord N30", ["NA"]),
    ("Nord N20", ["NA"]),
    ("Nord N200 5G", ["NA"]),
    ("Pad 3", ["NA"]),
]

print("=== OOS API ===")
for dev, regions in devices:
    for r in regions:
        try:
            res = get_from_oos_api(dev, r)
            status = "OK" if res else "FAIL"
            print(f"  {dev} / {r}: {status}")
        except Exception as e:
            print(f"  {dev} / {r}: ERROR {e}")

print()
print("=== Springer API (fallback) ===")
for dev, regions in devices:
    for r in regions:
        try:
            res = get_signed_url_springer(dev, r)
            status = "OK" if res else "FAIL"
            ver = res.get("version", "?") if res else ""
            print(f"  {dev} / {r}: {status} {ver}")
        except Exception as e:
            print(f"  {dev} / {r}: ERROR {e}")
