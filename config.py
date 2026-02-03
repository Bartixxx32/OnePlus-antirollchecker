"""
Shared configuration and constants for OnePlus ARB Checker.
"""

from typing import Dict, TypedDict

# Constants
BASE_URL = "https://roms.danielspringer.at/index.php?view=ota"
OOS_API_URL = "https://oosdownloader-gui.fly.dev/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HISTORY_DIR = "data/history"

# Type definitions
class DeviceModels(TypedDict, total=False):
    GLO: str
    EU: str
    IN: str
    CN: str

class DeviceMeta(TypedDict):
    name: str
    models: DeviceModels

# Device order for README and Website (OnePlus newest first, then Oppo newest first)
DEVICE_ORDER = [
    # OnePlus
    "15R", "Ace 6T", "15", "Pad 3", "Pad 2 Pro", "Ace 5 Ultimate", 
    "Ace 5 Pro", "Ace 5", "13", "Pad 2", "12", "12R", "Open", 
    "11", "11R", "10 Pro", "10T", "10R", "9 Pro", "9RT", "9", "9R",
    # Oppo
    "Find X8 Ultra", "Find N5", "Find N3", "Find X5 Pro", "Find X5"
]

# Device Metadata
# Used for display names, model numbers, and mapping internal IDs to names
DEVICE_METADATA: Dict[str, DeviceMeta] = {
    "15": {
        "name": "OnePlus 15",
        "models": {
            "GLO": "CPH2747",
            "EU": "CPH2747",
            "IN": "CPH2745",
            "CN": "PLK110"
        }
    },
    "15R": {
        "name": "OnePlus 15R", 
        "models": {
            "GLO": "CPH2741",
            "EU": "CPH2741",
            "IN": "CPH2741"
        }
    },
    "13": {
        "name": "OnePlus 13",
        "models": {
            "GLO": "CPH2649",
            "EU": "CPH2649",
            "IN": "CPH2649",
            "NA": "CPH2655",
            "CN": "PJZ110"
        }
    },
    "12": {
        "name": "OnePlus 12",
        "models": {
            "GLO": "CPH2573", 
            "EU": "CPH2573", 
            "IN": "CPH2573", 
            "NA": "CPH2583",
            "CN": "PJD110"
        }
    },
    "12R": {
        "name": "OnePlus 12R",
        "models": {
            "GLO": "CPH2585",
            "EU": "CPH2609",
            "IN": "CPH2585",
            "NA": "CPH2611"
        }
    },
    "11": {
        "name": "OnePlus 11",
        "models": {
            "GLO": "CPH2449",
            "EU": "CPH2449",
            "IN": "CPH2447",
            "NA": "CPH2451"
        }
    },
    "11R": {
        "name": "OnePlus 11R",
        "models": {
            "IN": "CPH2487"
        }
    },
    "10 Pro": {
        "name": "OnePlus 10 Pro",
        "models": {
            "GLO": "NE2215",
            "EU": "NE2213",
            "IN": "NE2211",
            "NA": "NE2215",
            "CN": "NE2210"
        }
    },
    "10T": {
        "name": "OnePlus 10T",
        "models": {
            "GLO": "CPH2417",
            "EU": "CPH2415",
            "IN": "CPH2413",
            "NA": "CPH2417"
        }
    },
    "10R": {
        "name": "OnePlus 10R",
        "models": {
            "IN": "CPH2423"
        }
    },
    "9 Pro": {
        "name": "OnePlus 9 Pro",
        "models": {
            "NA": "LE2125",
            "EU": "LE2123",
            "IN": "LE2121"
        }
    },
    "9": {
        "name": "OnePlus 9",
        "models": {
            "NA": "LE2115",
            "EU": "LE2113",
            "IN": "LE2111"
        }
    },
    "9RT": {
        "name": "OnePlus 9RT",
        "models": {
            "IN": "MT2111"
        }
    },
    "9R": {
        "name": "OnePlus 9R",
        "models": {
            "IN": "LE2101"
        }
    },
    "Ace 6T": {
        "name": "OnePlus Ace 6T",
        "models": {
            "CN": "PLR110"
        }
    },
    "Ace 5": {
        "name": "OnePlus Ace 5",
        "models": {
            "CN": "PKG110"
        }
    },
    "Ace 5 Pro": {
        "name": "OnePlus Ace 5 Pro",
        "models": {
            "CN": "PKR110"
        }
    },
    "Ace 5 Ultimate": {
        "name": "OnePlus Ace 5 Ultimate",
        "models": {
            "CN": "PLC110"
        }
    },
    "Pad 2 Pro": {
        "name": "OnePlus Pad 2 Pro",
        "models": {
            "CN": "OPD2413"
        }
    },

# ... skipping Pad 3/2 section ...

    "Open": {
        "name": "OnePlus Open",
        "models": {
            "EU": "CPH2551",
            "IN": "CPH2551",
            "NA": "CPH2551"
        }
    },

    "Find X5 Pro": {
        "name": "Oppo Find X5 Pro",
        "models": {
            "EU": "CPH2305",
            "EG": "CPH2305",
            "OCA": "CPH2305",
            "SG": "CPH2305",
            "TW": "CPH2305",
            "CN": "PFEM10"
        }
    },
    "Find X5": {
        "name": "Oppo Find X5",
        "models": {
            "GLO": "CPH2307",
            "EU": "CPH2307",
            "IN": "CPH2307",
            "CN": "PFFM10"
        }
    },

    "Find X8 Ultra": {
        "name": "Oppo Find X8 Ultra",
        "models": {
            "CN": "PKJ110"
        }
    },
    "Find N5": {
        "name": "Oppo Find N5",
        "models": {
            "SG": "CPH2671",
            "MY": "CPH2671",
            "CN": "PKV110"
        }
    },
    "Pad 3": {
        "name": "OnePlus Pad 3",
        "models": {
            "GLO": "OPD2415",
            "EU": "OPD2415",
            "IN": "OPD2415",
            "NA": "OPD2415"
        }
    },
    "Pad 2": {
        "name": "OnePlus Pad 2",
        "models": {
            "GLO": "OPD2403",
            "EU": "OPD2403",
            "IN": "OPD2403"
        }
    },


    "Find N3": {
        "name": "Oppo Find N3",
        "models": {
            "ID": "CPH2499",
            "IN": "CPH2519",
            "MY": "CPH2499",
            "OCA": "CPH2499",
            "SG": "CPH2499",
            "TH": "CPH2499",
            "TW": "CPH2499",
            "VN": "CPH2499"
        }
    }
}

