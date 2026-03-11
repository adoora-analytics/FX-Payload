# natural key made more defensive by wrapping in try & except
def natural_key(record):
    """Business key for FX rates """
    try:
        return (
            record["base_currency"],
            record["target_currency"],
            record["rate_date"],
        )
    except KeyError:
        return None


# prevent historical rows from crashing reruns
def deduplicate(new_records, existing_records):
    """ keep only records whose natural key does not already exist """

    seen = {
        natural_key(r) 
        for r in existing_records
        if natural_key(r) is not None
        } 

    clean = [
        r for r in new_records
        if natural_key(r) not in seen
    ]

    return clean