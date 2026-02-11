def safe_float(x):
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def safe_str(x):
    if x is None:
        return None
    s = str(x).strip()
    return s if s else None


def normalize_rates(raw_fx):
    """
    convert nested rates dict into a list of records:
    """
    
    base = raw_fx.get("base_code") 
    rates = raw_fx.get("rates", {})
    date = raw_fx.get("time_last_update_utc")


    cleaned = []
    for quote, rate in rates.items():
        cleaned.append(
            {
                "date": date,
                "base": base,
                "quote": quote,
                "rate": safe_float(rate),
            }
        )
    return cleaned