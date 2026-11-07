#!/usr/bin/env python3
"""Parse Qualcomm xbl_config ELF images and extract the ARB index.

The third-party ``arbextract`` 1.0 tool assumes a fixed layout for the
hash segment and reads the OEM metadata 16 bytes too early on devices
using hash-table format v8 (e.g. OnePlus 16).  That makes it report the
first field of an unrelated hash-table record (0x25 / 37) as the major
version and a constant ``3`` as the ARB index.

This parser keeps the legacy behaviour for images whose metadata is at
the classic offset, and falls back to scanning for a plausible OEM
metadata record when the classic offset clearly contains garbage.
"""

import argparse
import json
import struct
import sys
from pathlib import Path

ELF_MAGIC = b"\x7fELF"
MAX_MAJOR = 10
MAX_MINOR = 10
MAX_ARB = 100


def _find_hash_segment(data: bytes):
    """Return (offset, size) of the hash segment (last large PT_NULL)."""
    if len(data) < 64 or data[:4] != ELF_MAGIC or data[4] != 2:
        return None

    phoff = struct.unpack_from("<Q", data, 0x20)[0]
    phentsize = struct.unpack_from("<H", data, 0x36)[0]
    phnum = struct.unpack_from("<H", data, 0x38)[0]

    candidates = []
    for i in range(phnum):
        pos = phoff + i * phentsize
        if pos + 56 > len(data):
            break
        p_type = struct.unpack_from("<I", data, pos)[0]
        p_offset = struct.unpack_from("<Q", data, pos + 8)[0]
        p_filesz = struct.unpack_from("<Q", data, pos + 32)[0]
        # The hash segment is a PT_NULL segment.  Require a meaningful
        # size so the ELF header segment is not picked up.
        if p_type == 0 and p_filesz > 0x100:
            candidates.append((p_offset, p_filesz))

    return candidates[-1] if candidates else None


def _find_hash_header(data: bytes, start: int, length: int):
    """Locate the hash-table header inside the hash segment."""
    scan_limit = min(0x1000, max(0, length - 36))
    for off in range(0, scan_limit, 4):
        pos = start + off
        version, common, qti, oem, hash_tbl = struct.unpack_from("<IIIII", data, pos)
        if (
            1 <= version <= 10
            and common <= 0x1000
            and oem <= 0x4000
            and hash_tbl <= 0x4000
            and off + 36 + common + qti + oem <= length
        ):
            return off, common, qti
    return None


def _plausible(major: int, minor: int, arb: int, reserved: int) -> bool:
    return (
        0 <= major <= MAX_MAJOR
        and 0 <= minor <= MAX_MINOR
        and 0 <= arb <= MAX_ARB
        and reserved == 0
    )


def _read_record(data: bytes, pos: int):
    if pos < 0 or pos + 16 > len(data):
        return None
    major, minor, arb, reserved = struct.unpack_from("<IIII", data, pos)
    return major, minor, arb, reserved


def parse_elf64_arb(data: bytes):
    """Extract ARB metadata from an xbl_config ELF image.

    Returns a dict with ``arb``, ``major`` and ``minor`` or ``None``.
    """
    segment = _find_hash_segment(data)
    if not segment:
        return None

    hash_start, hash_len = segment
    if hash_start + hash_len > len(data):
        return None

    header = _find_hash_header(data, hash_start, hash_len)
    if not header:
        return None

    off, common, qti = header

    # Classic layout used by hash-table v7 and older: the OEM metadata
    # starts right after the 36-byte header and the common/QTI blocks.
    classic = hash_start + off + 36 + common + qti
    record = _read_record(data, classic)

    if record and _plausible(*record):
        major, minor, arb, _ = record
        return {"arb": arb, "major": major, "minor": minor}

    # Newer layout (hash-table v8, e.g. OnePlus 16) inserts an extra
    # 16-byte hash-table record, shifting the OEM metadata by 16 bytes.
    # Records are 16-byte aligned, so scan in steps of 16 to avoid
    # misaligned false positives (e.g. reading "3, 0, 4, 0" from the
    # middle of two adjacent records).
    limit = min(hash_start + hash_len - 16, classic + 0x400)
    pos = classic + 16
    while pos <= limit:
        record = _read_record(data, pos)
        if record:
            major, minor, arb, reserved = record
            # A major version of 0 is valid on legacy images, but when we
            # are in the fallback path the classic offset was already
            # implausible, so require a real major version here.
            if 1 <= major <= MAX_MAJOR and _plausible(major, minor, arb, reserved):
                return {"arb": arb, "major": major, "minor": minor}
        pos += 16

    return None


def parse_xbl_config_file(path: str):
    return parse_elf64_arb(Path(path).read_bytes())


def main():
    parser = argparse.ArgumentParser(description="Extract ARB index from xbl_config.img")
    parser.add_argument("image", help="Path to xbl_config.img")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    try:
        result = parse_xbl_config_file(args.image)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not result:
        print("ERROR: could not parse ARB metadata", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"arb_index": result["arb"], "major": result["major"], "minor": result["minor"]}))
    else:
        # Match arbextract's output format so existing pipelines keep working.
        print(f"ARB (Anti-Rollback): {result['arb']}")
        print(f"Major Version: {result['major']}")
        print(f"Minor Version: {result['minor']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
