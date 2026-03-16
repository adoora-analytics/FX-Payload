import logging

from fx_etl.extract import fetch_latest_rates, save_raw
from fx_etl.transform import normalize_rates
from fx_etl.dedup import deduplicate
from fx_etl.load import save_json, save_csv, read_csv
from fx_etl.validate import validate_rows
from fx_etl.logger import setup_logging

log = logging.getLogger("fx_etl")

def run(run_date: str, base: str) -> int:


    # extract
    log.info("[EXTRACT] start run_date=%s base=%s", run_date, base)
    raw_fx = fetch_latest_rates(run_date=run_date, base=base)         # base means: 1 USD = X currency
    raw_path = save_raw(raw_fx, f"fx_raw_{base.lower()}")

     # log something stable even if raw_fx is dict/json
    raw_keys = list(raw_fx.keys())[:15] if isinstance(raw_fx, dict) else []
    log.info("[EXTRACT] done raw_saved=%s keys_sample=%s", raw_path, raw_keys)

    
    # transform
    log.info("[TRANSFORM] start")
    transformed_records = normalize_rates(raw_fx, run_date=run_date, base=base)
    log.info("[TRANSFORM] done records=%d", len(transformed_records))

    # validate
    log.info("[VALIDATE] start")
    validated = validate_rows(transformed_records)  # returns list[FxRow]
    validated_dicts = [v.__dict__ for v in validated] 

    invalid_count = len(transformed_records) - len(validated_dicts)
    log.info(
        "[VALIDATE] done valid=%d invalid=%d total=%d",
        len(validated_dicts),
        invalid_count,
        len(transformed_records),
    )

    # Fail-fast boundary: no valid data means pipeline should not proceed.
    if len(validated_dicts) == 0:
        raise RuntimeError(
            f"Validation produced zero valid records (run_date={run_date}, base={base})."
        )

    # load existing & dedupe records
    # existing 
    clean_name = f"fx_rates_{base.lower()}_clean"
    existing_records = read_csv(clean_name)
    log.info("[DEDUPE] start existing=%d", len(existing_records))
    
    # dedupe 
    new_records = deduplicate(validated_dicts, existing_records)
    log.info(
        "[DEDUPE] done incoming_valid=%d new_unique=%d",
        len(validated_dicts),
        len(new_records),
    )
    # merge + save
    final_records = existing_records + new_records
             
    # save CSV & JSON
    csv_path = save_csv(final_records, clean_name)     
    json_path = save_json(final_records, clean_name)   


    log.info("[LOAD] done total_written=%d csv=%s json=%s", len(final_records), csv_path, json_path)
    return 0



