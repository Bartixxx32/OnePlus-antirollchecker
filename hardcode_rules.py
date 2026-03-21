import re

def is_hardcode_protected(device_id: str, version: str) -> bool:
    """
    Checks if a specific firmware version is 'hardcode protected' 
    (i.e., known to have ARB regardless of undetectable values).
    """
    if device_id == "Nord CE 3 Lite" and version:
        # Match version strings like .1600 or .1611
        match = re.search(r'\.(\d{4,})(?:\(|$|_)', version)
        if match and int(match.group(1)) >= 1600:
            return True
    return False

def version_sort_key(version_str: str) -> tuple:
    """Extract numeric parts from version string for correct ordering."""
    if not version_str:
        return (0,)
    parts = re.findall(r'\d+', version_str)
    return tuple(int(p) for p in parts)

