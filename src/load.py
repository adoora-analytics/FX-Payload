import csv
import json

from config import PROCESSED_DIR


def save_json(records, name):
    path = PROCESSED_DIR / f"{name}.json"
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return path


def save_csv(records, name):
    path = PROCESSED_DIR / f"{name}.csv"

    if not records:
        path.write_text("", encoding="utf-8")
        return path

    fieldnames = list(records[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return path