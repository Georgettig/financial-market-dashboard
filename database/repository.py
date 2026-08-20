import pandas as pd

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Asset, StockPrice


# STOCK PRICES

def save_stock_data(
    df: pd.DataFrame,
    symbol: str,
) -> int:

    inserted_count = 0

    with Session(engine) as session:

        for index, row in df.iterrows():

            stock_date = index.date()

            existing = session.scalar(
                select(StockPrice).where(
                    StockPrice.symbol == symbol,
                    StockPrice.date == stock_date,
                )
            )

            if existing is not None:
                continue

            stock_price = StockPrice(
                symbol=symbol,
                date=stock_date,
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"],
            )

            session.add(stock_price)

            inserted_count += 1

        session.commit()

    return inserted_count


def get_stock_data(
    symbol: str,
) -> pd.DataFrame:

    with Session(engine) as session:

        result = session.scalars(
            select(StockPrice)
            .where(
                StockPrice.symbol == symbol
            )
            .order_by(
                StockPrice.date
            )
        )

        records = result.all()

    if not records:

        return pd.DataFrame()

    data = [
        {
            "date": record.date,
            "open": float(record.open),
            "high": float(record.high),
            "low": float(record.low),
            "close": float(record.close),
            "volume": record.volume,
        }
        for record in records
    ]

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df.set_index("date")


def get_latest_date(
    symbol: str,
):

    with Session(engine) as session:

        latest_date = session.scalar(
            select(
                func.max(StockPrice.date)
            ).where(
                StockPrice.symbol == symbol
            )
        )

    return latest_date


# ASSETS

def add_asset(
    symbol: str,
    name: str,
    market: str,
) -> bool:

    symbol = symbol.upper().strip()

    with Session(engine) as session:

        existing = session.scalar(
            select(Asset).where(
                Asset.symbol == symbol
            )
        )

        if existing is not None:

            return False

        asset = Asset(
            symbol=symbol,
            name=name,
            market=market,
            active=True,
        )

        session.add(asset)

        session.commit()

        return True


def get_active_assets():

    with Session(engine) as session:

        result = session.scalars(
            select(Asset)
            .where(
                Asset.active.is_(True)
            )
            .order_by(
                Asset.symbol
            )
        )

        return result.all()


def get_active_symbols() -> list[str]:

    with Session(engine) as session:

        result = session.scalars(
            select(Asset.symbol)
            .where(
                Asset.active.is_(True)
            )
            .order_by(
                Asset.symbol
            )
        )

        return list(result)


def get_available_symbols() -> list[str]:

    with Session(engine) as session:

        result = session.scalars(
            select(StockPrice.symbol)
            .distinct()
            .order_by(StockPrice.symbol)
        )

        return list(result)