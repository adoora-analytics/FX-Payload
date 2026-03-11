import csv
import json
import os
import tempfile

from fx_etl.config import PROCESSED_DIR


# read csv is now tolerant of empty/bad records
def read_csv(name):
    path = PROCESSED_DIR / f"{name}.csv"
    if not path.exists() or path.stat().st_size == 0:
        return []

    with path.open("r", newline="", encoding="utf-8") as f:
        try:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return []

            rows = []
            for row in reader:
                # skip completely empty rows
                if not row or all((v is None or str(v).strip() == "") for v in row.values()):
                    continue
                    rows.append(row)
            return rows
        except csv.Error:
            # if csv is malformed, treat as no history to prevent crashing reruns
            return []

def save_json(records, name):
    path = PROCESSED_DIR / f"{name}.json"
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return path


def save_csv(records, name):
    path = PROCESSED_DIR / f"{name}.csv"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # decide schema 
    if records:
        fieldnames = list(records[0].keys())
    else:
        # if no records, keep/clear file safely
        fieldnames = []

    # writes to temp file first, then replace (atomic)
    fd, tmp_path = tempfile.mkstemp(prefix=f"{name}_", suffix=".csv", dir=str(PROCESSED_DIR))
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            if fieldnames:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            else:
                # no records - create an empty file
                f.write("")

        os.replace(tmp_path, path)
        return path

    except Exception:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise