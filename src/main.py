from extract import fetch_latest_rates, save_raw
from transform import normalize_rates
from dedup import deduplicate
from load import save_json, save_csv, read_csv
from validate import validate_rows

def run():
    # extract
    raw_fx = fetch_latest_rates()
    raw_path = save_raw(raw_fx, "fx_raw_usd")   

    # transform
    transformed_records = normalize_rates(raw_fx)

    # validate
    validated = validate_rows(transformed_records)  # returns list[FxRow]
    validated_dicts = [v.__dict__ for v in validated] 

    # load existing & new records
    existing_records = read_csv("fx_rates_usd_clean")
    new_records = deduplicate(transformed_records, existing_records)

    # merge + save
    final_records = existing_records + new_records
             
    # save CSV & JSON
    csv_path = save_csv(final_records, "fx_rates_USD_clean")     
    json_path = save_json(final_records, "fx_rates_USD_clean")   


    print("ETL complete")               # indicates ETL completion
    print("Raw:", raw_path)             # prints raw API response
    print("JSON:", json_path)           # prints path to cleaned JSON
    print("CSV:", csv_path)             # prints path to cleaned CSV
    print("Rows:", len(final_records))  # prints number of records in cleaned data

if __name__ == "__main__":
    run()



