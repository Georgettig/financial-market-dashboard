import pandas as pd

def transform_data(data: dict) -> pd.DataFrame:

    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(
        time_series,
        orient="index"
    )

    df.index = pd.to_datetime(df.index)

    df = df.rename(
        columns = {
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        }
    )

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": int
    })

    df = df.sort_index()

    df.index.name = "date"

    return df