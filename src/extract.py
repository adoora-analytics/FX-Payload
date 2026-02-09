import json
from datetime import datetime, timezone

import requests

from config import BASE_URL, RAW_DIR, TIMEOUT_SECONDS


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fetch_latest_rates(base_currency="USD"):
    url = f"{BASE_URL}/latest/{base_currency}"
    resp = requests.get(url, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()  # crash loudly if API fails
    data = resp.json() # fx APIs always returns a dict, not lists

    if not isinstance(data, dict):
        raise ValueError("Expected a dict of FX payload!")

    return data

def save_raw(data, name):
    path = RAW_DIR / f"{name}_{utc_stamp()}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path