import sys
import logging

from fx_etl.cli import parse_cli_args
from fx_etl.logger import setup_logging
from fx_etl.main import run

log = logging.getLogger("fx_etl") 

def main() -> None:
    setup_logging(log_dir="logs", level="INFO")
    args = parse_cli_args()

    try:
        code = run(run_date=args.run_date, base=args.base)
        sys.exit(code)
    except Exception as exc:
        log.exception("FX ETL failed: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()
