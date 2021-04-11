import uuid


def map_ticker(source):
    return {
        "Key": uuid.uuid4(),
        "UtcDate": source["time"]["updatedISO"],
        "Asset": "BTC",
        "PriceUsd": float(source["bpi"]["USD"]["rate_float"]),
        "PriceGbp": float(source["bpi"]["GBP"]["rate_float"]),
        "PriceEur": float(source["bpi"]["EUR"]["rate_float"])
    }
