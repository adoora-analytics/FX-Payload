# Data Model

Each record contains:

- base_currency (str)
- target_currency (str)
- rate (float)
- rate_date (date)
- ingested_at (timestamp)

Natural Key:
(base_currency, target_currency, rate_date)
