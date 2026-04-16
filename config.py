"""
Shared configuration and constants for OnePlus ARB Checker.
"""

from typing import Dict, TypedDict

# Constants
SPRINGER_API_URL = "https://roms.danielspringer.at/index.php?view=ota"
OOS_API_URL = "https://oosdownloader-gui.fly.dev/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HISTORY_DIR = "data/history"
GOOGLE_ANALYTICS_ID = "G-7B8F6LHTVF"

# Region Mapping (used for README and Website)
REGION_MAPPING = {
    'GLO': 'Global',
    'GLB': 'Global',
    'IN': 'India',
    'EU': 'Europe',
    'EEA': 'Europe',
    'NA': 'North America',
    'US': 'United States',
    'CN': 'China',
    'SG': 'Singapore',
    'MY': 'Malaysia',
    'TW': 'Taiwan',
    'ID': 'Indonesia',
    'VN': 'Vietnam',
    'APC': 'Asia Pacific',
    'OCA': 'Oceania',
    'EG': 'Egypt',
    'SA': 'Saudi Arabia',
    'MX': 'Mexico',
    'VISIBLE': 'Visible USA',
    'TH': 'Thailand',
    'PH': 'Philippines',
    'MEA': 'Middle East'
}

# Type definitions
class DeviceModels(TypedDict, total=False):
    GLO: str
    EU: str
    IN: str
    CN: str

class DeviceMeta(TypedDict):
    name: str
    models: DeviceModels

# Device order for README and Website (Flagships -> Open -> Nords -> Ace -> Pads -> Oppo)
DEVICE_ORDER = [
    # Flagships (New)
    "15", "15R", 
    "13", "13R", "13T", "13s",
    "Open",
    "12", "12R", 
    "11", "11R", 
    "10 Pro", "10T",
    "9 Pro", "9", "9RT", "9R",
    
    # Flagships (Legacy)
    "8T", "8 Pro", "8",
    "7T Pro", "7T", "7 Pro", "7",

    # Nords
    "Nord 6",
    "Nord 5",
    "Nord 4", 
    "Nord CE 4 Lite", "Nord CE 4", "Nord CE 3",
    "Nord CE 3 Lite", "Nord CE 2 Lite",
    "Nord N30", "Nord N20",
    "Nord 1", "Nord N200 5G",
    
    # China Exclusives (Ace)
    "Ace 6T", 
    "Ace 6",
    "Ace 5 Pro", "Ace 5", 
    "Ace 3 Pro", "Ace 3V", "Ace 3",

    # Pads
    "Pad 3", "Pad 2 Pro", "Pad 2", 
    
    # Oppo
    "Reno10 Pro",
    "Find X8 Ultra", "Find N5", "Find N3", "Find X5 Pro", "Find X5", "Find X3 Pro"
]

