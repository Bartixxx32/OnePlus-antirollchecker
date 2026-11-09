#!/usr/bin/env python3
"""Check the Anti-Rollback index without downloading a full OTA package.

The package is a ZIP whose ``payload.bin`` is stored uncompressed.  We read
the ZIP central directory, the payload manifest and only the bytes belonging
to ``xbl_config`` using HTTP range requests.  This keeps a single ARB check
in the low-megabyte range even for multi-gigabyte packages.
"""

import bz2
import logging
import lzma
import re
import struct
import time

import requests

from arb_parser import parse_elf64_arb
from ota_proto import update_metadata_pb2

logger = logging.getLogger(__name__)

PARTITION_CANDIDATES = ["xbl_config", "xbl", "abl", "xbl_ramdump"]
MAX_PARTITION_SIZE = 10 * 1024 * 1024


def _ota_headers():
    return {"User-Agent": "okhttp/3.12.12", "userId": "oplus-ota|16002018"}


def _read_range(url, start, end, retries=4, timeout=(30, 120)):
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers={**_ota_headers(), "Range": f"bytes={start}-{end}"},
                timeout=timeout,
            )
            response.raise_for_status()
            return response.content
        except Exception as exc:  # noqa: BLE001 - retry transient CDN errors
            last_error = exc
            if attempt < retries - 1:
                time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"Range request failed for {start}-{end}: {last_error}")


def _resolve_if_needed(url):
    """Follow redirects and return the effective CDN URL."""
    response = requests.head(
        url, allow_redirects=True, headers=_ota_headers(), timeout=30
    )
    if response.ok:
        return response.url
    response = requests.get(
        url,
        allow_redirects=True,
        headers={**_ota_headers(), "Range": "bytes=0-0"},
        timeout=30,
    )
    response.raise_for_status()
    return response.url


def _get_file_size(url):
    response = requests.head(url, headers=_ota_headers(), timeout=30)
    if response.ok:
        content_length = response.headers.get("Content-Length")
        if content_length:
            return int(content_length)

    response = requests.get(
        url, headers={**_ota_headers(), "Range": "bytes=0-0"}, timeout=30
    )
    if response.status_code == 206:
        match = re.search(r"/\s*(\d+)$", response.headers.get("Content-Range", ""))
        if match:
            return int(match.group(1))
    response.raise_for_status()
    content_length = response.headers.get("Content-Length")
    if content_length:
        return int(content_length)
    raise RuntimeError("Could not determine file size")


def _read_zip64_extra(extra_data):
    offset = 0
    result = {}
    while offset + 4 <= len(extra_data):
        tag, size = struct.unpack_from("<HH", extra_data, offset)
        if tag == 0x0001:
            pos = offset + 4
            if size >= 8:
                result["origSize"] = struct.unpack_from("<Q", extra_data, pos)[0]
                pos += 8
            if size >= 16:
                result["compSize"] = struct.unpack_from("<Q", extra_data, pos)[0]
                pos += 8
            if size >= 24:
                result["localOffset"] = struct.unpack_from("<Q", extra_data, pos)[0]
            break
        offset += 4 + size
    return result


def _parse_zip_find_entry(url, size, name):
    """Locate a file entry in a remote ZIP archive using range requests."""
    tail_size = min(65557, size)
    tail = _read_range(url, size - tail_size, size - 1)
    eocd_pos = tail.rfind(b"PK\x05\x06")
    if eocd_pos < 0:
        raise RuntimeError("ZIP EOCD not found")

    cd_size = struct.unpack_from("<I", tail, eocd_pos + 12)[0]
    cd_offset = struct.unpack_from("<I", tail, eocd_pos + 16)[0]
    num_entries = struct.unpack_from("<H", tail, eocd_pos + 10)[0]

    if cd_offset == 0xFFFFFFFF or num_entries == 0xFFFF:
        loc_pos = tail.rfind(b"PK\x06\x07", 0, eocd_pos)
        if loc_pos >= 0:
            zip64_offset = struct.unpack_from("<Q", tail, loc_pos + 8)[0]
            zip64 = _read_range(url, zip64_offset, zip64_offset + 55)
            cd_size = struct.unpack_from("<Q", zip64, 40)[0]
            cd_offset = struct.unpack_from("<Q", zip64, 48)[0]

    if cd_offset + cd_size > size:
        raise RuntimeError("Central directory extends beyond file")

    central_directory = _read_range(url, cd_offset, cd_offset + cd_size - 1)
    entries = {}
    pos = 0
    while pos + 46 <= len(central_directory):
        if central_directory[pos:pos + 4] != b"PK\x01\x02":
            break
        compressed_size = struct.unpack_from(
            "<I", central_directory, pos + 20
        )[0]
        filename_size = struct.unpack_from("<H", central_directory, pos + 28)[0]
        extra_size = struct.unpack_from("<H", central_directory, pos + 30)[0]
        comment_size = struct.unpack_from("<H", central_directory, pos + 32)[0]
        local_offset = struct.unpack_from("<I", central_directory, pos + 42)[0]
        filename = central_directory[
            pos + 46:pos + 46 + filename_size
        ].decode("utf-8", errors="replace")

        zip64 = {}
        if compressed_size == 0xFFFFFFFF or local_offset == 0xFFFFFFFF:
            extra = central_directory[
                pos + 46 + filename_size:
                pos + 46 + filename_size + extra_size
            ]
            zip64 = _read_zip64_extra(extra)

        entries[filename] = {
            "localOffset": zip64.get("localOffset", local_offset),
            "compSize": zip64.get("compSize", compressed_size),
        }
        pos += 46 + filename_size + extra_size + comment_size

    if name not in entries:
        raise RuntimeError(f"'{name}' not found in ZIP")

    entry = entries[name]
    local_offset = entry["localOffset"]
    local_header = _read_range(url, local_offset, local_offset + 29)
    if local_header[0:4] != b"PK\x03\x04":
        raise RuntimeError(f"Invalid local header at offset {local_offset}")

    compression = struct.unpack_from("<H", local_header, 8)[0]
    compressed_size_local = struct.unpack_from("<I", local_header, 18)[0]
    filename_size = struct.unpack_from("<H", local_header, 26)[0]
    extra_size = struct.unpack_from("<H", local_header, 28)[0]
    data_offset = local_offset + 30 + filename_size + extra_size

    compressed_size = entry["compSize"]
    if compressed_size_local == 0xFFFFFFFF and compressed_size == 0:
        extra = _read_range(
            url,
            local_offset + 30 + filename_size,
            local_offset + 30 + filename_size + extra_size - 1,
        )
        compressed_size = _read_zip64_extra(extra).get("compSize", 0)

    return {
        "dataOffset": data_offset,
        "compressedSize": compressed_size,
        "compression": compression,
    }


