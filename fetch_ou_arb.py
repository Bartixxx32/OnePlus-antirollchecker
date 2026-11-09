#!/usr/bin/env python3
"""Check ARB for one OTA package using HTTP range requests only."""

import argparse
import json
import logging
import sys

from ota_arb import (
    ArbUndetectableError,
    check_arb,
    classify_remote_package,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_result(args, arb_result):
    arb = int(arb_result.get("arb", -1))
    return {
        "device_short": args.device_short,
        "variant": args.variant,
        "version": args.version,
        "arb_index": str(arb),
        "arb_detected": arb >= 0,
        "major": str(arb_result.get("major", 0)),
        "minor": str(arb_result.get("minor", 0)),
        "partition": arb_result.get("partition"),
        "package_type": arb_result.get("package_type"),
        "md5": args.md5 or None,
        "ota_metadata": {
            "url": args.url,
            "ota_version": args.ota_version,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check ARB from a remote OTA package without downloading it."
    )
    parser.add_argument("--device-short", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--md5", default=None)
    parser.add_argument("--ota-version", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        arb_result = check_arb(args.url)
    except ArbUndetectableError as exc:
        # Some older packages (OnePlus 8/8 Pro/9) contain no parseable ARB
        # record.  Keep the version in history instead of losing the check.
        logger.warning("ARB undetectable: %s", exc)
        arb_result = {
            "arb": -1,
            "major": 0,
            "minor": 0,
            "partition": None,
            "package_type": classify_remote_package(args.url),
        }
    except Exception as exc:  # noqa: BLE001 - surface the reason to the workflow
        logger.error("ARB check failed: %s", exc)
        return 1

    result = build_result(args, arb_result)
    if args.json:
        print(json.dumps(result))
    else:
        print(f"ARB (Anti-Rollback): {result['arb_index']}")
        print(f"Major Version: {result['major']}")
        print(f"Minor Version: {result['minor']}")
        print(f"Package Type: {result.get('package_type') or 'unknown'}")
        print(f"Partition: {result['partition']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
