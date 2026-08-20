import pandas as pd

def calculate_daily_return(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["daily_return"] = df["close"].pct_change()

    return df

def calculate_cumulative_return(df:pd.Dataframe) -> pd.DataFrame:

    df = df.copy()

    df["cumulative_return"] = (
        (1 + df["daily_return"]).cumprod() - 1
    )

    return df

def calculate_moving_average(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:

    df = df.copy()

    df[f"moving_average_{window}"] = (
        df["close"].rolling(window=window).mean()
    )

    return df

def calculate_summary(df: pd.DataFrame) -> dict:

    summary = {
        "initial_price": df["close"].iloc[0],
        "final_price": df["close"].iloc[-1],
        "maximum_price": df["high"].max(),
        "minimum_price": df["low"].min(),
        "average_volume": df["volume"].mean(),
        "volatility": df["daily_return"].std()
    }

    return summary