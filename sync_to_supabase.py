#!/usr/bin/env python3
"""
Sync database.json to Supabase (1:1).
Models and versions that exist in database.json are upserted.
Models and versions NOT in database.json are deleted from Supabase.
"""

import os
import json
import logging
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
SUPABASE_SCHEMA = os.environ.get("SUPABASE_SCHEMA", "arb_checker")
DATABASE_PATH = Path("data/database.json")

HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

MODELS_TABLE = "models"
VERSIONS_TABLE = "versions"


def supabase_request(method, table, params=None, json_data=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = HEADERS.copy()
    headers["Accept-Profile"] = SUPABASE_SCHEMA
    headers["Content-Profile"] = SUPABASE_SCHEMA
    resp = requests.request(method, url, headers=headers, params=params, json=json_data)
    if resp.status_code >= 400 and resp.status_code != 204:
        logger.error(f"Supabase {method} {table} failed: {resp.status_code} {resp.text}")
        resp.raise_for_status()
    return resp


def get_existing_model_ids():
    resp = supabase_request("GET", MODELS_TABLE, params={"select": "model_id"})
    return {row["model_id"] for row in resp.json()}


def get_existing_version_keys():
    resp = supabase_request("GET", VERSIONS_TABLE, params={"select": "model_id,version_name"})
    return {(row["model_id"], row["version_name"]) for row in resp.json()}


def upsert_models(models_data):
    rows = []
    for model_id, meta in models_data.items():
        rows.append({
            "model_id": model_id,
            "device_name": meta["device_name"],
            "device_order": meta["device_order"],
            "expect_esim": meta.get("expect_esim", False),
            "expect_barometer": meta.get("expect_barometer", False),
        })
    if rows:
        headers = HEADERS.copy()
        headers["Accept-Profile"] = SUPABASE_SCHEMA
        headers["Content-Profile"] = SUPABASE_SCHEMA
        headers["Prefer"] = "resolution=merge-duplicates"
        url = f"{SUPABASE_URL}/rest/v1/{MODELS_TABLE}?on_conflict=model_id"
        resp = requests.post(url, headers=headers, json=rows)
        if resp.status_code >= 400:
            logger.error(f"Supabase POST models failed: {resp.status_code} {resp.text}")
            resp.raise_for_status()
        logger.info(f"Upserted {len(rows)} models")


def upsert_versions(models_data):
    rows = []
    for model_id, meta in models_data.items():
        for version_name, ver in meta["versions"].items():
            md5 = ver.get("md5")
            if md5 and isinstance(md5, dict):
                md5 = json.dumps(md5)
            rows.append({
                "model_id": model_id,
                "version_name": version_name,
                "arb": ver["arb"],
                "major": ver["major"],
                "minor": ver["minor"],
                "md5": md5,
                "first_seen": ver["first_seen"],
                "last_checked": ver["last_checked"],
                "status": ver["status"],
                "is_hardcoded": ver.get("is_hardcoded", False),
                "regions": ver.get("regions", []),
            })
    if rows:
        headers = HEADERS.copy()
        headers["Accept-Profile"] = SUPABASE_SCHEMA
        headers["Content-Profile"] = SUPABASE_SCHEMA
        headers["Prefer"] = "resolution=merge-duplicates"
        url = f"{SUPABASE_URL}/rest/v1/{VERSIONS_TABLE}?on_conflict=model_id,version_name"
        resp = requests.post(url, headers=headers, json=rows)
        if resp.status_code >= 400:
            logger.error(f"Supabase POST versions failed: {resp.status_code} {resp.text}")
            resp.raise_for_status()
        logger.info(f"Upserted {len(rows)} versions")


def delete_models(model_ids_to_delete):
    for mid in model_ids_to_delete:
        supabase_request("DELETE", MODELS_TABLE, params={"model_id": f"eq.{mid}"})
    if model_ids_to_delete:
        logger.info(f"Deleted {len(model_ids_to_delete)} models (and their versions via cascade)")


def delete_versions(version_keys_to_delete):
    for model_id, version_name in version_keys_to_delete:
        supabase_request(
            "DELETE", VERSIONS_TABLE,
            params={"model_id": f"eq.{model_id}", "version_name": f"eq.{version_name}"},
        )
    if version_keys_to_delete:
        logger.info(f"Deleted {len(version_keys_to_delete)} orphaned versions")


def sync():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        logger.error("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        raise SystemExit(1)

    if not DATABASE_PATH.exists():
        logger.error(f"{DATABASE_PATH} not found")
        raise SystemExit(1)

    with open(DATABASE_PATH) as f:
        data = json.load(f)

    logger.info(f"Loaded {len(data)} models from database.json")

    existing_models = get_existing_model_ids()
    existing_versions = get_existing_version_keys()
    logger.info(f"Supabase has {len(existing_models)} models, {len(existing_versions)} versions")

    json_model_ids = set(data.keys())

    json_version_keys = set()
    for model_id, meta in data.items():
        for version_name in meta.get("versions", {}):
            json_version_keys.add((model_id, version_name))

    # Upsert everything from database.json
    upsert_models(data)
    upsert_versions(data)

    # Delete models that no longer exist in database.json
    models_to_delete = existing_models - json_model_ids
    if models_to_delete:
        logger.info(f"Models to remove: {models_to_delete}")
        delete_models(models_to_delete)

    # Delete versions that no longer exist in database.json
    versions_to_delete = existing_versions - json_version_keys
    if versions_to_delete:
        delete_versions(versions_to_delete)

    if not models_to_delete and not versions_to_delete:
        logger.info("Supabase is already in sync — no deletions needed")

    logger.info("Sync complete")


if __name__ == "__main__":
    sync()
