"""
Central configuration for OnePlus ARB Checker.
"""

REGIONS = {
    'GLO': 'Global',
    'EU': 'Europe',
    'IN': 'India',
    'CN': 'China'
}

# Master device data
# Key: short code (used in history filenames and update_history.py args)
DEVICES = {
    "15": {
        "name": "OnePlus 15",
        "short_name": "OP 15",
        "id": "oneplus_15",  # Used in fetch_firmware.py and GitHub Actions matrix
        "models": {"GLO": "CPH2747", "EU": "CPH2747", "IN": "CPH2745", "CN": "PLK110"}
    },
    "15R": {
        "name": "OnePlus 15R",
        "short_name": "OP 15R",
        "id": "oneplus_15r",
        "models": {"GLO": "CPH2741", "EU": "CPH2741", "IN": "CPH2741"}
    },
    "13": {
        "name": "OnePlus 13",
        "short_name": "OP 13",
        "id": "oneplus_13",
        "models": {"GLO": "CPH2649", "EU": "CPH2649", "IN": "CPH2649", "CN": "PJZ110"}
    },
    "12": {
        "name": "OnePlus 12",
        "short_name": "OP 12",
        "id": "oneplus_12",
        "models": {"GLO": "CPH2573", "EU": "CPH2573", "IN": "CPH2573", "CN": "PJD110"}
    }
}

# Helper mappings for ease of use

# ID to Short Name (e.g. "oneplus_15" -> "OP 15")
# Used in fetch_firmware.py
DEVICE_ID_TO_NAME = {d['id']: d['short_name'] for d in DEVICES.values()}

# Short Code to Short Name (e.g. "15" -> "OP 15")
# Used in parse_ini.py
DEVICE_SHORT_TO_NAME = {k: v['short_name'] for k, v in DEVICES.items()}

# Ordered list of (short_code, full_name) for README generation
DEVICE_ORDER_LIST = [(k, v['name']) for k, v in DEVICES.items()]
