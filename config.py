"""
Centralized configuration for OnePlus Anti-Rollback Checker.
"""

DEVICE_CONFIG = {
    "15": {
        "name": "OnePlus 15",
        "short_name": "OP 15",
        "fetch_id": "oneplus_15",
        "models": {
            "GLO": "CPH2747",
            "EU": "CPH2747",
            "IN": "CPH2745",
            "CN": "PLK110"
        }
    },
    "15R": {
        "name": "OnePlus 15R",
        "short_name": "OP 15R",
        "fetch_id": "oneplus_15r",
        "models": {
            "GLO": "CPH2741",
            "EU": "CPH2741",
            "IN": "CPH2741"
        }
    },
    "13": {
        "name": "OnePlus 13",
        "short_name": "OP 13",
        "fetch_id": "oneplus_13",
        "models": {
            "GLO": "CPH2649",
            "EU": "CPH2649",
            "IN": "CPH2649",
            "CN": "PJZ110"
        }
    },
    "12": {
        "name": "OnePlus 12",
        "short_name": "OP 12",
        "fetch_id": "oneplus_12",
        "models": {
            "GLO": "CPH2573",
            "EU": "CPH2573",
            "IN": "CPH2573",
            "CN": "PJD110"
        }
    }
}

# Ordered list of device IDs for README generation
DEVICE_ORDER = ["15", "15R", "13", "12"]

def get_device_map_for_fetch():
    """Returns mapping for fetch_firmware.py"""
    return {
        cfg["fetch_id"]: cfg["short_name"]
        for cfg in DEVICE_CONFIG.values()
        if "fetch_id" in cfg
    }

def get_device_metadata():
    """Returns metadata for update_history.py"""
    return {
        k: {"name": v["name"], "models": v["models"]}
        for k, v in DEVICE_CONFIG.items()
    }

def get_device_short_name_map():
    """Returns mapping for parse_ini.py"""
    return {
        k: v["short_name"]
        for k, v in DEVICE_CONFIG.items()
    }
