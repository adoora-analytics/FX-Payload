from extract import fetch_latest_rates
from transform import normalize_rates

def main():
    raw = fetch_latest_rates()
    records = normalize_rates(raw)
    print(len(records))

if __name__ == "__main__":
    main()



