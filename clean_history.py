#!/usr/bin/env python3
import json
import glob
from pathlib import Path

def clean_history():
    history_files = glob.glob("data/history/*.json")
    for file_path in history_files:
        with open(file_path, "r") as f:
            data = json.load(f)
            
        if "history" in data:
            # Keep only entries with status 'current'
            original_len = len(data["history"])
            data["history"] = [e for e in data["history"] if e.get("status") == "current"]
            
            # If no current was found (unlikely but possible), keep the first one
            if not data["history"] and original_len > 0:
                 # Should not happen in normal use but safe fallback
                 pass 
            
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Cleaned {file_path}: {original_len} -> {len(data['history'])} entries")

if __name__ == "__main__":
    clean_history()
