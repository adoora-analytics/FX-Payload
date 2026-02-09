from extract import fetch_latest_rates

def main():
    data = fetch_latest_rates()
    print(data)

if __name__ == "__main__":
    main()

