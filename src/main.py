from extract import fetch_latest_rates, save_raw
from transform import normalize_rates
from load import save_json, save_csv

def main():
    # extract
    raw = fetch_latest_rates()
    raw_path = save_raw(raw, "fx_raw_usd")   

    # transform
    cleaned = normalize_rates(raw)          

    # load
    csv_path = save_csv(cleaned, "fx_rates_USD_clean")     
    json_path = save_json(cleaned, "fx_rates_USD_clean")   


    print("ETL complete")           # indicates ETL completion
    print("Raw:", raw)              # prints raw API response
    print("JSON:", json_path)       # prints path to cleaned JSON
    print("CSV:", csv_path)         # prints path to cleaned CSV
    print("Rows:", len(cleaned))    # prints number of records in cleaned data
    

if __name__ == "__main__":
    main()



