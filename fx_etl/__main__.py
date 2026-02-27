from fx_etl.cli import parse_cli_args
from .main import run

def _run():
    args = parse_cli_args()
    run(run_date=args.run_date, base=args.base)

if __name__ == "__main__":
    _run()
