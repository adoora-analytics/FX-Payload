
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo


LAGOS_TZ = ZoneInfo("Africa/Lagos")
CURRENCY_RE = re.compile(r"^[A-Za-z]{3}$")


@dataclass(frozen=True)
class CLIArgs:
    run_date: str  # "YYYY-MM-DD"
    base: str      # "USD"


def _parse_date(value: str) -> str:
    """
    Accept YYYY-MM-DD. Reject invalid dates and future dates (Africa/Lagos).
    Returns the same YYYY-MM-DD string if valid.
    """
    try:
        d = date.fromisoformat(value)  # strict ISO format
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid --date '{value}'. Use YYYY-MM-DD (e.g., 2026-02-14)."
        ) from e

    today_lagos = datetime.now(LAGOS_TZ).date()
    if d > today_lagos:
        raise argparse.ArgumentTypeError(
            f"Invalid --date '{value}'. Date cannot be in the future (Africa/Lagos)."
        )

    return d.isoformat()


def _parse_currency(value: str) -> str:
    """
    Accept 3-letter currency codes. Normalizes to uppercase.
    """
    v = value.strip().upper()
    if not CURRENCY_RE.fullmatch(v):
        raise argparse.ArgumentTypeError(
            f"Invalid --base '{value}'. Must be a 3-letter currency code (e.g., USD, EUR)."
        )
    return v


def _default_date_lagos() -> str:
    return datetime.now(LAGOS_TZ).date().isoformat()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m fx_etl",
        description="Run the FX ETL pipeline."
    )
    p.add_argument(
        "--date",
        dest="run_date",
        type=_parse_date,
        default=_default_date_lagos(),
        help="Run date in YYYY-MM-DD (default: today in Africa/Lagos).",
    )
    p.add_argument(
        "--base",
        dest="base",
        type=_parse_currency,
        default="USD",
        help="Base currency (default: USD).",
    )
    return p


def parse_cli_args(argv: list[str] | None = None) -> CLIArgs:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return CLIArgs(run_date=ns.run_date, base=ns.base)