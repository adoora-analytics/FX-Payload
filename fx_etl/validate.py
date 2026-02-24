from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, timezone
from email.utils import parsedate_to_datetime
import math


@dataclass(frozen=True)
class FxRow:
    rate_date: str           # normalized to 'YYYY-MM-DD'
    base_currency: str
    target_currency: str
    rate: float
    source: str


def _normalize_date(value: str) -> str:
    """
    Accepts:
      - 'YYYY-MM-DD'
      - RFC 2822-ish: 'Tue, 10 Feb 2026 00:02:32 +0000'  (your API field)
      - ISO datetime: '2026-02-10T00:02:32Z' etc.
    Returns: 'YYYY-MM-DD'
    """
    s = str(value).strip()

    # already ISO date
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        y, m, d = map(int, s.split("-"))
        _ = date(y, m, d)
        return s

    # RFC-style date (your case)
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.date().isoformat()
    except Exception:
        pass

    # ISO datetime fallback
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.date().isoformat()
    except Exception as e:
        raise ValueError(f"Unparseable rate_date: {s!r}") from e


def validate_rows(rows: list[dict]) -> list[FxRow]:
    if not rows:
        raise ValueError("Validation failed: 0 rows after transform")

    validated: list[FxRow] = []
    errors: list[str] = []
    seen_keys: set[tuple[str, str, str]] = set()

    for i, r in enumerate(rows):
        try:
            rate_date = _normalize_date(r["rate_date"])
            base = str(r["base_currency"]).upper().strip()
            target = str(r["target_currency"]).upper().strip()
            source = str(r.get("source", "")).strip() or "unknown"

            rate = r["rate"]
            if rate is None:
                raise ValueError("rate is None")
            rate = float(rate)

            # ISO code sanity
            if len(base) != 3 or not base.isalpha():
                raise ValueError(f"bad base_currency={base!r}")
            if len(target) != 3 or not target.isalpha():
                raise ValueError(f"bad target_currency={target!r}")

            # business rules
            if base == target:
                raise ValueError("base equals target (self-rate)")
            if not math.isfinite(rate) or rate <= 0:
                raise ValueError(f"invalid rate={rate}")

            key = (rate_date, base, target)
            if key in seen_keys:
                raise ValueError(f"duplicate business key in run: {key}")
            seen_keys.add(key)

            validated.append(
                FxRow(
                    rate_date=rate_date,
                    base_currency=base,
                    target_currency=target,
                    rate=rate,
                    source=source,
                )
            )

        except Exception as e:
            errors.append(f"row[{i}] invalid: {e} | raw={r}")

    if errors:
        raise ValueError("Validation failed:\n" + "\n".join(errors[:10]))

    return validated