# Mapping for fetching firmware (roms.danielspringer.at expects these names)
SPRING_MAPPING = {
    "oneplus_15": "OP 15",
    "oneplus_15r": "OP 15R",
    "oneplus_11": "OP 11",
    "oneplus_11r": "OP 11R",
    "oneplus_10_pro": "OP 10 PRO",
    "oneplus_13": "OP 13",
    "oneplus_12": "OP 12",
    "oneplus_12r": "OP ACE 3",
    "oneplus_ace_6t": "OP ACE 6T",
    "oneplus_ace_5": "OP ACE 5",
    "oneplus_ace_5_pro": "OP ACE 5 PRO",
    "oneplus_ace_5_ultimate": "OP ACE 5 ULTRA",
    "oneplus_pad2_pro": "OP PAD2 PRO",
    "oneplus_pad_3": "OP PAD3",
    "oneplus_pad_2": "OP PAD2",
    "oneplus_open": "OP OPEN",
    "oppo_find_x8_ultra": "OPPO FIND X8 ULTRA",
    "oppo_find_n5": "OPPO FIND N5",
    "oppo_find_x5_pro": "OPPO FIND X5 PRO",
    "oppo_find_x5": "OPPO FIND X5"
}



# Mapping for OOS Downloader API (oosdownloader-gui.fly.dev)
# It seems to use snake_case ids directly, but let's be explicit if needed.
# If keys match the input 'oneplus_XX', we might just pass them through.
# But for consistency, let's keep them here.
OOS_MAPPING = {
    "15": "oneplus_15",
    "15R": "oneplus_15r",
    "13": "oneplus_13",
    "12": "oneplus_12",
    "12R": "oneplus_12r",
    "11": "oneplus_11",
    "11R": "oneplus_11r",
    "10 Pro": "oneplus_10_pro",
    "10T": "oneplus_10t",
    "10R": "oneplus_10r_80w",
    "9 Pro": "oneplus_9_pro",
    "9": "oneplus_9",
    "9RT": "oneplus_9rt",
    "9R": "oneplus_9r",
    "9R": "oneplus_9r",
    "Ace 6T": "oneplus_ace_6t",
    "Ace 5": "oneplus_ace_5",
    "Ace 5 Pro": "oneplus_ace_5_pro", 
    "Ace 5 Ultimate": "oneplus_ace_5_ultimate",
    "Pad 2 Pro": "oneplus_pad2_pro",
    "Pad 3": "oneplus_pad_3",
    "Pad 2": "oneplus_pad_2",
    "Find X8 Ultra": "oppo_find_x8_ultra",
    "Find N5": "oppo_find_n5",
    "Find N3": "oppo_find_n3",
    "Find X5 Pro": "oppo_find_x5_pro",
    "Find X5": "oppo_find_x5",
    "Open": "oneplus_open"
}



def get_display_name(device_id: str) -> str:
    """Get the human-readable display name for a device ID."""
    return DEVICE_METADATA.get(device_id, {}).get("name", f"OnePlus {device_id}")

def get_model_number(device_id: str, region: str) -> str:
    """Get the model number for a specific device and region."""
    return DEVICE_METADATA.get(device_id, {}).get("models", {}).get(region, "Unknown")