# Device Metadata
# Used for display names, model numbers, and mapping internal IDs to names
DEVICE_METADATA: Dict[str, DeviceMeta] = {
    # ... existing 15-9 ...
    "15": {
        "name": "OnePlus 15",
        "models": {
            "GLO": "CPH2747",
            "EU": "CPH2747",
            "IN": "CPH2745",
            "CN": "PLK110"
        },
    },
    "15R": {
        "name": "OnePlus 15R", 
        "models": {
            "GLO": "CPH2769",
            "EU": "CPH2769",
            "IN": "CPH2767"
        },
    },
    "13": {
        "name": "OnePlus 13",
        "models": {
            "GLO": "CPH2653",
            "EU": "CPH2653",
            "IN": "CPH2649",
            "NA": "CPH2655",
            "CN": "PJZ110"
        },
    },
    "13R": {
        "name": "OnePlus 13R",
        "models": {
            "GLO": "CPH2645",
            "EU": "CPH2645",
            "IN": "CPH2691"
        },
    },
    "13T": {
        "name": "OnePlus 13T",
        "models": {
            "CN": "PKX110"
        },
    },
    "13s": {
        "name": "OnePlus 13s",
        "models": {
            "IN": "CPH2723"
        },
    },
    "12": {
        "name": "OnePlus 12",
        "models": {
            "GLO": "CPH2581", 
            "EU": "CPH2581", 
            "IN": "CPH2573", 
            "NA": "CPH2583",
            "CN": "PJD110"
        },
    },
    "12R": {
        "name": "OnePlus 12R",
        "models": {
            "GLO": "CPH2609",
            "EU": "CPH2609",
            "IN": "CPH2585",
            "NA": "CPH2611"
        },
    },
    "11": {
        "name": "OnePlus 11",
        "models": {
            "GLO": "CPH2449",
            "EU": "CPH2449",
            "IN": "CPH2447",
            "NA": "CPH2451"
        },
    },
    "11R": {
        "name": "OnePlus 11R",
        "models": {
            "IN": "CPH2487"
        },
    },
    "10 Pro": {
        "name": "OnePlus 10 Pro",
        "models": {
            "GLO": "NE2213",
            "EU": "NE2213",
            "IN": "NE2211",
            "NA": "NE2215",
            "CN": "NE2210"
        },
    },
    "10T": {
        "name": "OnePlus 10T",
        "models": {
            "GLO": "CPH2415",
            "EU": "CPH2415",
            "IN": "CPH2413",
            "NA": "CPH2417"
        },
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

    # Legacy Series 8
    "8T": {
        "name": "OnePlus 8T",
        "models": {
            "EU": "KB2003",
            "IN": "KB2001",
            "NA": "KB2005"
        },
    },
    "8 Pro": {
        "name": "OnePlus 8 Pro",
        "models": {
            "EU": "IN2023",
            "IN": "IN2021",
            "NA": "IN2025"
        },
    },
    "8": {
        "name": "OnePlus 8",
        "models": {
            "EU": "IN2013",
            "IN": "IN2011",
            "NA": "IN2015"
        },
    },

    # Legacy Series 7
    "7T Pro": {
        "name": "OnePlus 7T Pro",
        "models": {
            "GLO": "HD1917",
            "EU": "HD1913",
            "IN": "HD1911"
        },
    },
    "7T": {
        "name": "OnePlus 7T",
        "models": {
            "GLO": "HD1905",
            "EU": "HD1903",
            "IN": "HD1901"
        },
    },
    "7 Pro": {
        "name": "OnePlus 7 Pro",
        "models": {
            "GLO": "GM1917",
            "EU": "GM1913",
            "IN": "GM1911"
        },
    },
    "7": {
        "name": "OnePlus 7",
        "models": {
            "GLO": "GM1905",
            "EU": "GM1903",
            "IN": "GM1901"
        },
    },

    # Nords
    "Nord 6": {
        "name": "OnePlus Nord 6",
        "models": {
            "GLO": "CPH2795",
            "IN": "CPH2793"
        },
    },
    "Nord 5": {
        "name": "OnePlus Nord 5",
        "models": {
            "GLO": "CPH2709",
            "EU": "CPH2709",
            "IN": "CPH2707"
        },
    },
    "Nord 4": {
        "name": "OnePlus Nord 4",
        "models": {
            "GLO": "CPH2663",
            "EU": "CPH2663",
            "IN": "CPH2661"
        },
    },
    "Nord 1": {
        "name": "OnePlus Nord",
        "models": {
            "EU": "Nord_EEA",
            "IN": "AC2001"
        },
    },
    "Nord N200 5G": {
        "name": "OnePlus Nord N200 5G",
        "models": {
            "NA": "DE2117"
        },
    },
    "Nord N30": {
        "name": "OnePlus Nord N30",
        "models": {
            "NA": "CPH2513"
        },
    },
    "Nord N20": {
        "name": "OnePlus Nord N20",
        "models": {
            "NA": "CPH2459"
        },
    },
    "Nord CE 3 Lite": {
        "name": "OnePlus Nord CE 3 Lite",
        "models": {
            "EU": "CPH2465EEA",
            "GLO": "CPH2465",
            "IN": "CPH2467"
        },
    },
    "Nord CE 4 Lite": {
        "name": "OnePlus Nord CE 4 Lite",
        "models": {
            "EU": "CPH2619",
            "GLO": "CPH2619",
            "IN": "CPH2619"
        },
    },
    "Nord CE 4": {
        "name": "OnePlus Nord CE 4",
        "models": {
            "IN": "CPH2613"
        },
    },
    "Nord CE 3": {
        "name": "OnePlus Nord CE 3",
        "models": {
            "IN": "CPH2567"
        },
    },
    "Nord CE 2 Lite": {
        "name": "OnePlus Nord CE 2 Lite",
        "models": {
            "EU": "CPH2409EEA",
            "GLO": "CPH2409",
            "IN": "CPH2381"
        },
    },

    # China Exclusives (Ace)
    "Ace 6T": {
        "name": "OnePlus Ace 6T",
        "models": {
            "CN": "PLR110"
        },
    },
    "Ace 6": {
        "name": "OnePlus Ace 6",
        "models": {
            "CN": "PLQ110"
        },
    },
    "Ace 5": {
        "name": "OnePlus Ace 5",
        "models": {
            "CN": "PKG110"
        },
    },
    "Ace 5 Pro": {
        "name": "OnePlus Ace 5 Pro",
        "models": {
            "CN": "PKR110"
        },
    },
    "Ace 3 Pro": {
        "name": "OnePlus Ace 3 Pro",
        "models": {
            "CN": "PJX110"
        },
    },
    "Ace 3V": {
        "name": "OnePlus Ace 3V",
        "models": {
            "CN": "PJF110"
        },
    },
    "Ace 3": {
        "name": "OnePlus Ace 3",
        "models": {
            "CN": "PJE110"
        },
    },



    "Pad 3": {
        "name": "OnePlus Pad 3",
        "models": {
            "GLO": "OPD2415",
            "EU": "OPD2415",
            "IN": "OPD2415",
            "NA": "OPD2415"
        },
    },
    "Pad 2": {
        "name": "OnePlus Pad 2",
        "models": {
            "GLO": "OPD2403",
            "EU": "OPD2403",
            "IN": "OPD2403"
        },
    },
    "Pad 2 Pro": {
        "name": "OnePlus Pad 2 Pro",
        "models": {
            "CN": "OPD2413"
        },
    },

    "Open": {
        "name": "OnePlus Open",
        "models": {
            "EU": "CPH2551",
            "IN": "CPH2551",
            "NA": "CPH2551"
        },
    },

    "Find X5 Pro": {
        "name": "Oppo Find X5 Pro",
        "models": {
            "EU": "CPH2305",
            "EG": "CPH2305",
            "OCA": "CPH2305",
            "SG": "CPH2305",
            "TW": "CPH2305"
        },
    },
    "Find X5": {
        "name": "Oppo Find X5",
        "models": {
            "EU": "CPH2307",
            "EG": "CPH2307",
            "OCA": "CPH2307",
            "SA": "CPH2307"
        },
    },

    "Reno10 Pro": {
        "name": "Oppo Reno10 Pro",
        "models": {
            "EEA": "CPH2525EEA",
            "APC": "CPH2525",
            "IN": "CPH2525IN",
            "ID": "CPH2525ID",
            "MEA": "CPH2525MEA",
            "MY": "CPH2525MY",
            "OCA": "CPH2525OCA",
            "PH": "CPH2525PH",
            "SA": "CPH2525SA",
            "SG": "CPH2525SG",
            "TH": "CPH2525TH",
            "TW": "CPH2525TW",
            "VN": "CPH2525VN"
        },
    },

    "Find X8 Ultra": {
        "name": "Oppo Find X8 Ultra",
        "models": {
            "CN": "PKJ110"
        },
    },
    "Find N5": {
        "name": "Oppo Find N5",
        "models": {
            "SG": "CPH2671",
            "MY": "CPH2671",
            "APC": "CPH2671",
            "ID": "CPH2671",
            "MX": "CPH2671",
            "TH": "CPH2671",
            "CN": "PKV110"
        },
    },
    "Find N3": {
        "name": "Oppo Find N3",
        "models": {
            "ID": "CPH2499",
            "MY": "CPH2499",
            "OCA": "CPH2499",
            "SG": "CPH2499",
            "TH": "CPH2499",
            "TW": "CPH2499",
            "VN": "CPH2499"
        },
    },
    "Find X3 Pro": {
        "name": "Oppo Find X3 Pro",
        "models": {
            "EU": "CPH2173",
            "SG": "CPH2173",
            "TW": "CPH2173"
        },
    }
}

# Mapping for fetching firmware (roms.danielspringer.at expects these names)
SPRING_MAPPING = {
    # Existing
    "oneplus_15": "OP 15",
    "oneplus_15r": "OP 15R",
    "oneplus_11": "OP 11",
    "oneplus_11r": "OP 11R",
    "oneplus_10_pro": "OP 10 PRO",
    "oneplus_13": "OP 13",
    "oneplus_13r": "OP 13R",
    "oneplus_13t": "OP 13T",
    "oneplus_13s": "OP 13S",
    "oneplus_12": "OP 12",
    "oneplus_12r": "OP ACE 3",
    "oneplus_ace_6t": "OP ACE 6T",
    "oneplus_ace_6": "OP ACE 6",
    "oneplus_ace_5": "OP ACE 5",
    "oneplus_ace_5_pro": "OP ACE 5 PRO",
    "oneplus_pad2_pro": "OP PAD2 PRO",
    "oneplus_pad_3": "OP PAD3",
    "oneplus_pad_2": "OP PAD2",
    "oneplus_open": "OP OPEN",
    "oneplus_nord_6": "OP NORD 6",
    "oneplus_nord_5": "OP NORD 5",
    "oneplus_nord_4": "OP NORD 4",
    # Legacy
    "oneplus_8t": "OP 8T",
    "oneplus_8_pro": "OP 8 PRO",
    "oneplus_8": "OP 8",
    "oneplus_7t_pro": "OP 7T PRO",
    "oneplus_7t": "OP 7T",
    "oneplus_7_pro": "OP 7 PRO",
    "oneplus_7": "OP 7",
    "oneplus_nord_1": "OP NORD",
    "oneplus_nord_ce_4_lite": "OP NORD CE 4 LITE",
    "oneplus_nord_ce_4": "OP NORD CE 4",
    "oneplus_nord_ce_3": "OP NORD CE 3",
    # Ace
    "oneplus_ace_3_pro": "OP ACE 3 PRO",
    "oneplus_ace_3v": "OP ACE 3V",
    "oneplus_ace_3": "OP ACE 3",

    # Oppo
    "oppo_find_x8_ultra": "OPPO FIND X8 ULTRA",
    "oppo_find_n5": "OPPO FIND N5",
    "oppo_find_x5_pro": "OPPO FIND X5 PRO",
    "oppo_find_x5": "OPPO FIND X5",
    "oppo_find_x3_pro": "OPPO FIND X3 PRO"
}

# Mapping for OOS Downloader API (oosdownloader-gui.fly.dev)
OOS_MAPPING = {
    "15": "oneplus_15",
    "15R": "oneplus_15r",
    "13": "oneplus_13",
    "13R": "oneplus_13r",
    "13T": "oneplus_13t",
    "13s": "oneplus_13s",
    "12": "oneplus_12",
    "12R": "oneplus_12r",
    "11": "oneplus_11",
    "11R": "oneplus_11r",
    "10 Pro": "oneplus_10_pro",
    "10T": "oneplus_10t",
    "9 Pro": "oneplus_9_pro",
    "9": "oneplus_9",
    "9RT": "oneplus_9rt",
    "9R": "oneplus_9r",
    "Open": "oneplus_open",
    # Legacy
    "8T": "oneplus_8t",
    "8 Pro": "oneplus_8_pro",
    "8": "oneplus_8",
    "7T Pro": "oneplus_7t_pro",
    "7T": "oneplus_7t",
    "7 Pro": "oneplus_7_pro",
    "7": "oneplus_7",
    "Nord 1": "oneplus_nord",
    # Nords
    "Nord 6": "oneplus_nord_6",
    "Nord 5": "oneplus_nord_5",
    "Nord 4": "oneplus_nord_4",
    "Nord N30": "oneplus_nord_n30",
    "Nord N20": "oneplus_nord_n20",
    "Nord N200 5G": "oneplus_nord_n200",
    "Nord CE 4 Lite": "oneplus_nord_ce_4_lite",
    "Nord CE 4": "oneplus_nord_ce_4",
    "Nord CE 3": "oneplus_nord_ce_3",
    "Nord CE 3 Lite": "oneplus_nord_ce_3_lite",
    "Nord CE 2 Lite": "oneplus_nord_ce_2_lite",
    # Ace
    "Ace 6T": "oneplus_ace_6t",
    "Ace 6": "oneplus_ace_6",
    "Ace 5": "oneplus_ace_5",
    "Ace 5 Pro": "oneplus_ace_5_pro", 
    "Ace 3 Pro": "oneplus_ace_3_pro",
    "Ace 3V": "oneplus_ace_3v",
    "Ace 3": "oneplus_ace_3",

    # Pads
    "Pad 2 Pro": "oneplus_pad2_pro",
    "Pad 3": "oneplus_pad_3",
    "Pad 2": "oneplus_pad_2",
    # Oppo
    "Find X8 Ultra": "oppo_find_x8_ultra",
    "Find N5": "oppo_find_n5",
    "Find N3": "oppo_find_n3",
    "Find X5 Pro": "oppo_find_x5_pro",
    "Find X5": "oppo_find_x5",
    "Find X3 Pro": "oppo_find_x3_pro",
    "Reno10 Pro": "oppo_reno10_pro",
}


# Untracked devices provided by user to include in Risk Section



def get_display_name(device_id: str) -> str:
    """Get the human-readable display name for a device ID."""
    return DEVICE_METADATA.get(device_id, {}).get("name", f"OnePlus {device_id}")

def get_model_number(device_id: str, region: str) -> str:
    """Get the model number for a specific device and region."""
    return DEVICE_METADATA.get(device_id, {}).get("models", {}).get(region, "Unknown")