def _parse_payload_manifest(url, payload_offset):
    """Parse the payload header (big endian) and return manifest + blob start."""
    header = _read_range(url, payload_offset, payload_offset + 23)
    if header[0:4] != b"CrAU":
        raise RuntimeError("Invalid payload.bin magic")

    manifest_size = struct.unpack_from(">Q", header, 12)[0]
    metadata_signature_size = struct.unpack_from(">I", header, 20)[0]
    manifest_start = payload_offset + 24
    manifest_data = _read_range(
        url, manifest_start, manifest_start + manifest_size - 1
    )

    manifest = update_metadata_pb2.DeltaArchiveManifest()
    manifest.ParseFromString(manifest_data)
    blob_data_start = manifest_start + manifest_size + metadata_signature_size
    return manifest, blob_data_start


def _decompress(data, operation_type):
    if operation_type == 0:  # REPLACE
        return data
    if operation_type == 1:  # REPLACE_BZ
        try:
            return bz2.decompress(data)
        except Exception:  # noqa: BLE001
            return None
    if operation_type == 8:  # REPLACE_XZ
        try:
            return lzma.decompress(data)
        except Exception:  # noqa: BLE001
            return None
    if operation_type == 10:  # BROTLI_BSDIFF (rarely used for xbl_config)
        try:
            import brotli

            return brotli.decompress(data)
        except Exception:  # noqa: BLE001
            return None
    logger.warning("Unsupported payload operation type: %s", operation_type)
    return None


def _extract_partition(url, partition, blob_data_start):
    chunks = []
    for operation in partition.operations:
        operation_type = operation.type
        if operation_type in (2, 3, 4, 5, 6, 7):
            continue
        if operation_type == 9:
            size = (
                sum(extent.num_blocks for extent in operation.dst_extents) * 4096
            )
            if size > 0:
                chunks.append(b"\x00" * size)
            continue
        if operation.data_length == 0:
            continue

        blob_start = blob_data_start + operation.data_offset
        blob_end = blob_start + operation.data_length - 1
        raw = _read_range(url, blob_start, blob_end)
        decompressed = _decompress(raw, operation_type)
        if decompressed is None:
            return None
        chunks.append(decompressed)

    if not chunks:
        return None
    return b"".join(chunks)


def check_arb(download_url):
    """Return ``{arb, major, minor, partition}`` for a firmware URL."""
    logger.info("ARB range check: %s", download_url)
    url = _resolve_if_needed(download_url)
    file_size = _get_file_size(url)

    payload_entry = _parse_zip_find_entry(url, file_size, "payload.bin")
    manifest, blob_data_start = _parse_payload_manifest(
        url, payload_entry["dataOffset"]
    )

    partitions = {}
    for partition in manifest.partitions:
        partitions.setdefault(partition.partition_name, partition)

    for name in PARTITION_CANDIDATES:
        partition = partitions.get(name)
        if partition is None:
            continue
        logger.info("Found candidate partition: %s", name)
        data = _extract_partition(url, partition, blob_data_start)
        if not data:
            logger.warning("Could not extract %s", name)
            continue
        if len(data) > MAX_PARTITION_SIZE:
            logger.warning("Partition %s too large: %s bytes", name, len(data))
            continue
        result = parse_elf64_arb(data)
        if result:
            result["partition"] = name
            return result

    raise RuntimeError("Could not determine ARB from any partition")
