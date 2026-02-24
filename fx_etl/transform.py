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
    source = "exchangerate-api"     # additional column for all records


    # schema properly updated
    cleaned = []
    for currency, value in rates.items(): 
        if currency == base:    # skips the self rate record
            continue

        fval = safe_float(value)
        if fval is None and fval < 0:          # skip rates with empty & negative values
            continue
            
        cleaned.append(
            {
                "rate_date": date,
                "base_currency": base,
                "target_currency": currency,
                "rate": fval,
                "source": source,
            }
        )
    return cleaned