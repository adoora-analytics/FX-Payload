from __future__ import annotations

import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir: str, level: str = "INFO") -> str:
    """
    Creates a root logger that writes to:
      1) console (stdout)
      2) a rotating file under log_dir/

    Returns a run_id string that can correlate all logs from one run.
    """
    os.makedirs(log_dir, exist_ok=True)

    run_id = uuid.uuid4().hex[:12]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logfile = os.path.join(log_dir, f"fx_etl_{ts}_{run_id}.log")

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()  # important: avoids duplicate logs when re-running in VS Code

    formatter = logging.Formatter(
        fmt="%(asctime)sZ | %(levelname)s | run=%(run_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    class RunIdFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.run_id = run_id
            return True

    # Console handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    sh.addFilter(RunIdFilter())
    root.addHandler(sh)

    # File handler (rotates to prevent huge log files)
    fh = RotatingFileHandler(
        logfile,
        maxBytes=2_000_000,   # ~2MB per file
        backupCount=5,        # keeps last 5 rotated logs
        encoding="utf-8",
    )
    fh.setFormatter(formatter)
    fh.addFilter(RunIdFilter())
    root.addHandler(fh)

    # Reduce noisy dependency logs (optional)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return run_id