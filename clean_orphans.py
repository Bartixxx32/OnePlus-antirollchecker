import json
import logging
from pathlib import Path
from config import DEVICE_METADATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_orphans():
    """
    Scans the data/history directory for JSON artifacts belonging to devices 
    that have been removed from config.DEVICE_METADATA and permanently deletes them.
    """
    history_dir = Path("data/history")
    active_device_ids = set(DEVICE_METADATA.keys())
    count = 0

    if not history_dir.exists():
        logger.warning(f"History directory not found: {history_dir}")
        return

    for f in history_dir.glob("*.json"):
        if f.name == "database.json":
            continue
            
        try:
            # Derive device_id from filename pattern: {device_id}_{region}.json
            # This is much faster than loading the full JSON blob.
            device_id = f.stem.rsplit('_', 1)[0]
            
            if device_id not in active_device_ids:
                logger.info(f"Deleting orphan artifact: {f.name} (derived device_id: {device_id})")
                f.unlink()
                count += 1
                
        except Exception as e:
            logger.error(f"Error processing {f.name}: {e}")

    logger.info(f"Cleanup complete. Deleted {count} orphaned history file(s).")

if __name__ == "__main__":
    clean_orphans()
