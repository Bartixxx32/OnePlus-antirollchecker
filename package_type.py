#!/usr/bin/env python3
"""Classify OTA packages as full or incremental.

Incremental (delta) OTA packages cannot be flashed standalone: they contain
source-dependent operations and/or a ``pre-build`` fingerprint that must match
the firmware already installed on the device.  Classification is done per
package, never per source, because both full and incremental packages can be
served from the same updater API.
"""

import struct
import zipfile

from ota_proto import update_metadata_pb2

INCREMENTAL = "incremental"
FULL = "full"

# Android update_engine operation types that read data from the installed
# (source) build.  Their presence proves that a package is a delta update.
SOURCE_DEPENDENT_OPERATIONS = {
    2,   # MOVE
    3,   # BSDIFF
    4,   # SOURCE_COPY
    5,   # SOURCE_BSDIFF
    9,   # PUFFDIFF
    10,  # BROTLI_BSDIFF
    11,  # ZUCCHINI
    12,  # LZ4DIFF_BSDIFF
    13,  # LZ4DIFF_PUFFDIFF
}


def classify_metadata(metadata):
    """Return ``incremental`` when OTA metadata contains a ``pre-build``."""
    if not metadata:
        return None
    if metadata.get("pre-build") or metadata.get("pre-build-incremental"):
        return INCREMENTAL
    return None


def manifest_is_incremental(manifest):
    """Return True when a payload manifest contains source-dependent ops."""
    if manifest is None:
        return False
    for partition in manifest.partitions:
        for operation in partition.operations:
            if (
                operation.type in SOURCE_DEPENDENT_OPERATIONS
                or len(operation.src_extents) > 0
            ):
                return True
    return False


def classify_package(metadata=None, manifest=None):
    """Return ``incremental``, ``full`` or ``None`` when unknown.

    ``pre-build`` alone is enough to prove a delta package.  If it is absent,
    the payload operations decide; an empty manifest keeps the result unknown
    instead of guessing.
    """
    metadata_type = classify_metadata(metadata)
    if metadata_type:
        return metadata_type
    if manifest is None:
        return None
    return INCREMENTAL if manifest_is_incremental(manifest) else FULL


def manifest_from_zip(zip_path):
    """Read and parse ``payload.bin``'s manifest from a local OTA zip.

    Only the manifest header is read, so this stays cheap even for multi-GB
    packages.  ``payload.bin`` is normally stored uncompressed in OTA zips.
    """
    with zipfile.ZipFile(zip_path) as archive:
        info = archive.getinfo("payload.bin")
        with archive.open(info) as payload:
            header = payload.read(24)
            if len(header) < 24 or header[0:4] != b"CrAU":
                return None
            manifest_size = struct.unpack_from(">Q", header, 12)[0]
            manifest_data = payload.read(manifest_size)
    manifest = update_metadata_pb2.DeltaArchiveManifest()
    manifest.ParseFromString(manifest_data)
    return manifest


def classify_zip(zip_path):
    """Classify a local OTA zip using metadata and/or payload operations."""
    metadata = None
    manifest = None
    try:
        from analyze_firmware import extract_ota_metadata

        metadata = extract_ota_metadata(zip_path)
    except Exception:  # noqa: BLE001 - metadata is optional
        metadata = None
    try:
        manifest = manifest_from_zip(zip_path)
    except Exception:  # noqa: BLE001 - non-payload packages are allowed
        manifest = None
    return classify_package(metadata, manifest)
