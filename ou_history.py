#!/usr/bin/env python3
"""Historical Oxygen Updater helpers for North America firmware.

Oxygen Updater keeps an index of OnePlus/OPPO OTA packages.  Given the
internal OTA version (``ota_version`` from ``META-INF/com/android/metadata``)
of a package, ``updateData/{device}/{method}/{seed}`` returns the package
whose ``from_version`` matches that seed.  Walking those responses rebuilds
the North America update chain.

The chains are sealed with archived full packages from the community
``oneplus_archive`` repositories, which cover builds that are no longer
reachable through the update API.
"""

import logging
import re
import time

import requests

logger = logging.getLogger(__name__)

OU_API_URL = "https://oxygenupdater.com/api/v2.9"
OU_HEADERS = {
    "User-Agent": "Oxygen_updater_6.7.6",
    "Accept": "application/json",
}

# ARB device id / region -> Oxygen Updater numeric device id.
# Every tracked device that Oxygen Updater exposes with a North America
# variant must be listed here, otherwise the NA check silently disappears.
OU_NA_DEVICE_IDS = {
    "15": 814,
    "15R": 903,
    "13": 154,
    "13R": 158,
    "12": 130,
    "11": 93,
    "12R": 136,
    "10 Pro": 75,
    "10T": 87,
    "9 Pro": 57,
    "9": 56,
    "8T": 42,
    "8 Pro": 30,
    "8": 27,
    "Nord N30": 103,
    "Nord N20": 102,
    "Nord N200 5G": 67,
    "Pad 3": 625,
    "Pad 2": 150,
    "Open": 123,
}

# Internal OTA versions that start a walkable chain.  Each value is the
# ``ota_version`` of the oldest known full package for that device.
HISTORY_SEEDS = {
    "15": [
        "CPH2749_11.A.17_0170_202510192310",
        "CPH2749_11.A.25_0250_202512052342",
    ],
    "13": ["CPH2655_11.A.38_0380_202501160135"],
    "12": ["CPH2583_11.C.61_1610_202411230845"],
}

# Archived full packages (Google CDN links extracted from the release bodies
# of spike0en/oneplus_archive and imreallyliam/oneplus_archive).  These are
# needed for versions that the update API no longer resolves.
ARCHIVE_PACKAGES = {
    "15": [
        {
            "version": "CPH2749_16.0.2.401(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/d1f829f4ca9b09b78915c4a1eec6539a6b17fdbe.zip",
        },
        {
            "version": "CPH2749_16.0.3.503(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/76cc8d5124006f2491069b5cf581282cea59fb77.zip",
        },
    ],
    "13": [
        {
            "version": "CPH2655_15.0.0.405(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/791a2a5f55308aa4b577f05ec6ca2583151581b2.zip",
        },
        {
            "version": "CPH2655_15.0.0.832(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/cc05bc54d53631f2c946a9c6e02a3c6b6cb24c6b.zip",
        },
        {
            "version": "CPH2655_15.0.0.850(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/0cb08b94d8d2bc96c617c4ba7ba70aec63d5f6c5.zip",
        },
        {
            "version": "CPH2655_15.0.0.862(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/04031c2d566cae24ab5662e2217666aade935ffd.zip",
        },
        {
            "version": "CPH2655_15.0.0.864(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/9b7940fc45d00c423bcba0982436a90f1dc1ef6a.zip",
        },
        {
            "version": "CPH2655_16.0.0.213(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/d800bc5509d532471d4cadc207da43bce988963b.zip",
        },
        {
            "version": "CPH2655_16.0.1.304(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/659652189382037db75b31068fdd249a4503ee44.zip",
        },
        {
            "version": "CPH2655_16.0.2.403(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/e79a4f1c584373c0aadecc8b31b42db14f50673f.zip",
        },
    ],
    "12": [
        {
            "version": "CPH2583_15.0.0.305(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/8ddf7a13dc6b2b7d0e86996fabfbc98b19cdfe4e.zip",
        },
        {
            "version": "CPH2583_15.0.0.503(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/64bc2ad84808e3eb94d9f117e107eeefbeb32277.zip",
        },
        {
            "version": "CPH2583_15.0.0.510(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/964026d78502f50629c1f10572e156e287216734.zip",
        },
        {
            "version": "CPH2583_15.0.0.832(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/800185094c1f2f07a6fb067e50bd347ac561be03.zip",
        },
        {
            "version": "CPH2583_15.0.0.850(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/f11bdb93bf866da2fb594f42fa42881faabde2b3.zip",
        },
        {
            "version": "CPH2583_15.0.0.861(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/cb69b9c67a24d090035e61d6fe834e8feff23120.zip",
        },
        {
            "version": "CPH2583_15.0.0.863(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/2efcb0595e57b7b5affacc545b79d9cc3ce1665b.zip",
        },
        {
            "version": "CPH2583_16.0.0.202(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/fed2802d7b336a8a5d6cbd945bdde04d45d687ea.zip",
        },
        {
            "version": "CPH2583_16.0.3.500(EX01)",
            "url": "https://android.googleapis.com/packages/ota-api/package/5dbd9e29f6f38d4e572830c1739c94d7581daa7b.zip",
        },
    ],
}

# Known holes that cannot be reconstructed from the update API or the
# available archive mirrors (documented here to make the gaps explicit).
KNOWN_GAPS = {
    "15": ["CPH2749_16.0.0.205(EX01)"],
    "13": [],
    "12": [],
    "11": [],
    "12R": [],
    "15R": [],
    "13R": [],
}

