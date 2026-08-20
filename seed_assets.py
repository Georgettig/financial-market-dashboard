from database.connection import engine
from database.models import Base
from database.repository import add_asset


ASSETS = [
    {
        "symbol": "AAPL",
        "name": "Apple",
        "market": "US",
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft",
        "market": "US",
    },
    {
        "symbol": "GOOGL",
        "name": "Alphabet",
        "market": "US",
    },
    {
        "symbol": "AMZN",
        "name": "Amazon",
        "market": "US",
    },
    {
        "symbol": "META",
        "name": "Meta Platforms",
        "market": "US",
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA",
        "market": "US",
    },
    {
        "symbol": "TSLA",
        "name": "Tesla",
        "market": "US",
    },
    {
        "symbol": "AMD",
        "name": "Advanced Micro Devices",
        "market": "US",
    },
    {
        "symbol": "INTC",
        "name": "Intel",
        "market": "US",
    },
    {
        "symbol": "ORCL",
        "name": "Oracle",
        "market": "US",
    },
    {
        "symbol": "IBM",
        "name": "IBM",
        "market": "US",
    },
    {
        "symbol": "JPM",
        "name": "JPMorgan Chase",
        "market": "US",
    },
    {
        "symbol": "WMT",
        "name": "Walmart",
        "market": "US",
    },
    {
        "symbol": "KO",
        "name": "Coca-Cola",
        "market": "US",
    },
    {
        "symbol": "NFLX",
        "name": "Netflix",
        "market": "US",
    },
]


def seed_assets():

    Base.metadata.create_all(engine)

    inserted = 0
    skipped = 0

    for asset in ASSETS:

        created = add_asset(
            symbol=asset["symbol"],
            name=asset["name"],
            market=asset["market"],
        )

        if created:

            print(
                f"✓ {asset['symbol']} - "
                f"{asset['name']} cadastrado."
            )

            inserted += 1

        else:

            print(
                f"- {asset['symbol']} já existe."
            )

            skipped += 1

    print()
    print("================================")
    print("Cadastro finalizado")
    print("================================")
    print(f"Novos ativos: {inserted}")
    print(f"Já existentes: {skipped}")


if __name__ == "__main__":
    seed_assets()