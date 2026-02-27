import logging

from fx_etl.extract import fetch_latest_rates, save_raw
from fx_etl.transform import normalize_rates
from fx_etl.dedup import deduplicate
from fx_etl.load import save_json, save_csv, read_csv
from fx_etl.validate import validate_rows
from fx_etl.logger import setup_logging

log = logging.getLogger("fx_etl")

def run(run_date: str, base: str) -> None:

    #  log setup (console + logs/ file)
    setup_logging(log_dir="logs", level="INFO")
    log.info("ETL run started")


    # extract
    raw_fx = fetch_latest_rates(run_date=run_date, base=base)         # base means: 1 USD = X currency
    raw_path = save_raw(raw_fx, f"fx_raw_{base.lower()}")
    log.info("raw saved to %s", raw_path)

    # transform
    transformed_records = normalize_rates(raw_fx, run_date=run_date, base=base)
    log.info("transform produced %d rows", len(transformed_records))

    # validate
    validated = validate_rows(transformed_records)  # returns list[FxRow]
    validated_dicts = [v.__dict__ for v in validated] 
    log.info("validation passed for %d rows", len(validated_dicts))

    # load existing & dedupe records
    # existing 
    clean_name = f"fx_rates_{base.lower()}_clean"
    existing_records = read_csv(clean_name)
    log.info("loaded existing rows=%d from %s.csv", len(existing_records), clean_name)
    
    # dedupe 
    new_records = deduplicate(validated_dicts, existing_records)
    log.info("new unique rows after dedupe=%d", len(new_records))

    # merge + save
    final_records = existing_records + new_records
             
    # save CSV & JSON
    csv_path = save_csv(final_records, clean_name)     
    json_path = save_json(final_records, clean_name)   


    log.info("ETL complete")
    log.info("raw:  %s", raw_path)
    log.info("json: %s", json_path)
    log.info("csv:  %s", csv_path)
    log.info("appended rows: %d", len(new_records))


if __name__ == "__main__":
    try:
        run()
    except Exception:
        log.exception("ETL failed")
        raise