# Devices without a walkable OU chain or archived packages, so only the
# latest package can be checked.  Listed explicitly for visibility.
LATEST_ONLY = {
    "15R", "13R", "11", "12R",
    "10 Pro", "10T", "9 Pro", "9", "8T", "8 Pro", "8",
    "Nord N30", "Nord N20", "Nord N200 5G",
    "Pad 3", "Pad 2", "Open",
}

_UPDATE_PARAMS = {
    "osType": "Stable",
    "fingerprint": "x",
    "oplusPipeline": "UNKNOWN",
    "oplusPipelineCode": "UNKNOWN",
    "oplusManifestHash": "UNKNOWN",
    "deviceMarketName": "x",
    "isEuBuild": "false",
    "appVersion": "6.7.6",
}


def version_sort_key(version):
    """Return a numeric sort key for a marketing firmware version."""
    match = re.search(r"(\d+(?:\.\d+)+)", version or "")
    if not match:
        return (0,)
    return tuple(int(part) for part in match.group(1).split("."))


def _request_json(url, params=None, session=None, retries=4):
    session = session or requests
    last_error = None
    for attempt in range(retries):
        try:
            response = session.get(
                url,
                params=params,
                headers=OU_HEADERS,
                timeout=(30, 120),
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # noqa: BLE001 - retry all transient errors
            last_error = exc
            if attempt < retries - 1:
                delay = min(2 ** attempt, 10)
                logger.warning(
                    "Oxygen Updater request failed (%s), retrying in %ss",
                    exc,
                    delay,
                )
                time.sleep(delay)
    logger.warning("Oxygen Updater request failed: %s", last_error)
    return None


def get_next_package(ou_device_id, seed, session=None):
    """Return the package that directly follows ``seed`` in the OU chain."""
    params = dict(_UPDATE_PARAMS)
    params["osVersion"] = seed
    data = _request_json(
        f"{OU_API_URL}/updateData/{ou_device_id}/1/{seed}",
        params=params,
        session=session,
    )
    if not data:
        return None
    version = data.get("version_number")
    url = data.get("download_url")
    if not version or not url:
        logger.info(
            "No newer package for OU device %s seed %s: %s",
            ou_device_id,
            seed,
            data.get("information"),
        )
        return None
    return {
        "version": version,
        "url": url,
        "ota_version": data.get("ota_version_number"),
        "from_version": seed,
        "size": data.get("download_size"),
        "md5": data.get("md5sum"),
    }


def walk_chain(ou_device_id, seed, session=None, max_steps=64):
    """Walk ``updateData`` until the newest reachable package is found."""
    packages = []
    seen_seeds = set()
    current = seed

    while current and current not in seen_seeds and len(packages) < max_steps:
        seen_seeds.add(current)
        package = get_next_package(ou_device_id, current, session=session)
        if not package:
            break
        packages.append(package)
        current = package.get("ota_version")

    return packages


def get_latest_package(ou_device_id, session=None):
    """Return the newest package from the incremental channel."""
    data = _request_json(
        f"{OU_API_URL}/mostRecentUpdateData/{ou_device_id}/1",
        session=session,
    )
    if not data or not data.get("version_number") or not data.get("download_url"):
        return None
    return {
        "version": data["version_number"],
        "url": data["download_url"],
        "ota_version": data.get("ota_version_number"),
        "from_version": None,
        "size": data.get("download_size"),
        "md5": data.get("md5sum"),
    }


def get_history_packages(device_id, session=None):
    """Return all known NA packages for a device, deduplicated by version."""
    ou_device_id = OU_NA_DEVICE_IDS.get(device_id)
    if not ou_device_id:
        return []

    session = session or requests.Session()
    packages = {}

    for seed in HISTORY_SEEDS.get(device_id, []):
        for package in walk_chain(ou_device_id, seed, session=session):
            packages.setdefault(package["version"], package)

    for package in ARCHIVE_PACKAGES.get(device_id, []):
        packages.setdefault(
            package["version"],
            {
                "version": package["version"],
                "url": package["url"],
                "ota_version": None,
                "from_version": None,
                "size": None,
                "md5": None,
            },
        )

    latest = get_latest_package(ou_device_id, session=session)
    if latest:
        packages.setdefault(latest["version"], latest)

    return list(packages.values())


def get_na_packages(device_id, session=None):
    """Return the NA package list sorted newest first.

    Devices without archived history (15R/13R/11/12R) only contribute their
    current latest package.
    """
    packages = get_history_packages(device_id, session=session)
    packages.sort(key=lambda p: version_sort_key(p["version"]), reverse=True)
    return packages


def build_ou_matrix_entries(
    device_id,
    device_name,
    region,
    packages,
    max_versions,
    select_versions,
):
    """Build backfill matrix entries from OU packages."""
    entries = []
    for package in select_versions(packages, max_versions):
        entries.append(
            {
                "device": device_id,
                "variant": region,
                "device_short": device_id,
                "device_name": device_name,
                "version": package["version"],
                "source": "ou_url",
                "url": package["url"],
                "md5": package.get("md5"),
                "ou_device_id": OU_NA_DEVICE_IDS.get(device_id),
                "ota_version": package.get("ota_version"),
            }
        )
    return entries
