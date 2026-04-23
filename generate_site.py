import shutil
import logging
import os
import json
from pathlib import Path
from jinja2 import Template
from config import REGION_MAPPING, DEVICE_METADATA, OOS_MAPPING, SPRING_MAPPING

def generate(template_path: Path, output_path: Path, db_path: Path):
    """Core logic to generate the site."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Process template with Jinja for metadata (GA, etc)
    try:
        template_content = template_path.read_text(encoding="utf-8")
        template = Template(template_content)
        
        ga_id = os.environ.get("GOOGLE_ANALYTICS_ID")
        
        # Convert mapping to JSON for injection into script tag
        region_map_json = json.dumps(REGION_MAPPING)
        
        rendered = template.render(
            ga_id=ga_id,
            region_map_json=region_map_json
        )
        
        output_path.write_text(rendered, encoding="utf-8")
        logging.info(f"Site generated successfully with Jinja metadata at {output_path}")
    except Exception as e:
        logging.error(f"Failed to render template: {e}")
        # Fallback to copy if jinja fails
        shutil.copy2(template_path, output_path)

    # Copy database.json for local/SPA fetching
    if db_path.exists():
        shutil.copy2(db_path, output_path.parent / "database.json")
        logging.info(f"Database copied to {output_path.parent / 'database.json'}")

    # Copy static assets (css, js)
    for asset_dir in ["css", "js"]:
        src = template_path.parent / asset_dir
        dst = output_path.parent / asset_dir
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            logging.info(f"Asset directory {asset_dir} copied to {dst}")

    # Generate mapping.json for the bot
    try:
        mapping_data = {
            "DEVICE_METADATA": DEVICE_METADATA,
            "OOS_MAPPING": OOS_MAPPING,
            "SPRING_MAPPING": SPRING_MAPPING
        }
        mapping_path = output_path.parent / "mapping.json"
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping_data, f, ensure_ascii=False, indent=2)
        logging.info(f"Mapping generated at {mapping_path}")
    except Exception as e:
        logging.error(f"Failed to generate mapping.json: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    BASE_DIR = Path(__file__).resolve().parent
    DATABASE_PATH = BASE_DIR / 'data' / 'database.json'
    OUTPUT_PATH = BASE_DIR / 'page' / 'index.html'
    TEMPLATE_PATH = BASE_DIR / 'templates' / 'index.html'
    
    generate(TEMPLATE_PATH, OUTPUT_PATH, DATABASE_PATH)
