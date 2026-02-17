def natural_key(record):
    """Business key for FX rates """

    return (
        record["base_currency"],
        record["target_currency"],
        record["rate_date"],
    )


def deduplicate(new_records, existing_records):
    """ keep only records whose natural key does not already exist """

    seen = {natural_key(r) for r in existing_records} 

    clean = [
        r for r in new_records
        if natural_key(r) not in seen
    ]

    return clean