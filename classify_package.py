#!/usr/bin/env python3
"""Classify a remote OTA package as full or incremental.

Only ZIP central-directory, OTA metadata and payload-manifest bytes are read;
the firmware itself is never downloaded.
"""

import argparse
import json
import logging
import sys

from ota_arb import classify_remote_package

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Detect whether an OTA package is incremental or full."
    )
    parser.add_argument("url", help="Direct firmware download URL")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    package_type = classify_remote_package(args.url)
    result = {"package_type": package_type}

    if args.json:
        print(json.dumps(result))
    else:
        print(package_type or "unknown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
