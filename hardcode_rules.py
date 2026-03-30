import re

def is_hardcode_protected(device_id: str, version: str) -> bool:
    """
    Checks if a specific firmware version is 'hardcode protected'
    (i.e., known to have ARB regardless of undetectable values).
    """
    # Nord CE 3 Lite - build numbers >= 1600
    if device_id == "oneplus_nord_ce_3_lite" and version:
        match = re.search(r'\.(\d{4,})(?:\(|$|_)', version)
        if match and int(match.group(1)) >= 1600:
            return True
    
    # Nord CE 3 (non-lite) - build numbers >= 1600
    if device_id == "oneplus_nord_ce_3" and version:
        match = re.search(r'\.(\d{4,})(?:\(|$|_)', version)
        if match and int(match.group(1)) >= 1600:
            return True

    # Nord CE 4 Lite - build numbers > 303
    if device_id == "oneplus_nord_ce_4_lite" and version:
        match = re.search(r'\.(\d+)(?:\(|$|_)', version)
        if match and int(match.group(1)) >= 303:
            return True
    
    return False

def version_sort_key(version_str: str) -> tuple:
    """
    Extract numeric parts from version string for correct ordering.
    Note: Keep this in sync with versionSortKey() in templates/index.html.
    """
    if not version_str:
        return (0,)
    parts = re.findall(r'\d+', version_str)
    return tuple(int(p) for p in parts)

